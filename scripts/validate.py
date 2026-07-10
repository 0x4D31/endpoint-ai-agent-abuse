#!/usr/bin/env python3
"""Validate the EAA catalog and its Markdown projections using only stdlib."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import unquote, urlsplit, urlunsplit


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = ROOT / "data" / "catalog.json"
DEFAULT_SCHEMA = ROOT / "data" / "catalog.schema.json"

OUTCOME_SUPPORT = {
    "present": "artifact-present",
    "planted": "procedure-planted",
    "attempted": "execution-attempted",
    "executed": "execution-confirmed",
    "impact-confirmed": "impact-confirmed",
}


class DuplicateKeyError(ValueError):
    pass


def object_without_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError(f"duplicate object key: {key!r}")
        result[key] = value
    return result


def load_json(path: Path) -> Any:
    try:
        return json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=object_without_duplicate_keys,
        )
    except (OSError, UnicodeError, json.JSONDecodeError, DuplicateKeyError) as exc:
        try:
            display_path = path.resolve().relative_to(ROOT)
        except ValueError:
            display_path = path
        raise SystemExit(f"{display_path}: invalid JSON: {exc}") from exc


def json_path(parent: str, child: str | int) -> str:
    if isinstance(child, int):
        return f"{parent}[{child}]"
    return f"{parent}.{child}" if parent else child


def resolve_ref(schema_root: dict[str, Any], reference: str) -> dict[str, Any]:
    if not reference.startswith("#/"):
        raise ValueError(f"unsupported non-local schema reference: {reference}")
    current: Any = schema_root
    for raw_part in reference[2:].split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        current = current[part]
    if not isinstance(current, dict):
        raise ValueError(f"schema reference does not resolve to an object: {reference}")
    return current


def type_matches(value: Any, expected: str) -> bool:
    # bool is a subclass of int in Python, so check it explicitly.
    return {
        "object": isinstance(value, dict),
        "array": isinstance(value, list),
        "string": isinstance(value, str),
        "integer": isinstance(value, int) and not isinstance(value, bool),
        "number": isinstance(value, (int, float)) and not isinstance(value, bool),
        "boolean": isinstance(value, bool),
        "null": value is None,
    }.get(expected, False)


def validate_format(value: str, format_name: str) -> bool:
    if format_name == "date":
        try:
            return dt.date.fromisoformat(value).isoformat() == value
        except ValueError:
            return False
    if format_name == "uri":
        parsed = urlsplit(value)
        return bool(parsed.scheme and parsed.netloc and not parsed.username and not parsed.password)
    return True


def validate_against_schema(
    value: Any,
    schema: dict[str, Any],
    schema_root: dict[str, Any],
    path: str = "$",
) -> list[str]:
    """Validate the schema subset used by catalog.schema.json.

    Keeping this small subset in-tree makes CI deterministic and dependency-free.
    Unknown schema keywords are annotations from Draft 2020-12 or are deliberately
    handled by catalog-specific semantic checks below.
    """
    if "$ref" in schema:
        try:
            target = resolve_ref(schema_root, schema["$ref"])
        except (KeyError, TypeError, ValueError) as exc:
            return [f"{path}: invalid schema reference {schema['$ref']!r}: {exc}"]
        return validate_against_schema(value, target, schema_root, path)

    errors: list[str] = []
    expected_type = schema.get("type")
    if expected_type and not type_matches(value, expected_type):
        return [f"{path}: expected {expected_type}, got {type(value).__name__}"]

    if "const" in schema and value != schema["const"]:
        errors.append(f"{path}: expected constant {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: expected one of {schema['enum']!r}, got {value!r}")

    if isinstance(value, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                errors.append(f"{json_path(path, key)}: required property is missing")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in properties:
                    errors.append(f"{json_path(path, key)}: unknown property")
        for key, child in value.items():
            child_schema = properties.get(key)
            if child_schema is not None:
                errors.extend(
                    validate_against_schema(
                        child,
                        child_schema,
                        schema_root,
                        json_path(path, key),
                    )
                )

    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: expected at least {schema['minItems']} item(s)")
        if schema.get("uniqueItems"):
            seen: set[str] = set()
            for index, item in enumerate(value):
                fingerprint = json.dumps(item, sort_keys=True, ensure_ascii=False)
                if fingerprint in seen:
                    errors.append(f"{json_path(path, index)}: duplicate array item")
                seen.add(fingerprint)
        item_schema = schema.get("items")
        if item_schema is not None:
            for index, child in enumerate(value):
                errors.extend(
                    validate_against_schema(
                        child,
                        item_schema,
                        schema_root,
                        json_path(path, index),
                    )
                )

    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}: string is shorter than {schema['minLength']}")
        pattern = schema.get("pattern")
        if pattern and re.search(pattern, value) is None:
            errors.append(f"{path}: does not match pattern {pattern!r}")
        format_name = schema.get("format")
        if format_name and not validate_format(value, format_name):
            errors.append(f"{path}: invalid {format_name}")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{path}: must be at least {schema['minimum']}")

    return errors


def duplicates(values: Iterable[str]) -> set[str]:
    seen: set[str] = set()
    repeated: set[str] = set()
    for value in values:
        if value in seen:
            repeated.add(value)
        seen.add(value)
    return repeated


def normalize_url(url: str) -> str:
    parsed = urlsplit(url)
    path = parsed.path.rstrip("/") or "/"
    return urlunsplit(
        (parsed.scheme.lower(), parsed.netloc.lower(), path, parsed.query, parsed.fragment)
    )


def schema_enum(schema: dict[str, Any], definition: str) -> list[str]:
    return list(schema["$defs"][definition]["enum"])


def validate_catalog_semantics(
    catalog: dict[str, Any],
    schema: dict[str, Any],
    *,
    check_repository_version: bool,
) -> list[str]:
    errors: list[str] = []
    techniques = catalog.get("techniques", [])
    cases = catalog.get("cases", [])
    candidates = catalog.get("candidates", [])
    surfaces = catalog.get("surfaces", [])
    sources = catalog.get("sources", [])

    technique_ids = [item.get("id", "") for item in techniques if isinstance(item, dict)]
    case_ids = [item.get("id", "") for item in cases if isinstance(item, dict)]
    candidate_ids = [item.get("id", "") for item in candidates if isinstance(item, dict)]
    surface_ids = [item.get("id", "") for item in surfaces if isinstance(item, dict)]
    surface_names = [item.get("name", "") for item in surfaces if isinstance(item, dict)]
    source_ids = [item.get("id", "") for item in sources if isinstance(item, dict)]

    for label, values in (
        ("technique ID", technique_ids),
        ("case ID", case_ids),
        ("candidate ID", candidate_ids),
        ("source ID", source_ids),
        ("surface ID", surface_ids),
        ("surface name", [name.casefold() for name in surface_names]),
    ):
        repeated = sorted(duplicates(values))
        if repeated:
            errors.append(f"duplicate {label}(s): {', '.join(repeated)}")

    expected_ids = [f"EAA-{number:03d}" for number in range(1, len(technique_ids) + 1)]
    if technique_ids != expected_ids:
        errors.append(
            "$.techniques: IDs must be unique, contiguous, and sorted; expected "
            + ", ".join(expected_ids)
        )
    expected_case_ids = [f"EAA-C-{number:03d}" for number in range(1, len(case_ids) + 1)]
    if case_ids != expected_case_ids:
        errors.append(
            "$.cases: IDs must be unique, contiguous, and sorted; expected "
            + ", ".join(expected_case_ids)
        )
    expected_source_ids = [f"SRC-{number:03d}" for number in range(1, len(source_ids) + 1)]
    if source_ids != expected_source_ids:
        errors.append(
            "$.sources: IDs must be unique, contiguous, and sorted; expected "
            + ", ".join(expected_source_ids)
        )
    expected_candidate_ids = [
        f"EAA-C{number:03d}" for number in range(1, len(candidate_ids) + 1)
    ]
    if candidate_ids != expected_candidate_ids:
        errors.append(
            "$.candidates: IDs must be unique, contiguous, and sorted; expected "
            + ", ".join(expected_candidate_ids)
        )

    version_path = ROOT / "VERSION"
    if check_repository_version and version_path.exists():
        version = version_path.read_text(encoding="utf-8").strip()
        if catalog.get("version") != version:
            errors.append(
                f"$.version: {catalog.get('version')!r} does not match VERSION {version!r}"
            )

    today = dt.date.today()
    for field_path, value in [("$.last_reviewed", catalog.get("last_reviewed"))] + [
        (f"$.techniques[{index}].last_reviewed", item.get("last_reviewed"))
        for index, item in enumerate(techniques)
        if isinstance(item, dict)
    ] + [
        (f"$.candidates[{index}].last_reviewed", item.get("last_reviewed"))
        for index, item in enumerate(candidates)
        if isinstance(item, dict)
    ]:
        if isinstance(value, str):
            try:
                if dt.date.fromisoformat(value) > today:
                    errors.append(f"{field_path}: date is in the future")
            except ValueError:
                pass  # Already reported by schema validation.

    for source_index, source in enumerate(sources):
        if not isinstance(source, dict):
            continue
        for field in ("published", "verified_on"):
            value = source.get(field)
            if not isinstance(value, str):
                continue
            try:
                if dt.date.fromisoformat(value) > today:
                    errors.append(f"$.sources[{source_index}].{field}: date is in the future")
            except ValueError:
                pass
        if (
            "official-documentation" in source.get("types", [])
            and "verified_on" not in source
        ):
            errors.append(
                f"$.sources[{source_index}].verified_on: required for mutable official documentation"
            )

    for case_index, case in enumerate(cases):
        if not isinstance(case, dict):
            continue
        start_value = case.get("date_start")
        end_value = case.get("date_end")
        start_date: dt.date | None = None
        end_date: dt.date | None = None
        try:
            if isinstance(start_value, str):
                start_date = dt.date.fromisoformat(start_value)
                if start_date > today:
                    errors.append(f"$.cases[{case_index}].date_start: date is in the future")
            if isinstance(end_value, str):
                end_date = dt.date.fromisoformat(end_value)
                if end_date > today:
                    errors.append(f"$.cases[{case_index}].date_end: date is in the future")
        except ValueError:
            pass
        if start_date is not None and end_date is not None and end_date < start_date:
            errors.append(f"$.cases[{case_index}].date_end: precedes date_start")

    valid_surface_ids = set(surface_ids)
    tactic_order = schema_enum(schema, "tactic")
    tactic_rank = {name: index for index, name in enumerate(tactic_order)}
    source_type_order = schema_enum(schema, "sourceType")
    source_type_rank = {name: index for index, name in enumerate(source_type_order)}
    confidence_order = schema_enum(schema, "confidence")
    confidence_rank = {name: index for index, name in enumerate(confidence_order)}
    surface_rank = {name: index for index, name in enumerate(surface_ids)}
    known_technique_ids = set(technique_ids)
    source_by_id = {
        item["id"]: item
        for item in sources
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    known_source_ids = set(source_by_id)
    technique_by_id = {
        item["id"]: item
        for item in techniques
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    relation_keys: set[tuple[str, str, str]] = set()
    normalized_source_urls: dict[str, str] = {}

    for source_index, source in enumerate(sources):
        if not isinstance(source, dict):
            continue
        path = f"$.sources[{source_index}]"
        types = source.get("types", [])
        if types != sorted(types, key=lambda value: source_type_rank.get(value, 999)):
            errors.append(f"{path}.types: source types must follow schema order")
        url = source.get("url")
        if isinstance(url, str):
            normalized = normalize_url(url)
            prior = normalized_source_urls.get(normalized)
            if prior is not None:
                errors.append(
                    f"{path}.url: duplicate normalized source URL also registered as {prior}"
                )
            normalized_source_urls[normalized] = source.get("id", path)

    observed_case_techniques: set[str] = set()
    used_source_ids: set[str] = {
        item.get("source_id")
        for technique in techniques
        if isinstance(technique, dict)
        for item in technique.get("evidence", [])
        if isinstance(item, dict) and isinstance(item.get("source_id"), str)
    }
    for case_index, case in enumerate(cases):
        if not isinstance(case, dict):
            continue
        path = f"$.cases[{case_index}]"
        case_source_refs = case.get("source_refs", [])
        case_source_rank = {
            source_id: index for index, source_id in enumerate(case_source_refs)
        }
        for source_id in case_source_refs:
            if source_id not in known_source_ids:
                errors.append(f"{path}.source_refs: unknown source {source_id!r}")
        procedures = case.get("procedures", [])
        steps = [
            item.get("step") for item in procedures if isinstance(item, dict)
        ]
        expected_steps = list(range(1, len(procedures) + 1))
        if steps != expected_steps:
            errors.append(f"{path}.procedures: step numbers must be contiguous and ordered")
        used_source_refs: set[str] = set()
        for procedure_index, procedure in enumerate(procedures):
            if not isinstance(procedure, dict):
                continue
            procedure_path = f"{path}.procedures[{procedure_index}]"
            technique_id = procedure.get("technique_id")
            if technique_id not in known_technique_ids:
                errors.append(
                    f"{procedure_path}.technique_id: unknown technique {technique_id!r}"
                )
                continue
            procedure_refs = procedure.get("source_refs", [])
            if procedure_refs != sorted(
                procedure_refs, key=lambda value: case_source_rank.get(value, 999)
            ):
                errors.append(
                    f"{procedure_path}.source_refs: refs must follow case source order"
                )
            technique_evidence_by_source: dict[str, set[str]] = {}
            technique_evidence_confidence: dict[tuple[str, str], str] = {}
            for item in technique_by_id[technique_id].get("evidence", []):
                if not isinstance(item, dict):
                    continue
                source_id = item.get("source_id")
                support = item.get("support")
                if isinstance(source_id, str) and isinstance(support, str):
                    technique_evidence_by_source.setdefault(source_id, set()).add(support)
                    confidence = item.get("confidence")
                    if isinstance(confidence, str):
                        technique_evidence_confidence[(source_id, support)] = confidence
            required_support = OUTCOME_SUPPORT.get(procedure.get("outcome"))
            matching_confidences: list[str] = []
            for source_id in procedure_refs:
                used_source_refs.add(source_id)
                used_source_ids.add(source_id)
                if source_id not in case_source_rank:
                    errors.append(
                        f"{procedure_path}.source_refs: {source_id!r} is not in case source_refs"
                    )
                if source_id not in known_source_ids:
                    errors.append(
                        f"{procedure_path}.source_refs: unknown source {source_id!r}"
                    )
                if source_id not in technique_evidence_by_source:
                    errors.append(
                        f"{procedure_path}.source_refs: source {source_id!r} is not evidence "
                        f"for {technique_id}"
                    )
                elif (
                    required_support is not None
                    and required_support not in technique_evidence_by_source[source_id]
                ):
                    errors.append(
                        f"{procedure_path}.source_refs: source {source_id!r} lacks required "
                        f"{required_support!r} evidence for {technique_id} outcome "
                        f"{procedure.get('outcome')!r}"
                    )
                elif required_support is not None:
                    evidence_confidence = technique_evidence_confidence.get(
                        (source_id, required_support)
                    )
                    if evidence_confidence in confidence_rank:
                        matching_confidences.append(evidence_confidence)
            procedure_confidence = procedure.get("confidence")
            if (
                matching_confidences
                and procedure_confidence in confidence_rank
            ):
                strongest_confidence = max(
                    matching_confidences,
                    key=lambda value: confidence_rank[value],
                )
                if (
                    confidence_rank[procedure_confidence]
                    > confidence_rank[strongest_confidence]
                ):
                    errors.append(
                        f"{procedure_path}.confidence: {procedure_confidence!r} exceeds "
                        f"strongest matching evidence confidence "
                        f"{strongest_confidence!r} for {required_support!r}"
                    )
            qualifying_incident_source = any(
                "incident-report" in source_by_id.get(source_id, {}).get("types", [])
                and required_support
                in technique_evidence_by_source.get(source_id, set())
                for source_id in procedure_refs
            )
            if (
                "observed-incident" in case.get("contexts", [])
                and procedure.get("outcome")
                in {"planted", "executed", "impact-confirmed"}
                and qualifying_incident_source
            ):
                observed_case_techniques.add(technique_id)
        if used_source_refs != set(case_source_refs):
            missing = sorted(set(case_source_refs) - used_source_refs)
            extra = sorted(used_source_refs - set(case_source_refs))
            if missing:
                errors.append(f"{path}.source_refs: unused case source(s): {', '.join(missing)}")
            if extra:
                errors.append(f"{path}.source_refs: unlisted step source(s): {', '.join(extra)}")

    unused_source_ids = sorted(known_source_ids - used_source_ids)
    if unused_source_ids:
        errors.append(
            "$.sources: unreferenced canonical source(s): " + ", ".join(unused_source_ids)
        )

    for index, technique in enumerate(techniques):
        if not isinstance(technique, dict):
            continue
        path = f"$.techniques[{index}]"
        technique_id = technique.get("id", "")
        primary = technique.get("primary_surface")
        secondary = technique.get("secondary_surfaces", [])
        if primary not in valid_surface_ids:
            errors.append(f"{path}.primary_surface: unknown surface {primary!r}")
        for item in secondary:
            if item not in valid_surface_ids:
                errors.append(f"{path}.secondary_surfaces: unknown surface {item!r}")
        if primary in secondary:
            errors.append(f"{path}.secondary_surfaces: includes the primary surface")
        if secondary != sorted(secondary, key=lambda value: surface_rank.get(value, 999)):
            errors.append(
                f"{path}.secondary_surfaces: surfaces must follow catalog surface order"
            )
        if technique.get("tactics", []) != sorted(
            technique.get("tactics", []), key=lambda value: tactic_rank.get(value, 999)
        ):
            errors.append(f"{path}.tactics: tactics must follow the schema's canonical order")

        evidence = technique.get("evidence", [])
        supported_claims = {
            item.get("support")
            for item in evidence
            if isinstance(item, dict)
            and isinstance(item.get("support"), str)
        }
        implementation_claims = supported_claims - {"surface-documented"}
        qualifying_implementation_source = any(
            bool(
                {
                    "primary-artifact",
                    "reproducible-research",
                    "malicious-artifact",
                    "incident-report",
                }
                & set(source_by_id.get(item.get("source_id"), {}).get("types", []))
            )
            and item.get("support") in implementation_claims
            for item in evidence
            if isinstance(item, dict)
        )
        if technique_id in observed_case_techniques:
            expected_maturity = "observed"
        elif qualifying_implementation_source:
            expected_maturity = "demonstrated"
        else:
            expected_maturity = "feasible"
            if implementation_claims:
                errors.append(
                    f"{path}.evidence: implementation claims require a primary artifact, "
                    "reproducible research, malicious artifact, or incident report"
                )
        if technique.get("maturity") != expected_maturity:
            errors.append(
                f"{path}.maturity: expected {expected_maturity!r} from the cited evidence; "
                f"got {technique.get('maturity')!r}"
            )
        for evidence_index, item in enumerate(evidence):
            if not isinstance(item, dict):
                continue
            item_path = f"{path}.evidence[{evidence_index}]"
            source_id = item.get("source_id")
            if source_id not in known_source_ids:
                errors.append(f"{item_path}.source_id: unknown source {source_id!r}")
        evidence_pairs = [
            (item.get("source_id"), item.get("support"))
            for item in evidence
            if isinstance(item, dict)
        ]
        repeated_pairs = duplicates(
            f"{source_id}:{support}" for source_id, support in evidence_pairs
        )
        if repeated_pairs:
            errors.append(
                f"{path}.evidence: duplicate source/support assertion(s): "
                + ", ".join(sorted(repeated_pairs))
            )

        for relation_index, relation in enumerate(technique.get("relationships", [])):
            if not isinstance(relation, dict):
                continue
            target = relation.get("target")
            relation_type = relation.get("type")
            relation_path = f"{path}.relationships[{relation_index}]"
            if target == technique_id:
                errors.append(f"{relation_path}.target: self-reference is not allowed")
            if target not in known_technique_ids:
                errors.append(f"{relation_path}.target: unknown technique {target!r}")
            key = (technique_id, relation_type, target)
            if key in relation_keys:
                errors.append(f"{relation_path}: duplicate relationship")
            relation_keys.add(key)
        relationships = technique.get("relationships", [])
        if relationships != sorted(
            relationships,
            key=lambda item: (
                item.get("type", "") if isinstance(item, dict) else "",
                item.get("target", "") if isinstance(item, dict) else "",
            ),
        ):
            errors.append(f"{path}.relationships: relationships must be sorted by type and target")

    # `related-to` is the sole symmetric relationship type.
    for source, relation_type, target in sorted(relation_keys):
        if relation_type == "related-to" and (target, relation_type, source) not in relation_keys:
            errors.append(
                f"relationship {source} related-to {target} is missing reciprocal relationship"
            )

    for index, candidate in enumerate(candidates):
        if not isinstance(candidate, dict):
            continue
        for target in candidate.get("related_techniques", []):
            if target not in known_technique_ids:
                errors.append(
                    f"$.candidates[{index}].related_techniques: unknown technique {target!r}"
                )

    return errors


TECHNIQUE_HEADING = re.compile(r"^##\s+(EAA-[0-9]{3})\s+[—-]\s+(.+?)\s*$", re.MULTILINE)
CANDIDATE_HEADING = re.compile(r"^##\s+(EAA-C[0-9]{3})\s+[—-]\s+(.+?)\s*$", re.MULTILINE)
CASE_HEADING = re.compile(r"^##\s+(EAA-C-[0-9]{3})\s+[—-]\s+(.+?)\s*$", re.MULTILINE)
ID_REFERENCE = re.compile(r"\bEAA-(?:C[0-9]{3}|[0-9]{3})\b")
MARKDOWN_URL = re.compile(r"\]\((https://[^)\s]+)\)")
BARE_URL = re.compile(r"https://[^\s)>]+")
LOCAL_LINK = re.compile(r"\]\((?!https?://|mailto:)([^)\s]+)(?:\s+[^)]*)?\)")
CASE_SOURCE_LINE = re.compile(
    r"^-\s+`S([1-9][0-9]*)`\s+—\s+\[[^]]+\]\((https://[^)\s]+)\)\s*$",
    re.MULTILINE,
)


def section_map(text: str, heading_pattern: re.Pattern[str]) -> dict[str, tuple[str, str]]:
    matches = list(heading_pattern.finditer(text))
    sections: dict[str, tuple[str, str]] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections[match.group(1)] = (match.group(2).strip(), text[match.end() : end])
    return sections


def metadata(section: str, field: str) -> str | None:
    match = re.search(
        rf"^(?:-\s+)?\*\*{re.escape(field)}:\*\*\s*(.+?)\s*$",
        section,
        re.MULTILINE | re.IGNORECASE,
    )
    if match is None:
        return None
    return match.group(1).strip().rstrip("  ")


def markdown_label(value: str) -> str:
    value = value.strip().strip("`")
    match = re.fullmatch(r"\[([^]]+)]\([^)]+\)", value)
    return match.group(1).strip() if match else value


def parse_table(text: str, required_columns: set[str]) -> tuple[list[str], list[list[str]]] | None:
    lines = text.splitlines()
    for index in range(len(lines) - 1):
        if not lines[index].lstrip().startswith("|"):
            continue
        headers = [cell.strip() for cell in lines[index].strip().strip("|").split("|")]
        separator = lines[index + 1].strip()
        if not re.fullmatch(r"\|?(?:\s*:?-+:?\s*\|)+\s*", separator + ("|" if not separator.endswith("|") else "")):
            continue
        if not required_columns.issubset(set(headers)):
            continue
        rows: list[list[str]] = []
        for row_line in lines[index + 2 :]:
            if not row_line.lstrip().startswith("|"):
                break
            cells = [cell.strip() for cell in row_line.strip().strip("|").split("|")]
            if len(cells) == len(headers):
                rows.append(cells)
        return headers, rows
    return None


def github_slug(heading: str) -> str:
    characters: list[str] = []
    for character in heading.strip().lower():
        if character == "-":
            characters.append(character)
        elif character.isspace():
            characters.append("-")
        elif unicodedata.category(character).startswith("P"):
            continue
        else:
            characters.append(character)
    return "".join(characters)


def markdown_anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    counts: dict[str, int] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if match is None:
            continue
        base = github_slug(match.group(1))
        count = counts.get(base, 0)
        anchor = base if count == 0 else f"{base}-{count}"
        counts[base] = count + 1
        anchors.add(anchor)
    return anchors


def validate_local_links(markdown_paths: list[Path]) -> list[str]:
    errors: list[str] = []
    anchor_cache: dict[Path, set[str]] = {}
    for source in markdown_paths:
        if not source.exists():
            continue
        text = source.read_text(encoding="utf-8")
        for raw_target in LOCAL_LINK.findall(text):
            target_text = unquote(raw_target)
            file_part, separator, fragment = target_text.partition("#")
            target = (source.parent / file_part).resolve() if file_part else source.resolve()
            try:
                target.relative_to(ROOT)
            except ValueError:
                errors.append(
                    f"{source.relative_to(ROOT)}: local link escapes the repository: {raw_target}"
                )
                continue
            if not target.exists():
                errors.append(
                    f"{source.relative_to(ROOT)}: broken local link target: {raw_target}"
                )
                continue
            if separator and fragment and target.suffix.lower() == ".md":
                anchors = anchor_cache.setdefault(target, markdown_anchors(target))
                if fragment not in anchors:
                    errors.append(
                        f"{source.relative_to(ROOT)}: unknown Markdown anchor in {raw_target}"
                    )
    return errors


def normalize_whitespace(value: str) -> str:
    return " ".join(value.split())


def display_case_date(case: dict[str, Any]) -> str:
    value = case["date_start"]
    if case.get("date_end"):
        value += f" to {case['date_end']}"
    if case["date_basis"] in {"reported", "published"}:
        value = f"{case['date_basis']} {value}"
    return value


def validate_markdown(catalog: dict[str, Any], schema: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    technique_records = {item["id"]: item for item in catalog["techniques"]}
    case_records = {item["id"]: item for item in catalog["cases"]}
    candidate_records = {item["id"]: item for item in catalog["candidates"]}
    source_records = {item["id"]: item for item in catalog["sources"]}
    surface_names = {item["id"]: item["name"] for item in catalog["surfaces"]}
    known_ids = set(technique_records) | set(candidate_records)

    markdown_paths = sorted(
        set(ROOT.glob("*.md")) | {ROOT / "techniques" / "index.md"}
    )
    for path in markdown_paths:
        if not path.exists():
            errors.append(f"{path.relative_to(ROOT)}: required documentation file is missing")
            continue
        text = path.read_text(encoding="utf-8")
        unknown = sorted(set(ID_REFERENCE.findall(text)) - known_ids)
        if unknown:
            errors.append(
                f"{path.relative_to(ROOT)}: unknown catalog ID reference(s): {', '.join(unknown)}"
            )
    errors.extend(validate_local_links(markdown_paths))

    technique_path = ROOT / "techniques" / "index.md"
    if technique_path.exists():
        text = technique_path.read_text(encoding="utf-8")
        sections = section_map(text, TECHNIQUE_HEADING)
        if list(sections) != list(technique_records):
            errors.append(
                "techniques/index.md: technique headings must exactly match catalog ID order"
            )
        for technique_id, record in technique_records.items():
            if technique_id not in sections:
                continue
            documented_name, body = sections[technique_id]
            if documented_name != record["name"]:
                errors.append(
                    f"techniques/index.md: {technique_id} name {documented_name!r} does not "
                    f"match catalog {record['name']!r}"
                )
            documented_surface = metadata(body, "Primary surface") or metadata(body, "Surface")
            expected_surface = surface_names[record["primary_surface"]]
            if documented_surface != expected_surface:
                errors.append(
                    f"techniques/index.md: {technique_id} primary surface "
                    f"{documented_surface!r} does not match catalog {expected_surface!r}"
                )
            documented_tactics = metadata(body, "Tactics") or metadata(body, "Tactic")
            if documented_tactics is None:
                errors.append(f"techniques/index.md: {technique_id} is missing **Tactics:**")
            else:
                parsed_tactics = [item.strip() for item in documented_tactics.split(",")]
                if parsed_tactics != record["tactics"]:
                    errors.append(
                        f"techniques/index.md: {technique_id} tactics {parsed_tactics!r} do not "
                        f"match catalog {record['tactics']!r}"
                    )
            documented_maturity = metadata(body, "Maturity")
            if documented_maturity != record["maturity"]:
                errors.append(
                    f"techniques/index.md: {technique_id} maturity {documented_maturity!r} does "
                    f"not match catalog {record['maturity']!r}"
                )
            documented_source_types = metadata(body, "Evidence sources")
            if documented_source_types is None:
                errors.append(
                    f"techniques/index.md: {technique_id} is missing **Evidence sources:**"
                )
            else:
                parsed_source_types = [
                    item.strip() for item in documented_source_types.split(",")
                ]
                catalog_source_types = {
                    source_type
                    for item in record["evidence"]
                    for source_type in source_records[item["source_id"]]["types"]
                }
                if set(parsed_source_types) != catalog_source_types:
                    errors.append(
                        f"techniques/index.md: {technique_id} evidence source categories "
                        f"{parsed_source_types!r} do not match catalog "
                        f"{sorted(catalog_source_types)!r}"
                    )
            documented_related = metadata(body, "Related")
            expected_related = [
                item["target"]
                for item in record["relationships"]
                if item["type"] == "related-to"
            ]
            parsed_related = (
                [item.strip() for item in documented_related.split(",")]
                if documented_related
                else []
            )
            if parsed_related != expected_related:
                errors.append(
                    f"techniques/index.md: {technique_id} related IDs {parsed_related!r} do not "
                    f"match catalog {expected_related!r}"
                )
            section_urls = {normalize_url(url) for url in MARKDOWN_URL.findall(body)}
            evidence_urls = {
                normalize_url(source_records[item["source_id"]]["url"])
                for item in record["evidence"]
            }
            if section_urls != evidence_urls:
                missing = sorted(evidence_urls - section_urls)
                extra = sorted(section_urls - evidence_urls)
                if missing:
                    errors.append(
                        f"techniques/index.md: {technique_id} omits catalog source URL(s): "
                        + ", ".join(missing)
                    )
                if extra:
                    errors.append(
                        f"data/catalog.json: {technique_id} omits documented source URL(s): "
                        + ", ".join(extra)
                    )

    candidate_path = ROOT / "candidates.md"
    if candidate_path.exists():
        sections = section_map(candidate_path.read_text(encoding="utf-8"), CANDIDATE_HEADING)
        if list(sections) != list(candidate_records):
            errors.append("candidates.md: candidate headings must exactly match catalog ID order")
        for candidate_id, record in candidate_records.items():
            if candidate_id in sections and sections[candidate_id][0] != record["name"]:
                errors.append(
                    f"candidates.md: {candidate_id} name {sections[candidate_id][0]!r} does not "
                    f"match catalog {record['name']!r}"
                )

    readme_path = ROOT / "README.md"
    if readme_path.exists():
        table = parse_table(readme_path.read_text(encoding="utf-8"), {"ID", "Technique"})
        if table is None:
            errors.append("README.md: could not find the technique summary table")
        else:
            headers, rows = table
            column = {name: index for index, name in enumerate(headers)}
            readme_ids = [markdown_label(row[column["ID"]]) for row in rows]
            if readme_ids != list(technique_records):
                errors.append("README.md: technique table IDs/order do not match catalog")
            for row in rows:
                technique_id = markdown_label(row[column["ID"]])
                if technique_id not in technique_records:
                    continue
                record = technique_records[technique_id]
                if markdown_label(row[column["Technique"]]) != record["name"]:
                    errors.append(f"README.md: {technique_id} technique name does not match catalog")
                surface_column = "Primary surface" if "Primary surface" in column else "Surface"
                if surface_column in column:
                    expected = surface_names[record["primary_surface"]]
                    if markdown_label(row[column[surface_column]]) != expected:
                        errors.append(f"README.md: {technique_id} surface does not match catalog")
                if "Maturity" in column and markdown_label(row[column["Maturity"]]) != record["maturity"]:
                    errors.append(f"README.md: {technique_id} maturity does not match catalog")
        version_match = re.search(
            r"Current catalog version:\s*\*\*([^*]+)\*\*", readme_path.read_text(encoding="utf-8")
        )
        if version_match is None or version_match.group(1) != catalog["version"]:
            errors.append("README.md: current catalog version does not match data/catalog.json")

    surface_path = ROOT / "surfaces.md"
    if surface_path.exists():
        table = parse_table(
            surface_path.read_text(encoding="utf-8"), {"Surface", "Techniques"}
        )
        if table is None:
            errors.append("surfaces.md: could not find the surface mapping table")
        else:
            headers, rows = table
            column = {name: index for index, name in enumerate(headers)}
            documented_surfaces = [markdown_label(row[column["Surface"]]) for row in rows]
            if documented_surfaces != list(surface_names.values()):
                errors.append("surfaces.md: surface names/order do not match catalog")
            for row in rows:
                surface_name = markdown_label(row[column["Surface"]])
                surface_id = next(
                    (key for key, value in surface_names.items() if value == surface_name), None
                )
                if surface_id is None:
                    continue
                documented_ids = ID_REFERENCE.findall(row[column["Techniques"]])
                expected_ids = [
                    record["id"]
                    for record in catalog["techniques"]
                    if record["primary_surface"] == surface_id
                ]
                if documented_ids != expected_ids:
                    errors.append(
                        f"surfaces.md: {surface_name} technique mapping does not match catalog"
                    )
        secondary_table = parse_table(
            surface_path.read_text(encoding="utf-8"),
            {"Technique", "Secondary surfaces"},
        )
        if secondary_table is None:
            errors.append("surfaces.md: could not find the secondary-surface table")
        else:
            headers, rows = secondary_table
            column = {name: index for index, name in enumerate(headers)}
            documented_ids = [
                markdown_label(row[column["Technique"]]) for row in rows
            ]
            expected_records = [
                record for record in catalog["techniques"] if record["secondary_surfaces"]
            ]
            if documented_ids != [record["id"] for record in expected_records]:
                errors.append(
                    "surfaces.md: secondary-surface rows/order do not match catalog"
                )
            for row in rows:
                technique_id = markdown_label(row[column["Technique"]])
                if technique_id not in technique_records:
                    continue
                documented_names = [
                    value.strip()
                    for value in row[column["Secondary surfaces"]].split(";")
                    if value.strip()
                ]
                expected_names = [
                    surface_names[surface_id]
                    for surface_id in technique_records[technique_id]["secondary_surfaces"]
                ]
                if documented_names != expected_names:
                    errors.append(
                        f"surfaces.md: {technique_id} secondary surfaces do not match catalog"
                    )

    tactic_path = ROOT / "tactics.md"
    if tactic_path.exists():
        table = parse_table(tactic_path.read_text(encoding="utf-8"), {"Tactic", "Techniques"})
        if table is None:
            errors.append("tactics.md: could not find the tactic mapping table")
        else:
            headers, rows = table
            column = {name: index for index, name in enumerate(headers)}
            expected_tactics = schema_enum(schema, "tactic")
            documented_tactics = [markdown_label(row[column["Tactic"]]) for row in rows]
            if documented_tactics != expected_tactics:
                errors.append("tactics.md: tactic names/order do not match catalog schema")
            for row in rows:
                tactic = markdown_label(row[column["Tactic"]])
                if tactic not in expected_tactics:
                    continue
                documented_ids = ID_REFERENCE.findall(row[column["Techniques"]])
                expected_ids = [
                    record["id"]
                    for record in catalog["techniques"]
                    if tactic in record["tactics"]
                ]
                if documented_ids != expected_ids:
                    errors.append(f"tactics.md: {tactic} technique mapping does not match catalog")

    cases_path = ROOT / "cases.md"
    if cases_path.exists():
        case_text = cases_path.read_text(encoding="utf-8")
        case_matches = list(CASE_HEADING.finditer(case_text))
        documented_case_ids = [match.group(1) for match in case_matches]
        if documented_case_ids != list(case_records):
            errors.append("cases.md: case headings/order do not match catalog")
        case_sections = section_map(case_text, CASE_HEADING)
        for case_id, record in case_records.items():
            if case_id not in case_sections:
                continue
            documented_name, body = case_sections[case_id]
            if documented_name != record["name"]:
                errors.append(
                    f"cases.md: {case_id} name {documented_name!r} does not match catalog "
                    f"{record['name']!r}"
                )
            if metadata(body, "Type") != record["type"]:
                errors.append(f"cases.md: {case_id} type does not match catalog")
            if metadata(body, "Date") != display_case_date(record):
                errors.append(f"cases.md: {case_id} date does not match catalog")
            activation_notes = metadata(body, "Activation notes")
            if normalize_whitespace(activation_notes or "") != normalize_whitespace(
                record["activation_notes"]
            ):
                errors.append(f"cases.md: {case_id} activation notes do not match catalog")

            table = parse_table(
                body,
                {"Step", "Technique", "Outcome", "Confidence", "Claim", "Sources"},
            )
            if table is None:
                errors.append(f"cases.md: {case_id} has no canonical procedure table")
            else:
                headers, rows = table
                column = {name: index for index, name in enumerate(headers)}
                if len(rows) != len(record["procedures"]):
                    errors.append(
                        f"cases.md: {case_id} procedure count does not match catalog"
                    )
                local_source_ids = {
                    source_id: f"S{index}"
                    for index, source_id in enumerate(record["source_refs"], start=1)
                }
                for row, procedure in zip(rows, record["procedures"]):
                    step = str(procedure["step"])
                    if row[column["Step"]] != step:
                        errors.append(f"cases.md: {case_id} step {step} number mismatch")
                    if markdown_label(row[column["Technique"]]) != procedure["technique_id"]:
                        errors.append(f"cases.md: {case_id} step {step} technique mismatch")
                    if row[column["Outcome"]] != procedure["outcome"]:
                        errors.append(f"cases.md: {case_id} step {step} outcome mismatch")
                    if row[column["Confidence"]] != procedure["confidence"]:
                        errors.append(f"cases.md: {case_id} step {step} confidence mismatch")
                    if normalize_whitespace(row[column["Claim"]]) != normalize_whitespace(
                        procedure["claim"]
                    ):
                        errors.append(f"cases.md: {case_id} step {step} claim mismatch")
                    documented_refs = re.findall(
                        r"\bS[1-9][0-9]*\b", row[column["Sources"]]
                    )
                    expected_refs = [
                        local_source_ids[source_id]
                        for source_id in procedure["source_refs"]
                    ]
                    if documented_refs != expected_refs:
                        errors.append(f"cases.md: {case_id} step {step} source mismatch")

            documented_sources = CASE_SOURCE_LINE.findall(body)
            expected_labels = [
                str(index) for index in range(1, len(record["source_refs"]) + 1)
            ]
            if [label for label, _ in documented_sources] != expected_labels:
                errors.append(f"cases.md: {case_id} source labels/order do not match catalog")
            for (label, url), source_id in zip(
                documented_sources, record["source_refs"]
            ):
                if normalize_url(url) != normalize_url(source_records[source_id]["url"]):
                    errors.append(
                        f"cases.md: {case_id} S{label} URL does not match {source_id}"
                    )

    sources_path = ROOT / "sources.md"
    if sources_path.exists():
        indexed_url_list = [
            normalize_url(url.rstrip(".,;"))
            for url in BARE_URL.findall(sources_path.read_text(encoding="utf-8"))
        ]
        indexed_urls = set(indexed_url_list)
        registry_urls = {
            normalize_url(source["url"]) for source in source_records.values()
        }
        duplicate_urls = sorted(
            url for url, count in Counter(indexed_url_list).items() if count > 1
        )
        missing = sorted(registry_urls - indexed_urls)
        extra = sorted(indexed_urls - registry_urls)
        if duplicate_urls:
            errors.append(
                "sources.md: repeats canonical registry URL(s): "
                + ", ".join(duplicate_urls)
            )
        if missing:
            errors.append(
                "sources.md: omits canonical registry URL(s): " + ", ".join(missing)
            )
        if extra:
            errors.append(
                "sources.md: contains URL(s) absent from canonical registry: "
                + ", ".join(extra)
            )
        for source_doc in (technique_path, cases_path):
            if not source_doc.exists():
                continue
            for url in MARKDOWN_URL.findall(source_doc.read_text(encoding="utf-8")):
                if normalize_url(url) not in registry_urls:
                    errors.append(
                        f"{source_doc.relative_to(ROOT)}: URL is absent from source registry: {url}"
                    )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument(
        "--skip-docs",
        action="store_true",
        help="validate only schema and catalog semantics (useful for external catalogs)",
    )
    args = parser.parse_args()

    catalog = load_json(args.catalog)
    schema = load_json(args.schema)
    schema_errors = validate_against_schema(catalog, schema, schema)
    errors = list(schema_errors)
    if isinstance(catalog, dict) and isinstance(schema, dict) and not schema_errors:
        is_repository_catalog = args.catalog.resolve() == DEFAULT_CATALOG.resolve()
        errors.extend(
            validate_catalog_semantics(
                catalog,
                schema,
                check_repository_version=is_repository_catalog,
            )
        )
        if not args.skip_docs and is_repository_catalog:
            errors.extend(validate_markdown(catalog, schema))

    if errors:
        print(f"validation failed with {len(errors)} error(s):", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(
        f"ok: schema {catalog['schema_version']}, {len(catalog['sources'])} sources, "
        f"{len(catalog['techniques'])} techniques, {len(catalog['cases'])} cases, "
        f"{len(catalog['candidates'])} candidates"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
