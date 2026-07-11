# Endpoint AI Agent Abuse (EAA)

A curated, evidence-scoped catalog of techniques for abusing endpoint-resident AI agents.

EAA tracks how attackers can misuse local agents—especially coding and developer agents—as execution, persistence, collection, exfiltration, defense-evasion, and inherited-authority surfaces. The focus is the endpoint behavior around agents: launchers and flags, environment and provider routing, instructions, memory, hooks, plugins, skills, MCP, transcripts, telemetry, and access inherited from the local user.

This is not a general AI security taxonomy or a claim that every technique applies identically to every product. Product applicability is asserted only where an official document, primary artifact, incident, or reproducible study supports it. Trust gates, defaults, operating systems, and product versions are part of the claim.

## Start here

- [`techniques/index.md`](techniques/index.md) — main catalog
- [`surfaces.md`](surfaces.md) — where a technique acts
- [`tactics.md`](tactics.md) — the adversary objective
- [`cases.md`](cases.md) — procedure-level incident, artifact, and research mappings
- [`hunting.md`](hunting.md) — detection and forensic hypotheses with telemetry and limitations
- [`candidates.md`](candidates.md) — plausible ideas below the promotion threshold
- [`evidence.md`](evidence.md) — maturity, source, outcome, and confidence rules
- [`data/catalog.json`](data/catalog.json) — machine-readable catalog
- [`data/catalog.schema.json`](data/catalog.schema.json) — catalog schema
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — entry and source requirements

## Evidence model

Technique maturity and evidence source are independent:

- `feasible` — an authoritative source establishes the surface and an agent-specific abuse path, but no public implementation is known;
- `demonstrated` — public research or a malicious artifact implements the technique;
- `observed` — an incident-context case establishes that the scoped attacker action was planted, executed, or produced confirmed impact. For a planting technique, this does not imply later activation.

Cases separately record whether a procedure was present, planted, attempted, executed, or produced confirmed impact. An `observed` technique does not mean that every cited artifact executed successfully or that every reported downstream effect was confirmed. See [`evidence.md`](evidence.md) for the full rules.

## Techniques

| ID | Technique | Primary surface | Tactics | Maturity |
|---|---|---|---|---|
| [EAA-001](techniques/index.md#eaa-001--agent-cli-invocation-by-adversary-controlled-initiator) | Agent CLI invocation by adversary-controlled initiator | Launcher | Execution | demonstrated |
| [EAA-002](techniques/index.md#eaa-002--permissive-or-unattended-agent-execution) | Permissive or unattended agent execution | Launcher | Execution | demonstrated |
| [EAA-003](techniques/index.md#eaa-003--lifecycle-hook-planting) | Lifecycle hook planting | Control Plane | Execution, Persistence | observed |
| [EAA-004](techniques/index.md#eaa-004--persistent-instruction-or-memory-poisoning) | Persistent instruction or memory poisoning | Control Plane | Persistence | observed |
| [EAA-005](techniques/index.md#eaa-005--transcript-and-agent-state-collection) | Transcript and agent-state collection | State & Telemetry | Credential Access, Collection | observed |
| [EAA-006](techniques/index.md#eaa-006--mcp-or-tool-configuration-abuse) | MCP or tool configuration abuse | Tools & Integrations | Execution, Persistence | demonstrated |
| [EAA-007](techniques/index.md#eaa-007--hostile-modelapi-gateway-routing) | Hostile model/API gateway routing | Runtime & Environment | Collection, Exfiltration | demonstrated |
| [EAA-008](techniques/index.md#eaa-008--shadow-agent-profile-or-config-directory) | Shadow agent profile or config directory | Runtime & Environment | Execution, Defense Evasion | demonstrated |
| [EAA-009](techniques/index.md#eaa-009--remote-plugin-sideload-or-marketplace-installation) | Remote plugin sideload or marketplace installation | Control Plane | Execution, Persistence | feasible |
| [EAA-010](techniques/index.md#eaa-010--mcp-tool-poisoning-or-definition-drift) | MCP tool poisoning or definition drift | Tools & Integrations | Execution, Collection, Exfiltration | demonstrated |
| [EAA-011](techniques/index.md#eaa-011--environment-variable-manipulation-of-mcp-activation) | Environment-variable manipulation of MCP activation | Tools & Integrations | Execution | feasible |
| [EAA-012](techniques/index.md#eaa-012--telemetry-redirection-or-sensitive-logging) | Telemetry redirection or sensitive logging | State & Telemetry | Execution, Collection, Exfiltration | demonstrated |
| [EAA-013](techniques/index.md#eaa-013--cloud-hosted-skill-poisoning-and-sync) | Cloud-hosted skill poisoning and sync | Control Plane | Execution, Persistence | feasible |
| [EAA-014](techniques/index.md#eaa-014--cross-agent-control-plane-fan-out-planting) | Cross-agent control-plane fan-out planting | Control Plane | Persistence | observed |
| [EAA-015](techniques/index.md#eaa-015--inherited-authority-abuse) | Inherited authority abuse | Identity & Authority | Execution, Collection, Exfiltration | observed |
| [EAA-016](techniques/index.md#eaa-016--agent-environment-discovery) | Agent environment discovery | Runtime & Environment | Discovery | demonstrated |
| [EAA-017](techniques/index.md#eaa-017--agent-native-evidence-tampering) | Agent-native evidence tampering | State & Telemetry | Defense Evasion | observed |

## Validation

Run the dependency-free validator before submitting changes:

```bash
python3 scripts/validate.py
```

It validates the structured catalog and cross-checks IDs, metadata, relationships, canonical case mappings, cases, surfaces, tactics, candidates, versions, and local links. A passing result confirms structural consistency, not the truth of an external source; claim-level source review is still required.

## Versioning

Current catalog version: **0.2.0**.

Bump minor versions for taxonomy, surface, evidence, or naming changes. Patch versions are enough for wording fixes, source updates, and new examples that do not change the model.

## License

Released under [CC0 1.0 Universal](LICENSE).
