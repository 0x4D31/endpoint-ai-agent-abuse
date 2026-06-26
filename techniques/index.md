# Techniques

This is the main catalog. Each technique has a surface, evidence label, short abuse path, examples, hunting notes, and sources.

Surfaces are defined in [`../surfaces.md`](../surfaces.md). Evidence labels are defined in [`../evidence.md`](../evidence.md).

## EAA-001 — Agent CLI invocation by untrusted parent

**Surface:** Invocation  
**Evidence:** observed  
**Seen in:** Nx s1ngularity, Trivy OpenVSX extension  
**Related:** EAA-002, EAA-015, EAA-016

Malware, package scripts, extensions, repo bootstrap code, or CI jobs launch an installed local AI agent and use it as a trusted helper.

```text
untrusted parent process
  -> local agent CLI
  -> filesystem/tool reconnaissance
  -> credential or SaaS/cloud action
```

Examples:

- Nx malware discovered local AI agents and used available agents for semantic filesystem reconnaissance.
- The Trivy OpenVSX extension attempted to launch multiple local agents from extension code.

Hunt ideas:

- Package manager, installer, IDE extension host, repo setup script, or CI job starts an agent binary.
- Agent process has no TTY, runs detached, or starts outside normal interactive shell ancestry.
- Agent activity is followed by sensitive file reads, archiving, upload, or authenticated SaaS/cloud actions.

