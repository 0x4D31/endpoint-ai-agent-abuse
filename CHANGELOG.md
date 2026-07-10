# Changelog

## 0.2.0

Evidence and reproducibility hardening.

- Separated technique maturity, evidence-source type, case outcome, and confidence.
- Added tactics as an independent axis and normalized the six primary endpoint surfaces.
- Preserved EAA-001 through EAA-016 while correcting names, mappings, activation gates, and version-sensitive claims.
- Added EAA-017 for agent-native evidence tampering, anchored in a public forensic investigation.
- Added stable case IDs, distinguished artifact presence, planting, attempts, execution, and confirmed impact, and enforced exact case-outcome-to-evidence support.
- Added current vendor documentation, advisories, incident reporting, and controlled research.
- Expanded hunting hypotheses with required telemetry, limitations, and cross-plane forensic checks.
- Added a JSON Schema, typed relationships, source-support metadata, stronger validation, and CI.
- Added contribution requirements for technique, case, and source changes.

## 0.1.0

Initial public-ready catalog seed.

- Added the human-readable technique catalog at `techniques/index.md`.
- Added six endpoint-agent surfaces in `surfaces.md`.
- Added cases, hunting notes, candidates, evidence rules, and focused source index.
- Added `data/catalog.json` as a secondary machine-readable artifact.
