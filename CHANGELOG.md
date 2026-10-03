# Changelog

## 0.5.0

Agent-tool implementation and case evidence update.

- Added a version-pinned comparison of selected mechanisms with MITRE ATLAS and primary-source case-selection decisions.
- Added EAA-021 for hidden side effects in executable agent-tool implementations, grounded in the Postmark MCP artifact.
- Added eight cases: Amazon Q extension payload, Postmark MCP, Claude Code GitHub Action, OpenClaw gateway takeover, AI ClickFix, Mitiga poisoned assessment, Orca skill updates, and Sentry Agentjacking.
- Promoted EAA-006 and EAA-010 to observed using the medium-confidence Mitiga incident assertions; preserved per-procedure qualifications.
- Clarified skill update versus cloud synchronization, rendered task context, runtime policy changes, and tool arguments versus actual service effects. EAA-013 remains feasible.
- Recorded Amazon Q and Postmark artifact presence separately from execution, limited OpenClaw to reported execution, and captured the reported Sentry test version.
- Retained schema 1.0.0.

## 0.4.0

- Added six cases: ChainDrop, trojanized skills.sh packages, Kiro MCP configuration rewriting, GitSpawn, dangling-reference takeover, and GhostSplice.
- Added EAA-019 for command execution through repository metadata interpreted by an agent’s automatic helpers.
- Added EAA-020 for takeover of package or domain references in unchanged agent-facing documentation.
- Added hunting guidance for Git helper execution, reference ownership changes, and instructions split across MCP messages.
- Recorded tested versions, activation conditions, and evidence limits for each case. Pinned the GhostSplice source revision.
- Clarified the introduction, evidence rules, and technique descriptions; corrected the distinction between skill installation and activation.

## 0.3.2

Blacklight implementation and hunting update.

- Added Blacklight v0.2.0 and its first-party research as implementation and controlled-execution evidence for existing EAA-005 and EAA-016.
- Added adversary-emulation guidance that separates metadata enumeration, selected artifact reads, operator-provided C2 transfer, and offline analysis.
- Preserved Blacklight's boundaries: no agent invocation, credential reuse, inherited-authority exercise, source agent-state modification, or evidence tampering.
- Added no new technique or case, and made no maturity, relationship, or schema change.

## 0.3.1

Computer History evidence and forensics update.

- Added official ChatGPT Computer History documentation to the existing persistent-memory, state-collection, evidence-tampering, and task-context techniques.
- Added IRFlow residual-evidence guidance for Computer History event counts, summaries, and Git recovery.
- Preserved the distinctions between App Group-isolated raw events and memories potentially accessible to same-user software, and between deletion leads and proof of tampering.
- Added no technique, case, maturity, or schema change.

## 0.3.0

Scope and task-context update.

- Added an explicit victim-side agent scope, hosted-runner boundary, and adjacent-case decisions.
- Added Task & Retrieved Context and EAA-018 for indirect instruction injection through task data or retrieved content.
- Broadened EAA-009 to name remote skill installation while keeping later cloud-hosted modification and sync in EAA-013.
- Added procedure-level cases for Amazon Q MCP auto-execution, SANDWORM_MODE, Claude Code persistent settings injection, ContextCrush, and GitLost.
- Preserved source disagreements and activation gates, including the Amazon Q workspace-trust discrepancy and unconfirmed SANDWORM_MODE agent activation.
- Corrected Jscrambler procedure scope to distinguish targeted agent products from carrier package versions.
- Clarified applicability, relationship, and scope-writing guidance for future contributions.

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