Sources: [Nx postmortem](https://nx.dev/blog/s1ngularity-postmortem), [Snyk Nx analysis](https://snyk.io/blog/weaponizing-ai-coding-agents-for-malware-in-the-nx-malicious-package/), [Aqua Trivy advisory](https://github.com/aquasecurity/trivy-vscode-extension/security/advisories/GHSA-8mr6-gf9x-j8qg), [Socket Trivy write-up](https://socket.dev/blog/unauthorized-ai-agent-execution-code-published-to-openvsx-in-aqua-trivy-vs-code-extension)

---

## EAA-002 — Permissive or unattended agent execution

**Surface:** Invocation  
**Evidence:** malicious artifact  
**Seen in:** Trivy OpenVSX extension, Nx s1ngularity  
**Related:** EAA-001, EAA-015

An attacker starts a local agent with flags or settings that reduce approval prompts, sandboxing, or trust checks.

```text
untrusted parent
  -> agent with approval-bypass / trust-all / sandbox-disabled mode
  -> agent executes tools with fewer interruptions
```

Examples:

- The Trivy extension attempted multiple agents with permissive or non-interactive execution modes.
- Nx malware tried to use available agents without relying on normal interactive user intent.

Hunt ideas:

- Agent command line includes approval-bypass, trust-all, sandbox-disabled, yolo, or similar flags.
- No TTY plus permissive flags.
- Permissive agent start from package lifecycle, extension host, or repo automation.

Sources: [Aqua Trivy advisory](https://github.com/aquasecurity/trivy-vscode-extension/security/advisories/GHSA-8mr6-gf9x-j8qg), [Socket Trivy write-up](https://socket.dev/blog/unauthorized-ai-agent-execution-code-published-to-openvsx-in-aqua-trivy-vs-code-extension), [Snyk Nx analysis](https://snyk.io/blog/weaponizing-ai-coding-agents-for-malware-in-the-nx-malicious-package/)

---

## EAA-003 — Lifecycle hook persistence

**Surface:** Control Plane  
**Evidence:** observed  
**Seen in:** Mini Shai-Hulud, Miasma  
**Related:** EAA-004, EAA-014

An attacker writes agent hook configuration so the agent runs attacker-controlled commands during session start, tool use, stop, or similar lifecycle events.

```text
malicious package/repo/extension
  -> writes agent hook config
  -> user starts or reloads agent
  -> hook launches attacker code
```

Examples:

- Mini Shai-Hulud planted Claude Code `SessionStart` hook persistence.
- Miasma used Claude and Gemini agent startup/config surfaces.

Hunt ideas:

- Writes to agent hook files by package managers, extension hosts, repo scripts, or unknown processes.
- Hook command points to shell, package manager, network fetch, opaque script, or recently written binary.
- Hook fires before or immediately after an agent session starts.

Sources: [StepSecurity Mini Shai-Hulud](https://www.stepsecurity.io/blog/a-mini-shai-hulud-has-appeared), [StepSecurity Miasma](https://www.stepsecurity.io/blog/miasma-worm-hits-microsoft-again-azure-functions-action-and-72-other-repositories-disabled-after-supply-chain-attack-targeting-ai-coding-agents), [Claude Code hooks docs](https://code.claude.com/docs/en/hooks)

---

## EAA-004 — Persistent instruction or memory poisoning

**Surface:** Control Plane  
**Evidence:** documented surface  
**Seen in:** no known public malware campaign yet  
**Related:** EAA-003, EAA-005, EAA-014

An attacker modifies local agent instructions, rules, or memory so later sessions load attacker-controlled guidance as trusted context.

```text
unexpected writer
  -> memory / instructions / rules file
  -> future agent session
  -> attacker instruction influences tool use or output
```

Examples:

- Claude Code documents local auto-memory stored as `MEMORY.md` and loaded into sessions.
- Miasma and Hades show the broader pattern of writing persistent assistant/rule files across agent ecosystems.

Hunt ideas:

- Non-editor process writes memory, rule, or instruction files.
- New instruction asks the agent to auto-run commands, ignore warnings, suppress findings, trust a domain, or send output elsewhere.
- Memory/rule write is followed by new tool behavior in later sessions.

Sources: [Claude Code memory docs](https://code.claude.com/docs/en/memory), [StepSecurity Miasma](https://www.stepsecurity.io/blog/miasma-worm-hits-microsoft-again-azure-functions-action-and-72-other-repositories-disabled-after-supply-chain-attack-targeting-ai-coding-agents), [StepSecurity Hades](https://www.stepsecurity.io/blog/the-hades-campaign-pypi-packages)

---

## EAA-005 — Transcript and agent-state collection

**Surface:** State & Telemetry  
**Evidence:** documented surface  
**Seen in:** no known public coding-agent transcript theft campaign yet  
**Related:** EAA-004, EAA-012

An attacker reads local transcripts, tool histories, plans, logs, caches, or session stores to recover secrets, internal context, repo details, or operational history.

```text
non-agent process
  -> bulk reads agent state
  -> archives or filters content
  -> exfiltrates useful context/secrets
```

Examples:

- Agent docs expose local transcript/history/state surfaces.
- Malicious packages already harvest developer files; agent state is a natural nearby target.

Hunt ideas:

- Non-agent process recursively reads transcript/history/cache directories.
- Bulk state reads followed by zip/tar/base64/curl/gh/cloud upload.
- Transcript files deleted or truncated after sensitive activity.

Sources: [Claude Code hooks docs](https://code.claude.com/docs/en/hooks), [Claude Code memory docs](https://code.claude.com/docs/en/memory)

---

## EAA-006 — MCP or tool configuration abuse

**Surface:** Capabilities  
**Evidence:** observed  
**Seen in:** Miasma, agent/MCP research  
**Related:** EAA-010, EAA-011, EAA-015

An attacker adds or modifies MCP/tool configuration so the agent gains a new filesystem, shell, browser, SaaS, or network capability.

```text
malicious config write
  -> new MCP/tool capability
  -> agent sees tool as available
  -> tool performs attacker-useful action
```

Examples:

- Supply-chain payloads have targeted agent config surfaces, including MCP-adjacent and assistant configuration files.
- MCP research shows tool descriptions and tool definitions can become an attack surface before or during tool use.

Hunt ideas:

- New MCP server or tool config from an untrusted writer.
- Stdio MCP command uses shell, package manager, network fetch, or unpinned package execution.
- Capability appears shortly before sensitive file, browser, GitHub, Slack, or cloud activity.

Sources: [Claude Code MCP docs](https://code.claude.com/docs/en/mcp), [Trail of Bits MCP line-jumping](https://blog.trailofbits.com/2025/04/21/jumping-the-line-how-mcp-servers-can-attack-you-before-you-ever-use-them/), [MCP injection experiments](https://github.com/invariantlabs-ai/mcp-injection-experiments), [StepSecurity Miasma](https://www.stepsecurity.io/blog/miasma-worm-hits-microsoft-again-azure-functions-action-and-72-other-repositories-disabled-after-supply-chain-attack-targeting-ai-coding-agents)

---

## EAA-007 — Hostile model/API gateway routing

**Surface:** Runtime  
**Evidence:** documented surface  
**Seen in:** no known public campaign yet  
**Related:** EAA-008, EAA-012

An attacker changes provider routing so a trusted local agent talks to an attacker-controlled or unapproved model/API gateway.

```text
changed env/config
  -> agent connects to attacker gateway
  -> prompts/tool context exposed or responses steered
```

Examples:

- Claude Code documents environment variables for API base URL, auth token, custom headers, and gateway behavior.
- The same idea applies to other agents that support custom model endpoints or provider gateways.

Hunt ideas:

- Provider base URL points outside approved domains.
- Custom auth headers or tokens appear only in one agent launch environment.
- Gateway change is set by package script, repo bootstrap, extension host, or unknown process.

Sources: [Claude Code env vars](https://code.claude.com/docs/en/env-vars), [Claude Code settings](https://code.claude.com/docs/en/settings)

---

## EAA-008 — Shadow agent config directory

**Surface:** Runtime  
**Evidence:** documented surface  
**Seen in:** no known public campaign yet  
**Related:** EAA-003, EAA-004, EAA-009

An attacker launches an agent with an alternate config/profile directory containing attacker-controlled settings, hooks, plugins, skills, MCP, or state.

```text
agent start with alternate config dir
  -> attacker-controlled profile loads
  -> hooks/plugins/MCP/settings become active
```

Examples:

- Claude Code documents `CLAUDE_CONFIG_DIR` for changing where config is stored.
- A shadow profile can avoid modifying the user’s normal agent directory.

Hunt ideas:

- Agent starts with config/profile directory outside expected user path.
- Alternate config directory was recently created by untrusted parent.
- Shadow profile contains hooks, MCP, plugins, or provider settings.

Sources: [Claude Code env vars](https://code.claude.com/docs/en/env-vars), [Claude Code settings](https://code.claude.com/docs/en/settings)

---

## EAA-009 — Remote plugin or marketplace hot-load

**Surface:** Control Plane  
**Evidence:** documented surface  
**Seen in:** no known public campaign yet  
**Related:** EAA-003, EAA-006, EAA-013

An attacker causes the agent to load a remote plugin, marketplace, or plugin update that brings new hooks, commands, skills, MCP servers, binaries, or monitors.

```text
plugin source added or passed at startup
  -> plugin loads into agent ecosystem
  -> new command/hook/MCP/skill becomes available
```

Examples:

- Claude Code documents plugins, plugin marketplaces, `--plugin-url`, and plugin reload behavior.
- Plugin docs explicitly treat plugins as highly trusted components.

Hunt ideas:

- Agent starts with remote plugin URL or unapproved plugin directory.
- New plugin marketplace appears in config.
- Plugin reload is followed by first-seen hook, MCP, command, monitor, or binary execution.

Sources: [Claude Code plugins](https://code.claude.com/docs/en/plugins), [Claude Code plugin discovery/security](https://code.claude.com/docs/en/discover-plugins)

---

## EAA-010 — MCP dynamic tool mutation or pushed context

**Surface:** Capabilities  
**Evidence:** research  
**Seen in:** MCP rug-pull/tool-poisoning research  
**Related:** EAA-006, EAA-011

A trusted MCP server changes its advertised tools or pushes context after approval, giving the agent new or modified instructions/capabilities mid-session.

```text
trusted MCP server
  -> tool definition changes or context is pushed
  -> agent acts on changed capability/context
```

Examples:

- MCP research demonstrates tool-description injection and post-approval tool definition drift.
- Claude Code documents dynamic MCP behavior and remote/local MCP transports.

Hunt ideas:

- Tool list changes after initial approval.
- New write/network/admin capability appears mid-session.
- MCP-originated content precedes an agent action without matching user request.

Sources: [MCP injection experiments](https://github.com/invariantlabs-ai/mcp-injection-experiments), [Trail of Bits MCP line-jumping](https://blog.trailofbits.com/2025/04/21/jumping-the-line-how-mcp-servers-can-attack-you-before-you-ever-use-them/), [Claude Code MCP docs](https://code.claude.com/docs/en/mcp)

---

## EAA-011 — Environment-expanded MCP activation

**Surface:** Capabilities  
**Evidence:** documented surface  
**Seen in:** no known public campaign yet  
**Related:** EAA-006, EAA-007

An MCP config uses environment-variable expansion so repo or project content resolves differently on the victim machine.

```text
project MCP config
  -> env-expanded command/url/header/token
  -> victim-specific MCP capability activates
```

Examples:

- Claude Code documents project MCP configuration and env expansion in MCP command, args, env, URL, and headers.
- This can make a repo-shipped config look inert until run in a credentialed developer environment.

Hunt ideas:

- Project MCP config references sensitive or unusual env vars.
- Expanded command or URL differs from the literal checked-in file.
- MCP activation follows a repo checkout, install, or setup step.

Sources: [Claude Code MCP docs](https://code.claude.com/docs/en/mcp)

---

## EAA-012 — Observability/logging exfiltration

**Surface:** State & Telemetry  
**Evidence:** documented surface  
**Seen in:** no known public campaign yet  
**Related:** EAA-005, EAA-007

An attacker changes telemetry or logging settings so prompts, tool content, raw API bodies, or session metadata are sent to an unapproved collector.

```text
telemetry env/config changed
  -> agent logs raw prompts/tool content
  -> collector receives sensitive data
```

Examples:

- Claude Code documents OpenTelemetry-related settings and warns that raw API bodies/tool content/user prompts may contain sensitive data.

Hunt ideas:

- `OTEL_*` collector endpoint points outside approved domains.
- Raw API bodies, tool content, or user prompt logging is enabled unexpectedly.
- Telemetry change is scoped only to agent process launch.

Sources: [Claude Code env vars](https://code.claude.com/docs/en/env-vars)

---

## EAA-013 — Cloud-synced skill drift

**Surface:** Control Plane  
**Evidence:** documented surface  
**Seen in:** no known public campaign yet  
**Related:** EAA-004, EAA-009

Agent behavior changes because cloud-enabled skills or similar remote components sync into the local agent environment outside normal endpoint package review.

```text
cloud skill enabled/updated
  -> local skill sync
  -> agent loads new instructions/tools
```

Examples:

- Claude Code documents local skill sync behavior controlled by environment variables.
- The risk is drift: local agent capability changes without a package install, repo diff, or explicit endpoint deployment.

Hunt ideas:

- First-seen skill files appear under agent skill directories.
- Skill sync is followed by new tool calls, hook execution, or changed agent behavior.
- Skill content includes network, credential, filesystem, or instruction-override patterns.

Sources: [Claude Code env vars](https://code.claude.com/docs/en/env-vars), [Claude Code plugins](https://code.claude.com/docs/en/plugins)

---

## EAA-014 — Multi-agent config fan-out

**Surface:** Control Plane  
**Evidence:** observed  
**Seen in:** Miasma, Hades, Immobiliare Labs Backstage plugins  
**Related:** EAA-003, EAA-004, EAA-006

A payload writes persistence or instructions across many local agent ecosystems at once, increasing the chance that one will execute or load the attacker’s content.

```text
malicious package/repo
  -> writes Claude/Cursor/Gemini/Codex/Kiro/etc config
  -> whichever agent user opens later activates payload
```

Examples:

- Miasma targeted Claude, Gemini, Cursor, and VS Code-style surfaces.
- Hades traversed workspaces looking for many assistant/rule/config surfaces.
- The Immobiliare Labs Backstage plugin campaign targeted multiple AI assistant config ecosystems.

Hunt ideas:

- One process writes several agent config/rule directories within a short window.
- Same payload string appears across multiple assistant config formats.
- Writes occur during package install, repo setup, or IDE extension activation.

Sources: [StepSecurity Miasma](https://www.stepsecurity.io/blog/miasma-worm-hits-microsoft-again-azure-functions-action-and-72-other-repositories-disabled-after-supply-chain-attack-targeting-ai-coding-agents), [StepSecurity Hades](https://www.stepsecurity.io/blog/the-hades-campaign-pypi-packages), [StepSecurity Binding.gyp report](https://www.stepsecurity.io/blog/binding-gyp-npm-supply-chain-attack-spreads-like-worm)

---

## EAA-015 — Inherited authority abuse

**Surface:** Inherited Authority  
**Evidence:** observed  
**Seen in:** Nx s1ngularity, Trivy OpenVSX extension  
**Related:** EAA-001, EAA-002, EAA-006

An attacker uses the agent’s access to local shell, filesystem, authenticated CLIs, browser/session state, MCP servers, or SaaS/cloud tools.

```text
agent session
  -> authenticated local tool or MCP
  -> GitHub/Slack/cloud/package/browser action
```

Examples:

- The Trivy extension attempted to use local agents and authenticated GitHub tooling as part of its collection/exfiltration path.
- Nx used agents for local semantic discovery, then conventional malware handled collection/exfiltration.

Hunt ideas:

- Agent process or descendant invokes `gh`, cloud CLIs, package managers, browser automation, or Slack/GitHub MCP.
- Agent action uses existing logged-in identity rather than attacker-supplied credentials.
- SaaS/cloud audit event correlates to an unusual local agent session.

Sources: [Aqua Trivy advisory](https://github.com/aquasecurity/trivy-vscode-extension/security/advisories/GHSA-8mr6-gf9x-j8qg), [Socket Trivy write-up](https://socket.dev/blog/unauthorized-ai-agent-execution-code-published-to-openvsx-in-aqua-trivy-vs-code-extension), [Nx postmortem](https://nx.dev/blog/s1ngularity-postmortem)

---

## EAA-016 — Agent config and permission reconnaissance

**Surface:** Inherited Authority  
**Evidence:** observed  
**Seen in:** Nx s1ngularity, Trivy OpenVSX extension, Miasma/Hades-style payloads  
**Related:** EAA-001, EAA-006, EAA-015

An attacker enumerates installed agents, configs, MCP servers, skills, hooks, permissions, transcripts, or connected tools to choose the best abuse path.

```text
malware/package/extension
  -> enumerate agent installs and config
  -> choose available agent/tools
  -> invoke, poison, or collect
```

Examples:

- Nx malware discovered local AI agents before deciding how to use them.
- Trivy extension code attempted multiple local agent families.
- Miasma/Hades-style payloads show broad targeting of local assistant surfaces.

Hunt ideas:

- Non-agent process lists known agent config directories across many vendors.
- Process checks for multiple agent binaries in quick succession.
- Recon is followed by agent launch, config write, or state collection.

Sources: [Snyk Nx analysis](https://snyk.io/blog/weaponizing-ai-coding-agents-for-malware-in-the-nx-malicious-package/), [Aqua Trivy advisory](https://github.com/aquasecurity/trivy-vscode-extension/security/advisories/GHSA-8mr6-gf9x-j8qg), [StepSecurity Miasma](https://www.stepsecurity.io/blog/miasma-worm-hits-microsoft-again-azure-functions-action-and-72-other-repositories-disabled-after-supply-chain-attack-targeting-ai-coding-agents), [StepSecurity Hades](https://www.stepsecurity.io/blog/the-hades-campaign-pypi-packages)
