# EAA and MITRE ATLAS

MITRE ATLAS is useful for finding relevant research and comparing mechanisms. Its scope is broader than EAA: an ATLAS case can concern a hosted assistant, a model, an AI supply chain, or an attacker operating an agent. EAA requires an affected agent or agent component that belongs to or operates for the victim; see [`scope.md`](scope.md).

The comparisons use the [ATLAS 2026.09 release](https://github.com/mitre-atlas/atlas-data/releases/tag/v2026.09), modified September 15, 2026, and its [versioned dataset at commit `3259f388`](https://github.com/mitre-atlas/atlas-data/blob/3259f388d19cbcca11bacf12a0ef97f4198f711b/dist/v6/ATLAS-2026.09.yaml). Reviewed October 3, 2026. The comparisons describe related mechanisms; they are not an official MITRE mapping. Case outcomes and applicability are documented in the linked EAA entries.

## Selected mechanism comparisons

These four comparisons identify specific overlaps useful to EAA. They are not a complete crosswalk.

| EAA mechanism | Relevant ATLAS entry | Relationship and limit |
|---|---|---|
| EAA-010: tool-definition poisoning or drift | [AML.T0110.000: Definition and Instructions](https://atlas.mitre.org/techniques/AML.T0110.000) | Closely related mechanism, subject to EAA's victim-side scope. Distinct from hidden implementation behavior and instructions in runtime results. |
| EAA-016: agent environment discovery | [AML.T0084: Discover AI Agent Configuration](https://atlas.mitre.org/techniques/AML.T0084), [AML.T0133: Discover AI Agent Runtime Capabilities](https://atlas.mitre.org/techniques/AML.T0133) | Related discovery actions. Reading static configuration does not prove a tool is available or permitted in a running session. |
| EAA-018: task-context instruction injection | [AML.T0051.001: Indirect](https://atlas.mitre.org/techniques/AML.T0051.001); [AML.T0110.002: Runtime Response](https://atlas.mitre.org/techniques/AML.T0110.002) for the tool-response subset | EAA requires a mechanism that can cause a local or delegated action. Ordinary issue, log, web, or rendered content is not necessarily a poisoned tool implementation; a trusted integration can transport attacker-controlled upstream data. |
| EAA-021: tool implementation poisoning | [AML.T0110.001: Implementation](https://atlas.mitre.org/techniques/AML.T0110.001) | Closely related mechanism. The executable tool can perform an undisclosed side effect during an ordinary invocation without persuading the model to request that effect. |

## Case decisions

These six ATLAS cases have corresponding EAA entries. Each EAA entry cites the primary research, artifacts, or vendor advisories that support its claims.

| ATLAS case | EAA case |
|---|---|
| [AML.CS0047: Amazon Q extension](https://atlas.mitre.org/studies/AML.CS0047) | [EAA-C-029](cases.md#eaa-c-029--amazon-q-vs-code-extension-destructive-agent-payload) |
| [AML.CS0053: Postmark MCP](https://atlas.mitre.org/studies/AML.CS0053) | [EAA-C-030](cases.md#eaa-c-030--postmark-mcp-implementation-backdoor) and EAA-021 |
| [AML.CS0067: Claude Code GitHub Action](https://atlas.mitre.org/studies/AML.CS0067) | [EAA-C-031](cases.md#eaa-c-031--claude-code-github-action-process-environment-disclosure) |
| [AML.CS0050: OpenClaw](https://atlas.mitre.org/studies/AML.CS0050) | [EAA-C-032](cases.md#eaa-c-032--openclaw-control-gateway-takeover) |
| [AML.CS0055: AI ClickFix](https://atlas.mitre.org/studies/AML.CS0055) | [EAA-C-033](cases.md#eaa-c-033--ai-clickfix-through-a-computer-use-interface) |
| [AML.CS0054: remote poisoned MCP tool](https://atlas.mitre.org/studies/AML.CS0054) | [EAA-C-009](cases.md#eaa-c-009--mcp-injection-and-rug-pull-research) |

Two groups of ATLAS cases fall outside EAA’s scope:

- Attacker-operated agent campaigns and evaluation agents attacking external infrastructure (AML.CS0068 through AML.CS0071) do not, by themselves, establish abuse of a victim-side agent.
- Recommendation poisoning (AML.CS0072) does not establish an EAA procedure when the supported effect is only changed output or a recommendation. A later agent-specific installation or endpoint action needs its own evidence.
