# EAA and MITRE ATLAS

MITRE ATLAS is useful for finding relevant research and comparing mechanisms. Its scope is broader than EAA: an ATLAS case can concern a hosted assistant, a model, an AI supply chain, or an attacker operating an agent. EAA requires the victim-side agent or agent ecosystem boundary in [`scope.md`](scope.md).

This review uses the [ATLAS 2026.09 release](https://github.com/mitre-atlas/atlas-data/releases/tag/v2026.09), modified September 15, 2026, and its [versioned dataset at commit `3259f388`](https://github.com/mitre-atlas/atlas-data/blob/3259f388d19cbcca11bacf12a0ef97f4198f711b/dist/v6/ATLAS-2026.09.yaml). Reviewed September 16, 2026. These are editorial comparisons, not equivalence assertions or an official MITRE mapping. Follow the primary sources in each EAA case for outcomes, applicability, and confidence; ATLAS inclusion does not establish execution on a victim endpoint.

## Selected mechanism comparisons

These four comparisons identify specific overlaps useful to EAA. They are not a complete crosswalk.

| EAA mechanism | Relevant ATLAS entry | Relationship and limit |
|---|---|---|
| EAA-010: tool-definition poisoning or drift | [AML.T0110.000: Definition and Instructions](https://atlas.mitre.org/techniques/AML.T0110.000) | Closely related mechanism, subject to EAA's victim-side scope. Distinct from hidden implementation behavior and instructions in runtime results. |
| EAA-016: agent environment discovery | [AML.T0084: Discover AI Agent Configuration](https://atlas.mitre.org/techniques/AML.T0084), [AML.T0133: Discover AI Agent Runtime Capabilities](https://atlas.mitre.org/techniques/AML.T0133) | Related discovery actions. Reading static configuration does not prove a tool is available or permitted in a running session. |
| EAA-018: task-context instruction injection | [AML.T0051.001: Indirect](https://atlas.mitre.org/techniques/AML.T0051.001); [AML.T0110.002: Runtime Response](https://atlas.mitre.org/techniques/AML.T0110.002) for the tool-response subset | EAA requires a scoped endpoint or delegated action. Ordinary issue, log, web, or rendered content is not necessarily a poisoned tool implementation; a trusted integration can transport attacker-controlled upstream data. |
| EAA-021: tool implementation poisoning | [AML.T0110.001: Implementation](https://atlas.mitre.org/techniques/AML.T0110.001) | Closely related mechanism. The executable tool can perform an undisclosed side effect during an ordinary invocation without persuading the model to request that effect. |

## Case decisions

The ATLAS review identified five useful additions and one case already represented. The additions below were checked against their primary research, artifacts, or vendor advisories rather than copied from the ATLAS narratives.

| ATLAS case | EAA decision | Evidence boundary |
|---|---|---|
| [AML.CS0047: Amazon Q extension](https://atlas.mitre.org/studies/AML.CS0047) | Add [EAA-C-029](cases.md#eaa-c-029--amazon-q-vs-code-extension-destructive-agent-payload) | Malicious launcher and permissive flags were present. AWS says a syntax error prevented execution; no attempted or completed destructive action is inferred. |
| [AML.CS0053: Postmark MCP](https://atlas.mitre.org/studies/AML.CS0053) | Add [EAA-C-030](cases.md#eaa-c-030--postmark-mcp-implementation-backdoor) and EAA-021 | Inspected code supports hidden BCC behavior. Public evidence cited here does not establish a particular victim's tool call or email delivery. |
| [AML.CS0067: Claude Code GitHub Action](https://atlas.mitre.org/studies/AML.CS0067) | Add [EAA-C-031](cases.md#eaa-c-031--claude-code-github-action-process-environment-disclosure) | Controlled research supports process-environment disclosure through the Read tool. Do not present every proposed exfiltration channel as reproduced. |
| [AML.CS0050: OpenClaw](https://atlas.mitre.org/studies/AML.CS0050) | Add [EAA-C-032](cases.md#eaa-c-032--openclaw-control-gateway-takeover) | The researcher reports using gateway authority for policy reconfiguration and host execution; the published request does not independently confirm the marker-file effect. This does not establish a container-runtime escape. Vendor and research affected ranges are recorded separately. |
| [AML.CS0055: AI ClickFix](https://atlas.mitre.org/studies/AML.CS0055) | Add [EAA-C-033](cases.md#eaa-c-033--ai-clickfix-through-a-computer-use-interface) | Rendered page content induced a computer-use agent to operate clipboard and terminal in a controlled demonstration. No general product/version success claim is made. |
| [AML.CS0054: remote poisoned MCP tool](https://atlas.mitre.org/studies/AML.CS0054) | Already represented by EAA-C-009 | Preserve the existing Invariant case instead of adding a second case for the same underlying research. |

The comparison also preserves two scope exclusions:

- Attacker-operated agent campaigns and evaluation agents attacking external infrastructure (AML.CS0068 through AML.CS0071) do not, by themselves, establish abuse of a victim-side agent.
- Recommendation poisoning (AML.CS0072) does not establish an EAA procedure when the supported effect is only changed output or a recommendation. A later agent-specific installation or endpoint action needs its own evidence.
