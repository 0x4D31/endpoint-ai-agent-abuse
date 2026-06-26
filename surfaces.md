# Surfaces

The catalog groups techniques by endpoint-agent surface. A technique may touch more than one surface, but each entry has one primary home.

| Surface | What it covers | Techniques |
|---|---|---|
| Invocation | Who starts the agent, from where, and with what mode. | EAA-001, EAA-002 |
| Runtime | Launch environment and process-level behavior before the agent begins normal work. | EAA-007, EAA-008 |
| Control Plane | Files and settings that shape agent behavior across sessions: instructions, memory, rules, hooks, plugins, skills. | EAA-003, EAA-004, EAA-009, EAA-013, EAA-014 |
| State & Telemetry | Local transcripts, tool history, logs, caches, and observability output. | EAA-005, EAA-012 |
| Capabilities | Tools the agent can call: MCP servers, built-in tools, dynamic tool definitions, env-expanded tool config. | EAA-006, EAA-010, EAA-011 |
| Inherited Authority | Access the agent inherits from the user or endpoint: shell, files, browser state, CLIs, SaaS sessions, cloud creds. | EAA-015, EAA-016 |

## Why these surfaces

Endpoint agents blur normal boundaries. A single session can read local files, load project config, call MCP servers, invoke tools, use existing credentials, and leave transcripts behind. These surfaces separate the attacker’s entry point from the thing they ultimately abuse.

Example:

```text
package install script        -> Invocation
provider/config override      -> Runtime
Claude hook write             -> Control Plane
new MCP server                -> Capabilities
transcript read               -> State & Telemetry
gh repo upload                -> Inherited Authority
```
