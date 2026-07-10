# Surfaces

Surfaces describe **where** an endpoint-agent technique acts. They are separate from [`tactics.md`](tactics.md), which describe the adversary's objective. A technique can touch several surfaces, but the catalog assigns one primary surface for navigation. A secondary surface is recorded only when the technique's core action directly manipulates, selects, reads, or invokes that surface—not merely because a downstream consequence could occur there.

| Surface | What it covers | Techniques |
|---|---|---|
| Launcher | The process, automation, extension, package lifecycle, service, or user session that starts the agent and selects its execution mode. | EAA-001, EAA-002 |
| Runtime & Environment | Launch-time environment, profile selection, provider routing, installed-agent discovery, and other effective runtime state. | EAA-007, EAA-008, EAA-016 |
| Control Plane | Instructions, memory, rules, hooks, plugins, skills, and other durable inputs that shape behavior across turns or sessions. | EAA-003, EAA-004, EAA-009, EAA-013, EAA-014 |
| State & Telemetry | Transcripts, tool history, logs, caches, session state, and observability output. | EAA-005, EAA-012, EAA-017 |
| Tools & Integrations | MCP servers, tool definitions, plugin-provided capabilities, and the configuration that connects an agent to local or remote tools. | EAA-006, EAA-010, EAA-011 |
| Identity & Authority | Filesystem, shell, browser, CLI, cloud, SaaS, and integration access inherited from the user or endpoint. | EAA-015 |

## Secondary surface assignments

| Technique | Secondary surfaces | Direct contact |
|---|---|---|
| EAA-005 | Identity & Authority | Complete agent-state collection can directly acquire stored credentials or tokens. |
| EAA-006 | Control Plane | Durable MCP/tool configuration is behavior-shaping control-plane state. |
| EAA-008 | Control Plane; State & Telemetry | Selecting an alternate profile directly selects its settings, plugins, session history, and other stored state. |
| EAA-011 | Runtime & Environment | The attacker action is manipulation of a launch-environment value referenced by MCP configuration. |
| EAA-012 | Runtime & Environment | Exporter and helper behavior can be selected through the effective process environment. |
| EAA-015 | Tools & Integrations | The technique directly invokes authenticated local tools, CLIs, MCP servers, or delegated integrations. |
| EAA-016 | Control Plane; State & Telemetry; Tools & Integrations; Identity & Authority | The discovery action can directly enumerate agent configuration, state, connected capabilities, and available authority. |

## Modeling rules

- A surface is an affected subsystem, not an attacker objective or evidence source.
- The primary surface should describe the part of the agent ecosystem most directly manipulated by the technique.
- Secondary surfaces are direct contacts in the technique definition, not a list of every possible impact surface.
- Product-specific paths, scopes, and precedence belong in procedure records rather than the surface definition.
- A technique can cross surfaces. For example, a malicious launcher may select a shadow profile, which loads a hook that later uses inherited authority.
- Cross-agent fan-out planting does not prove that every planted configuration activated.

Example chain:

```text
package install script            -> Launcher
alternate profile / base URL      -> Runtime & Environment
project or user hook write        -> Control Plane
new or changed MCP definition     -> Tools & Integrations
transcript read or rewrite        -> State & Telemetry
authenticated GitHub action       -> Identity & Authority
```
