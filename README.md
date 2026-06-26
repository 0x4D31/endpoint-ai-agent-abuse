# Endpoint AI Agent Abuse (EAA)

A curated catalog of techniques for abusing local AI agents.

EAA tracks how attackers can misuse local AI agents — especially coding and developer agents — as execution, persistence, collection, and inherited-access surfaces.

The scope is deliberately narrow. This is not a general AI security taxonomy or a list of every way attackers use LLMs. The focus is endpoint-resident agents such as Claude Code, Gemini CLI, Codex, Cursor, Kiro, Windsurf, and similar tools, plus the local surfaces around them: runtime flags, environment variables, config, hooks, plugins, MCP, transcripts, memory, and inherited credentials/tools.

Entries require a public anchor: an incident, malicious artifact, official documentation, or credible research. Unproven ideas stay in [`candidates.md`](candidates.md).

## Start here

- [`techniques/index.md`](techniques/index.md) — main catalog
- [`surfaces.md`](surfaces.md) — endpoint-agent surfaces used by the catalog
- [`cases.md`](cases.md) — incidents and malicious artifacts mapped to techniques
- [`hunting.md`](hunting.md) — detection and forensics starting points
- [`candidates.md`](candidates.md) — plausible ideas not promoted yet
- [`evidence.md`](evidence.md) — inclusion and promotion rules
- [`data/catalog.json`](data/catalog.json) — machine-readable catalog

## Techniques

| ID | Technique | Surface | Evidence |
|---|---|---|---|
| [EAA-001](techniques/index.md#eaa-001--agent-cli-invocation-by-untrusted-parent) | Agent CLI invocation by untrusted parent | Invocation | observed |
| [EAA-002](techniques/index.md#eaa-002--permissive-or-unattended-agent-execution) | Permissive or unattended agent execution | Invocation | malicious artifact |
| [EAA-003](techniques/index.md#eaa-003--lifecycle-hook-persistence) | Lifecycle hook persistence | Control Plane | observed |
| [EAA-004](techniques/index.md#eaa-004--persistent-instruction-or-memory-poisoning) | Persistent instruction or memory poisoning | Control Plane | documented surface |
| [EAA-005](techniques/index.md#eaa-005--transcript-and-agent-state-collection) | Transcript and agent-state collection | State & Telemetry | documented surface |
| [EAA-006](techniques/index.md#eaa-006--mcp-or-tool-configuration-abuse) | MCP or tool configuration abuse | Capabilities | observed |
| [EAA-007](techniques/index.md#eaa-007--hostile-modelapi-gateway-routing) | Hostile model/API gateway routing | Runtime | documented surface |
| [EAA-008](techniques/index.md#eaa-008--shadow-agent-config-directory) | Shadow agent config directory | Runtime | documented surface |
| [EAA-009](techniques/index.md#eaa-009--remote-plugin-or-marketplace-hot-load) | Remote plugin or marketplace hot-load | Control Plane | documented surface |
| [EAA-010](techniques/index.md#eaa-010--mcp-dynamic-tool-mutation-or-pushed-context) | MCP dynamic tool mutation or pushed context | Capabilities | research |
| [EAA-011](techniques/index.md#eaa-011--environment-expanded-mcp-activation) | Environment-expanded MCP activation | Capabilities | documented surface |
| [EAA-012](techniques/index.md#eaa-012--observabilitylogging-exfiltration) | Observability/logging exfiltration | State & Telemetry | documented surface |
| [EAA-013](techniques/index.md#eaa-013--cloud-synced-skill-drift) | Cloud-synced skill drift | Control Plane | documented surface |
| [EAA-014](techniques/index.md#eaa-014--multi-agent-config-fan-out) | Multi-agent config fan-out | Control Plane | observed |
| [EAA-015](techniques/index.md#eaa-015--inherited-authority-abuse) | Inherited authority abuse | Inherited Authority | observed |
| [EAA-016](techniques/index.md#eaa-016--agent-config-and-permission-reconnaissance) | Agent config and permission reconnaissance | Inherited Authority | observed |

## Versioning

Current catalog version: **0.1.0**.

Bump minor versions for taxonomy, surface, evidence, or naming changes. Patch versions are enough for wording fixes, source updates, and new examples that do not change the model.

## License

Released under [CC0 1.0 Universal](LICENSE).
