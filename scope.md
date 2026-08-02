# Scope

EAA tracks adversarial abuse of an AI agent, or its agent-specific ecosystem, in a victim-controlled execution environment. The agent must act, or be positioned to act, with authority available to the victim user or organization.

“Endpoint” includes developer workstations and other bounded environments where an agent runs with local or delegated authority, such as development containers and CI or agent runners. It does not require a physical laptop, but it does require a victim-side agent runtime or agent-specific surface.

## Inclusion test

A technique or case belongs in EAA when all of the following are true:

1. **Victim-side agent:** the affected agent, runner, or agent configuration belongs to or operates for the victim, rather than being only an attacker-operated tool.
2. **Agent-specific mechanism:** the attacker acts through an agent launcher, control plane, runtime, tool integration, state store, telemetry path, or inherited authority. Generic malware in an AI-branded package is not enough.
3. **Endpoint or delegated consequence:** the mechanism can affect local execution, persistence, discovery, collection, exfiltration, defense evasion, or an authenticated action delegated from that environment.

Publication or discovery alone may support a `present` outcome only when the inspected artifact itself implements an EAA technique. It does not establish planting, activation, execution, or impact on a victim.

## Included boundaries

- An installer, extension, repository, or other external process invokes a victim-side agent or writes its configuration.
- Adversarial content reaches an endpoint agent through a repository, issue, tool result, log, or other input and induces a local or delegated action.
- An attacker commandeers or copies an existing endpoint-agent environment and uses authority available in that environment.
- A hosted runner is in scope when an agent running for the victim organization is the confused deputy and the procedure affects its execution or delegated authority.

## Adjacent but excluded

- An attacker uses an agent on attacker-controlled infrastructure against a conventional target.
- Malware is distributed through an AI-related package but does not manipulate an agent-specific surface or authority.
- An agent causes accidental damage without adversarial influence.
- A prompt-injection result changes only model output and produces no endpoint or delegated action.
- A scan reports suspicious instructions or marketplace prevalence without establishing an agent-specific procedure in an inspectable artifact.

## Boundary decisions

| Scenario | Decision | Reason |
|---|---|---|
| Attacker uses a copied victim agent installation, its state, or its authenticated environment | Include | The abused agent environment and inherited authority are victim-side even if the attacker later controls the host. |
| Autonomous offensive agent runs from evaluation or attacker infrastructure | Exclude | The agent is the attacker's instrument, not a victim-side confused deputy. |
| Malicious repository is surfaced or recommended, but no agent-specific local procedure is established | Hold | Discovery alone does not establish endpoint-agent abuse. |
| Large-scale scan of public skills or instructions | Source or corpus lead | Prevalence evidence can inform research, but is not automatically a case. |

When a boundary remains uncertain, record it in [`candidates.md`](candidates.md) rather than stretching an existing technique or outcome.
