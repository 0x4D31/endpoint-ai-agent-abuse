# Changelog

## 0.2.1

Jscrambler supply-chain incident update.

- Added the Jscrambler npm compromise as a procedure-level case for agent-environment discovery and agent-state collection.
- Clarified that discovery can locate agent assets for immediate collection, not only select a later abuse path.
- Extended collection and reconnaissance hunts to cover cross-product reads of agent and MCP configuration.
- Recorded the still-unresolved affected-version discrepancy between Socket's analysis and Jscrambler's ongoing advisory.

## 0.2.0

Evidence and reproducibility hardening.

- Separated technique maturity, evidence-source type, case outcome, and confidence.
- Added tactics as an independent axis and normalized the six primary endpoint surfaces.
- Preserved EAA-001 through EAA-016 while correcting names, mappings, activation gates, and version-sensitive claims.
- Added EAA-017 for agent-native evidence tampering, anchored in a public forensic investigation.
- Added stable case IDs, distinguished artifact presence, planting, attempts, execution, and confirmed impact, and enforced exact case-outcome-to-evidence support.
- Enforced that case-step confidence cannot exceed the strongest exact evidence assertion it cites.
- Added machine-checked technique-to-case projections and exact vendor-advisory version ranges for the historical Claude Code project-configuration cases.
- Added current vendor documentation, advisories, incident reporting, and controlled research.
- Added official Claude Code, Codex, and Gemini CLI anchors for transcript retention, hooks, MCP trust, provider routing, profile roots, telemetry, and native project-data purge.
- Expanded hunting hypotheses with required telemetry, limitations, and cross-plane forensic checks.
- Added a JSON Schema, typed relationships, source-support metadata, stronger validation, and CI.
- Added contribution requirements for technique, case, and source changes.

## 0.1.0

Initial public-ready catalog seed.

- Added the human-readable technique catalog at `techniques/index.md`.
- Added six endpoint-agent surfaces in `surfaces.md`.
- Added cases, hunting notes, candidates, evidence rules, and focused source index.
- Added `data/catalog.json` as a secondary machine-readable artifact.
