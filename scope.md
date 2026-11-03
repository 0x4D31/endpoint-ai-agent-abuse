# Scope

EAA tracks attacks that misuse an AI agent, its configuration, or its integrations in a victim’s environment. The attacker targets access that the agent has on behalf of the victim user or organization.

The catalog covers developer workstations, development containers, CI jobs, and other agent runners. The affected agent or component must belong to or operate for the victim; an attacker’s own agent is outside this scope.

## Inclusion test

A technique or case belongs in EAA when all of the following are true:

1. **Victim-side agent:** the affected agent, runner, or agent configuration belongs to or operates for the victim, rather than being only an attacker-operated tool.
2. **Agent-specific mechanism:** the attacker acts through an agent launcher, task or retrieved-context input path, control plane, runtime, tool integration, state store, telemetry path, or inherited authority. Generic malware in an AI-branded package is not enough.
3. **Endpoint or delegated consequence:** the mechanism can affect local execution, persistence, discovery, collection, exfiltration, defense evasion, or an authenticated action delegated from that environment.

Publication or discovery alone may support a `present` outcome only when the inspected artifact itself implements an EAA technique. It does not establish planting, activation, execution, or impact on a victim.

## Included examples

- An installer, extension, repository, or other external process invokes a victim-side agent or writes its configuration.
- Adversarial content reaches an endpoint agent through a repository, issue, tool result, log, or other input and induces a local or delegated action.
- An attacker commandeers or copies an existing endpoint-agent environment and uses authority available in that environment.
- A hosted runner is in scope when an agent running for the victim organization is the confused deputy and the procedure affects its execution or delegated authority.

## Excluded examples

- An attacker uses an agent on attacker-controlled infrastructure against a conventional target.
- Malware is distributed through an AI-related package but does not manipulate an agent-specific surface or authority.
- An agent causes accidental damage without adversarial influence.
- A prompt-injection result changes only model output and produces no endpoint or delegated action.
- A scan reports suspicious instructions or marketplace prevalence without establishing an agent-specific procedure in an inspectable artifact.

## Cases that need care

| Scenario | Decision | Reason |
|---|---|---|
| Attacker uses a copied victim agent installation, its state, or its authenticated environment | Include | The abused agent environment and inherited authority are victim-side even if the attacker later controls the host. |
| Autonomous offensive agent runs from evaluation or attacker infrastructure | Exclude | The agent is the attacker's instrument, not a victim-side confused deputy. |
| Malicious repository is surfaced or recommended, but no agent-specific local procedure is established | Hold | Discovery alone does not establish endpoint-agent abuse. |
| Large-scale scan of public skills or instructions | Source or corpus lead | Prevalence evidence can inform research, but is not automatically a case. |

When a case’s fit remains uncertain, record it in [`candidates.md`](candidates.md) rather than stretching an existing technique or outcome.

## Incident leads awaiting a mechanism

Binance’s [November 3 initial report](https://www.binance.com/en/blog/community/3229153443759566763) says attackers used a compromised employee computer and an internal AI tool to gain control of two wallet engineers’ systems on October 20, 2026. It does not identify the tool’s execution model, the attacker’s requests, or the permissions exercised. The disclosure does not yet support a technique mapping or attribute the theft to an agent procedure.

[Mandiant’s September 2026 report](https://cloud.google.com/security/resources/ai-risk-and-resilience-2026) also describes an incident involving an internal AI repository and tampered assistant CLI hooks. It reports code execution but does not identify the hook type or invocation path. That description alone does not distinguish lifecycle-hook planting from modification of executable tool code; no separate mapping is assigned.
