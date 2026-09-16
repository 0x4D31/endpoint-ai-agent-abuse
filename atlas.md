# EAA and MITRE ATLAS

MITRE ATLAS is useful for finding relevant research and comparing mechanisms. Its scope is broader than EAA: an ATLAS case can concern a hosted assistant, a model, an AI supply chain, or an attacker operating an agent. EAA requires the victim-side agent or agent ecosystem boundary in [`scope.md`](scope.md).

This review uses the [ATLAS 2026.09 release](https://github.com/mitre-atlas/atlas-data/releases/tag/v2026.09), modified September 15, 2026, and its [versioned dataset at commit `3259f388`](https://github.com/mitre-atlas/atlas-data/blob/3259f388d19cbcca11bacf12a0ef97f4198f711b/dist/v6/ATLAS-2026.09.yaml). Reviewed September 16, 2026. These are editorial comparisons, not equivalence assertions or an official MITRE mapping. Follow the primary sources in each EAA case for outcomes, applicability, and confidence; ATLAS inclusion does not establish execution on a victim endpoint.

## Mechanism comparison

| EAA mechanism | Relevant ATLAS entry | Relationship and limit |
|---|---|---|
| EAA-001: adversary-controlled CLI launch | [AML.T0053: AI Agent Tool Invocation](https://atlas.mitre.org/techniques/AML.T0053) | Partial overlap. EAA distinguishes who launches the agent from what tools it later invokes. |
| EAA-002, EAA-003, EAA-006, EAA-008, EAA-011, EAA-014: permissive execution, hooks, tool registration, profiles, activation environment, and cross-agent planting | [AML.T0081: Modify AI Agent Configuration](https://atlas.mitre.org/techniques/AML.T0081) | Configuration modification can implement these paths. EAA additionally distinguishes launch-time choices, activation gates, and the specific endpoint surface; not every procedure modifies stored configuration. |
| EAA-004: persistent instructions or memory | [AML.T0080.000: Memory](https://atlas.mitre.org/techniques/AML.T0080.000), [AML.T0081](https://atlas.mitre.org/techniques/AML.T0081) | Partial overlap. A durable rules file and agent-managed memory have different writers and activation conditions. |
| EAA-005: transcript and state collection | [AML.T0083: Credentials from AI Agent Configuration](https://atlas.mitre.org/techniques/AML.T0083) | Credential-bearing configuration is a subset. Transcripts, session history, and other state can be valuable without containing credentials. |
| EAA-007 and EAA-012: model routing and telemetry changes | [AML.T0081](https://atlas.mitre.org/techniques/AML.T0081) | Related configuration action; EAA identifies the affected data path. A local gateway control-interface takeover is not automatically hostile model-provider routing. |
| EAA-009: remote plugin or skill installation/update | [AML.T0010.005: AI Agent Tool](https://atlas.mitre.org/techniques/AML.T0010.005), [AML.T0115.002: AI Agent Tools](https://atlas.mitre.org/techniques/AML.T0115.002) | Related supply-chain and publication actions. Publication alone does not establish installation, loading, or later execution. |
| EAA-010: tool-definition poisoning or drift | [AML.T0110.000: Definition and Instructions](https://atlas.mitre.org/techniques/AML.T0110.000) | Closely related mechanism, subject to EAA's victim-side scope. Distinct from hidden implementation behavior and instructions in runtime results. |
| EAA-013: cloud-hosted skill poisoning and sync | [AML.T0081](https://atlas.mitre.org/techniques/AML.T0081), [AML.T0080.000](https://atlas.mitre.org/techniques/AML.T0080.000) | Partial overlap only. EAA requires the account-backed cloud modification and local synchronization path; an installer fetching an updated marketplace skill does not establish that path. |
| EAA-015: inherited authority | [AML.T0053](https://atlas.mitre.org/techniques/AML.T0053), [AML.T0086: Exfiltration via AI Agent Tool Invocation](https://atlas.mitre.org/techniques/AML.T0086) | Map only the relevant procedure. Inherited filesystem, credential, or authenticated session access is broader than exfiltration. |
| EAA-016: agent environment discovery | [AML.T0084: Discover AI Agent Configuration](https://atlas.mitre.org/techniques/AML.T0084), [AML.T0133: Discover AI Agent Runtime Capabilities](https://atlas.mitre.org/techniques/AML.T0133) | Related discovery actions. Reading static configuration does not prove a tool is available or permitted in a running session. |
| EAA-017: agent-native evidence tampering | No close mechanism-level mapping selected | Preserve the agent-state and forensic-evidence boundary rather than assign a broad evasion label as an equivalent. |
| EAA-018: task-context instruction injection | [AML.T0051.001: Indirect](https://atlas.mitre.org/techniques/AML.T0051.001); [AML.T0110.002: Runtime Response](https://atlas.mitre.org/techniques/AML.T0110.002) for the tool-response subset | EAA requires a scoped endpoint or delegated action. Ordinary issue, log, web, or rendered content is not necessarily a poisoned tool implementation; a trusted integration can transport attacker-controlled upstream data. |
| EAA-019: preflight helper execution through repository metadata | No close mechanism-level mapping selected | A helper interpreting command-bearing local metadata can execute before any model-directed action. Do not label it prompt injection without evidence. |
| EAA-020: agent-consumed reference takeover | No close mechanism-level mapping selected | Taking over a package/domain reference used by an agent differs from modifying the instructions containing that reference. A model-name or namespace technique should not be generalized to this path without checking its scope. |
| EAA-021: tool implementation poisoning | [AML.T0110.001: Implementation](https://atlas.mitre.org/techniques/AML.T0110.001) | Closely related mechanism. The executable tool can perform an undisclosed side effect during an ordinary invocation without persuading the model to request that effect. |

This comparison does not add causal relationships to the catalog. A procedure may combine several techniques, but one case's sequence does not establish a universal prerequisite between them.

## Case decisions

The ATLAS review identified five useful additions and one case already represented. The additions below were checked against their primary research, artifacts, or vendor advisories rather than copied from the ATLAS narratives.

| ATLAS case | EAA decision | Evidence boundary |
|---|---|---|
| [AML.CS0047: Amazon Q extension](https://atlas.mitre.org/studies/AML.CS0047) | Add [EAA-C-029](cases.md#eaa-c-029--amazon-q-vs-code-extension-destructive-agent-payload) | Malicious launcher and permissive flags were present. AWS says a syntax error prevented execution; no attempted or completed destructive action is inferred. |
| [AML.CS0053: Postmark MCP](https://atlas.mitre.org/studies/AML.CS0053) | Add [EAA-C-030](cases.md#eaa-c-030--postmark-mcp-implementation-backdoor) and EAA-021 | Inspected code supports hidden BCC behavior. Public evidence cited here does not establish a particular victim's tool call or email delivery. |
| [AML.CS0067: Claude Code GitHub Action](https://atlas.mitre.org/studies/AML.CS0067) | Add [EAA-C-031](cases.md#eaa-c-031--claude-code-github-action-process-environment-disclosure) | Controlled research supports process-environment disclosure through the Read tool. Do not present every proposed exfiltration channel as reproduced. |
| [AML.CS0050: OpenClaw](https://atlas.mitre.org/studies/AML.CS0050) | Add [EAA-C-032](cases.md#eaa-c-032--openclaw-control-gateway-takeover) | Authenticated gateway authority enabled policy reconfiguration and host execution in research. This does not establish a container-runtime escape. Vendor and research affected ranges are recorded separately. |
| [AML.CS0055: AI ClickFix](https://atlas.mitre.org/studies/AML.CS0055) | Add [EAA-C-033](cases.md#eaa-c-033--ai-clickfix-through-a-computer-use-interface) | Rendered page content induced a computer-use agent to operate clipboard and terminal in a controlled demonstration. No general product/version success claim is made. |
| [AML.CS0054: remote poisoned MCP tool](https://atlas.mitre.org/studies/AML.CS0054) | Already represented by EAA-C-009 | Preserve the existing Invariant case instead of adding a second case for the same underlying research. |

Three additional primary-source cases address gaps identified during EAA's earlier assessment: Mitiga's poisoned coding assessment (EAA-C-034), Orca's marketplace/update research (EAA-C-035), and Sentry Agentjacking (EAA-C-036). Their procedure rows distinguish reported incident activity from controlled callbacks, and distinguish persistent rules, tool definitions, and transient error data.

Other ATLAS entries remain leads or outside the current inclusion boundary:

- Rules File Backdoor (AML.CS0041) and MCP web-context exfiltration (AML.CS0045) are relevant leads, but this release does not add a case without completing an independent primary-source review of activation and endpoint effects.
- Exposed ClawdBot interfaces and poisoned skills (AML.CS0048 and AML.CS0049) do not justify importing exposure counts as successful compromise counts. The cited social-post evidence needs further artifact-level review before additional EAA procedure assertions.
- Attacker-operated agent campaigns and evaluation agents attacking external infrastructure (AML.CS0068 through AML.CS0071) do not, by themselves, establish abuse of a victim-side agent.
- Recommendation poisoning (AML.CS0072) does not establish an EAA procedure when the supported effect is only changed output or a recommendation. A later agent-specific installation or endpoint action would need its own evidence.

## Resulting catalog choices

- Add only EAA-021 as a new technique: the code behind a tool is a distinct execution boundary from its description and returned data.
- Preserve EAA-018 for rendered content, issues, logs, and tool-result instructions; do not create separate techniques solely for each delivery format.
- Keep EAA-013 at `feasible`: marketplace updates and nested skill replacement support EAA-009/EAA-004, not the specific cloud-to-local synchronization claim.
- Promote EAA-006 and EAA-010 to `observed` using the scoped Mitiga incident claims at medium confidence. This is a claim about those reported actions, not independent confirmation of every product or downstream consequence.
- Retain the existing schema, source assertions, and ordered procedure model. The additions do not require a normalized assertion-ID migration or universal causal edges.
