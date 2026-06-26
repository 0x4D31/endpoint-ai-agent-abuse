# Hunting

Starting points for detection and forensics. Keep these correlation-first; single indicators are noisy.

## H1 — Agent launched by untrusted parent

**Techniques:** EAA-001, EAA-002, EAA-016

Look for package managers, installers, IDE extension hosts, repo setup scripts, CI jobs, or document handlers launching local agents.

```text
untrusted parent -> agent process -> sensitive read or SaaS/cloud action
```

## H2 — Permissive agent execution

**Techniques:** EAA-002

Look for unattended, approval-bypass, sandbox-disabled, or trust-all flags on agent processes.

```text
agent process + permissive flag + no TTY + suspicious parent
```

## H3 — Control-plane write followed by execution

**Techniques:** EAA-003, EAA-004, EAA-009, EAA-013, EAA-014

Track writes to agent hooks, instructions, memory, rules, plugins, skills, or marketplaces, then correlate to later agent start/reload/tool execution.

```text
unexpected writer -> agent control-plane file -> agent start/reload -> hook/plugin/tool activity
```

## H4 — Transcript and state collection

**Techniques:** EAA-005, EAA-012

Look for non-agent processes reading agent transcripts, plans, logs, caches, memory stores, or session files in bulk.

```text
bulk state read -> archive/encode -> network/upload
```

## H5 — Hostile gateway or shadow profile

**Techniques:** EAA-007, EAA-008

Alert on provider gateway/env/config overrides outside approved domains or profile paths.

```text
provider base URL / custom headers / config dir override -> agent start
```

## H6 — Capability drift

**Techniques:** EAA-006, EAA-010, EAA-011

Track first-seen MCP servers, tool definitions, env-expanded config, tool-list changes, and pushed context.

```text
new capability -> reload/start -> new tool/hook/network action
```

## H7 — Observability exfiltration

**Techniques:** EAA-012

Watch for tracing/logging env vars that route raw prompts, tool content, or API bodies to unknown collectors.

## H8 — Inherited authority abuse

**Techniques:** EAA-015

Correlate agent sessions to downstream `gh`, cloud CLI, Slack, browser, package-manager, or MCP actions.

```text
agent session -> authenticated local tool -> GitHub/Slack/cloud/package action
```

## H9 — Agent surface reconnaissance

**Techniques:** EAA-016

Look for one process enumerating many agent binaries, config directories, MCP files, skills, hooks, rules, or transcript paths.

```text
multi-agent enumeration -> agent launch / config write / state collection
```

## H10 — Evidence gap

**Techniques:** EAA-005, EAA-012, EAA-015

Flag sensitive endpoint/SaaS action with no matching agent transcript/tool-call evidence, or deleted/truncated agent state.
