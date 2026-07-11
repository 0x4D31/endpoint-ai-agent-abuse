# Contributing

EAA favors narrow, falsifiable entries over broad risk statements. Contributions should make it possible for another researcher to verify the mechanism and for a defender to understand what evidence would remain.

Read [`evidence.md`](evidence.md) before proposing a technique or case.

## Technique changes

A technique should describe one attacker action at a stable level of abstraction. Keep these concepts separate:

- **Tactic:** why the adversary acts, such as Discovery, Persistence, Collection, or Defense Evasion.
- **Technique:** how the objective is achieved, such as writing a lifecycle hook.
- **Procedure:** the product-, version-, and case-specific implementation.
- **Campaign property:** repetition or targeting patterns across victims, organizations, regions, or campaign waves.
- **Activation condition:** a trust decision, approval, reload, restart, environment value, or other prerequisite.

Include:

- a concise definition and abuse path;
- primary surface and tactics;
- prerequisites and activation conditions;
- technique maturity, evidence source types, and confidence for each evidence-to-claim assertion;
- product/version/OS scope supported by the sources;
- hunting ideas with false-positive context;
- direct sources for every material product or incident claim.

Do not generalize behavior from one product to all local agents. If support has only been verified for one product or version, say so.

`Highlights` is an optional editorial summary. `Case mappings` is the canonical Markdown projection: list every structured case that maps the technique, once, in catalog order; use `none` when there is no mapped case. The validator derives this list from case procedures and rejects missing, extra, duplicate, or reordered mappings.

## Case changes

Give each case a stable `EAA-C-NNN` identifier. Map ordered procedure steps, not just the case as a whole.

Use this shape:

```markdown
## EAA-C-NNN — Name

**Type:** incident | campaign | malicious artifact | research | vendor advisory
**Date:** YYYY-MM-DD | YYYY-MM-DD to YYYY-MM-DD | reported YYYY-MM-DD | published YYYY-MM-DD

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-NNN | present | high | One source-supported fact. | S1 |

**Activation notes:** Product/version trust or approval conditions.

**Sources:**

- `S1` — [Direct source](https://example.com/direct-source)
```

Each procedure row must cite one or more direct links or stable source labels resolved immediately below that case. If a report does not confirm execution or impact, use `present`, `planted`, or `attempted` and say what remains unknown.

For every source cited by a procedure row, add the exact matching technique-evidence assertion in `data/catalog.json`: `present` → `artifact-present`, `planted` → `procedure-planted`, `attempted` → `execution-attempted`, `executed` → `execution-confirmed`, and `impact-confirmed` → `impact-confirmed`. Merely listing the source elsewhere in the technique is not enough.

When an affected or fixed version range comes from a different source than the procedure outcome, record it in `scope.version_source_refs` and project it through a `Version sources` table column. Version sources must carry `version-range-documented` evidence for the technique and must not be presented as execution or impact evidence.

Confidence is claim-scoped. Assign it to each evidence item in `data/catalog.json` and to each case step; do not assign one confidence value to an entire technique, report, or campaign. A source can support artifact presence at high confidence while supporting activation only at medium or low confidence. A case step cannot claim greater confidence than the strongest exact source/support assertion it cites.

## Source quality

Prefer sources in this order:

1. vendor advisories, product documentation, public code, and primary artifacts;
2. incident investigators and reproducible original research;
3. high-quality secondary analysis.

Classify the source that the URL actually resolves to, independently of the claim it supports. For example, a vendor security advisory is a `primary-artifact`; an investigator's campaign report is an `incident-report`; and a blog post describing malicious code is not a `malicious-artifact` unless the link itself resolves to the inspectable code, configuration, package, or extension. Record artifact presence, planting, attempts, execution, and impact separately as support claims.

For mutable documentation, record when it was verified. For malicious artifacts, include versions, hashes, or immutable commits when the public source provides them. Before each release, re-check mutable documentation, CVE/advisory affected ranges, and date-stamped negative claims; refresh `verified_on` annotations where applicable.


## Catalog versioning

Version the published catalog once per release, not once per commit:

- **Patch:** new cases or procedures within the existing model, plus source, hunting, wording, or accuracy updates.
- **Minor:** taxonomy, surface, evidence semantics, maturity, naming, or backward-compatible schema changes.
- **Major:** incompatible schema or field-semantics changes, or other consumer-breaking changes.
- **No bump:** tests, CI, or contributor-documentation changes that do not alter published catalog content.

Keep `VERSION`, `README.md`, `data/catalog.json`, and `CHANGELOG.md` aligned, tag merged releases as `vX.Y.Z`, and never reuse or renumber stable IDs; deprecate them instead.

## Validation

Run:

```bash
python3 scripts/validate.py
```

The validator checks structured data, cross-file IDs and metadata, relationships, cases, source coverage, version consistency, and local links. A passing validator does not replace source review or product-version testing.
