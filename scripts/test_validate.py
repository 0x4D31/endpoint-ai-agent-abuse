#!/usr/bin/env python3
"""Regression tests for the dependency-free EAA validator."""

from __future__ import annotations

import copy
import unittest
from unittest import mock

import validate


class CatalogValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = validate.load_json(validate.DEFAULT_CATALOG)
        cls.schema = validate.load_json(validate.DEFAULT_SCHEMA)

    def semantic_errors(self, catalog: dict) -> list[str]:
        return validate.validate_catalog_semantics(
            catalog,
            self.schema,
            check_repository_version=False,
        )

    def test_repository_catalog_schema_and_docs(self) -> None:
        errors = validate.validate_against_schema(
            self.catalog,
            self.schema,
            self.schema,
        )
        errors.extend(self.semantic_errors(self.catalog))
        errors.extend(validate.validate_markdown(self.catalog, self.schema))
        self.assertEqual([], errors)

    def test_research_execution_is_demonstrated_not_observed(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        technique = next(item for item in catalog["techniques"] if item["id"] == "EAA-007")
        self.assertEqual("demonstrated", technique["maturity"])
        technique["maturity"] = "observed"
        self.assertTrue(
            any("expected 'demonstrated'" in error for error in self.semantic_errors(catalog))
        )

    def test_version_range_does_not_promote_technique_maturity(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        technique = next(item for item in catalog["techniques"] if item["id"] == "EAA-009")
        self.assertEqual("feasible", technique["maturity"])
        technique["evidence"].append(
            {
                "source_id": "SRC-040",
                "support": "version-range-documented",
                "confidence": "high",
            }
        )
        self.assertFalse(
            any(
                "techniques[8].maturity" in error
                for error in self.semantic_errors(catalog)
            )
        )

    def test_incident_case_with_confirmed_impact_is_observed(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        technique = next(item for item in catalog["techniques"] if item["id"] == "EAA-005")
        self.assertEqual("observed", technique["maturity"])
        technique["maturity"] = "demonstrated"
        self.assertTrue(
            any("expected 'observed'" in error for error in self.semantic_errors(catalog))
        )

    def test_observed_without_qualifying_case_is_rejected(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        case = next(item for item in catalog["cases"] if item["id"] == "EAA-C-008")
        step = next(
            item for item in case["procedures"] if item["technique_id"] == "EAA-005"
        )
        step["outcome"] = "attempted"
        self.assertTrue(
            any(
                "expected 'demonstrated'" in error
                and "techniques[4].maturity" in error
                for error in self.semantic_errors(catalog)
            )
        )

    def test_case_source_orphan_is_rejected(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        technique = next(item for item in catalog["techniques"] if item["id"] == "EAA-005")
        technique["evidence"] = [
            item for item in technique["evidence"] if item["source_id"] != "SRC-010"
        ]
        self.assertTrue(
            any(
                "source 'SRC-010' is not evidence for EAA-005" in error
                for error in self.semantic_errors(catalog)
            )
        )

    def test_case_outcome_requires_matching_evidence_support(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        technique = next(item for item in catalog["techniques"] if item["id"] == "EAA-012")
        technique["evidence"] = [
            item
            for item in technique["evidence"]
            if not (
                item["source_id"] == "SRC-028"
                and item["support"] == "impact-confirmed"
            )
        ]
        self.assertTrue(
            any(
                "source 'SRC-028' lacks required 'impact-confirmed' evidence"
                in error
                for error in self.semantic_errors(catalog)
            )
        )

    def test_case_confidence_cannot_exceed_matching_evidence(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        case = next(item for item in catalog["cases"] if item["id"] == "EAA-C-002")
        step = next(item for item in case["procedures"] if item["step"] == 3)
        self.assertEqual("medium", step["confidence"])
        step["confidence"] = "high"
        self.assertTrue(
            any(
                "exceeds strongest matching evidence confidence 'medium'"
                in error
                for error in self.semantic_errors(catalog)
            )
        )

    def test_case_version_source_requires_version_range_evidence(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        technique = next(item for item in catalog["techniques"] if item["id"] == "EAA-003")
        technique["evidence"] = [
            item
            for item in technique["evidence"]
            if item["source_id"] != "SRC-040"
        ]
        self.assertTrue(
            any(
                "scope.version_source_refs: source 'SRC-040' is not evidence for EAA-003"
                in error
                for error in self.semantic_errors(catalog)
            )
        )

    def test_official_documentation_requires_verified_on(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        source = next(item for item in catalog["sources"] if item["id"] == "SRC-012")
        del source["verified_on"]
        self.assertTrue(
            any(
                "verified_on: required for mutable official documentation or security "
                "advisory" in error
                for error in self.semantic_errors(catalog)
            )
        )

    def test_security_advisory_requires_verified_on(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        source = next(item for item in catalog["sources"] if item["id"] == "SRC-003")
        del source["verified_on"]
        self.assertTrue(
            any(
                "verified_on: required for mutable official documentation or security "
                "advisory" in error
                for error in self.semantic_errors(catalog)
            )
        )

    def test_duplicate_evidence_assertion_is_rejected(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        evidence = catalog["techniques"][0]["evidence"]
        evidence.append(copy.deepcopy(evidence[0]))
        self.assertTrue(
            any(
                "duplicate source/support assertion" in error
                for error in self.semantic_errors(catalog)
            )
        )

    def test_duplicate_normalized_source_url_is_rejected(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        duplicate = copy.deepcopy(catalog["sources"][0])
        duplicate["id"] = f"SRC-{len(catalog['sources']) + 1:03d}"
        duplicate["url"] += "/"
        duplicate["types"] = ["secondary-analysis"]
        catalog["sources"].append(duplicate)
        self.assertTrue(
            any(
                "duplicate normalized source URL" in error
                for error in self.semantic_errors(catalog)
            )
        )

    def test_duplicate_source_index_url_is_rejected(self) -> None:
        original_read_text = validate.Path.read_text
        duplicate_url = self.catalog["sources"][0]["url"]
        sources_path = validate.ROOT / "sources.md"

        def read_text(path: validate.Path, *args: object, **kwargs: object) -> str:
            text = original_read_text(path, *args, **kwargs)
            if path == sources_path:
                return text + f"\n- Duplicate source — {duplicate_url}\n"
            return text

        with mock.patch.object(validate.Path, "read_text", read_text):
            errors = validate.validate_markdown(self.catalog, self.schema)

        self.assertTrue(
            any(
                "sources.md: repeats canonical registry URL(s)" in error
                for error in errors
            )
        )

    def test_missing_technique_case_mapping_is_rejected(self) -> None:
        original_read_text = validate.Path.read_text
        technique_path = validate.ROOT / "techniques" / "index.md"

        def read_text(path: validate.Path, *args: object, **kwargs: object) -> str:
            text = original_read_text(path, *args, **kwargs)
            if path == technique_path:
                return text.replace(
                    "**Case mappings:** EAA-C-001, EAA-C-002",
                    "**Case mappings:** EAA-C-001",
                    1,
                )
            return text

        with mock.patch.object(validate.Path, "read_text", read_text):
            errors = validate.validate_markdown(self.catalog, self.schema)

        self.assertTrue(
            any(
                "EAA-001 case mappings ['EAA-C-001'] do not match catalog "
                "['EAA-C-001', 'EAA-C-002']" in error
                for error in errors
            )
        )

    def test_missing_case_version_source_projection_is_rejected(self) -> None:
        original_read_text = validate.Path.read_text
        cases_path = validate.ROOT / "cases.md"

        def read_text(path: validate.Path, *args: object, **kwargs: object) -> str:
            text = original_read_text(path, *args, **kwargs)
            if path == cases_path:
                return text.replace(
                    "| S1 | S2 |\n| 2 | EAA-006",
                    "| S1 |  |\n| 2 | EAA-006",
                    1,
                )
            return text

        with mock.patch.object(validate.Path, "read_text", read_text):
            errors = validate.validate_markdown(self.catalog, self.schema)

        self.assertTrue(
            any(
                "EAA-C-015 step 1 version source mismatch" in error
                for error in errors
            )
        )

    def test_unknown_relationship_target_is_rejected(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        catalog["techniques"][0]["relationships"][0]["target"] = "EAA-999"
        self.assertTrue(
            any("unknown technique 'EAA-999'" in error for error in self.semantic_errors(catalog))
        )

    def test_duplicate_technique_id_is_rejected(self) -> None:
        catalog = copy.deepcopy(self.catalog)
        catalog["techniques"][1]["id"] = catalog["techniques"][0]["id"]
        self.assertTrue(
            any("duplicate technique ID" in error for error in self.semantic_errors(catalog))
        )


if __name__ == "__main__":
    unittest.main()
