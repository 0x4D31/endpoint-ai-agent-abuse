# Techniques

This is the main catalog. Each technique records a primary surface, tactics, maturity, evidence-source categories, a short abuse path, examples, hunting notes, and sources. Structured evidence assigns confidence to individual source-to-claim assertions rather than to the technique as a whole.

Maturity describes the strongest public anchor for the mechanism as scoped. It does not imply that every cited artifact executed successfully or produced confirmed impact. In particular, a planted project configuration is not proof that a product loaded it: workspace trust, local approval, product version, execution mode, and configuration scope can all be activation gates.

Surfaces are defined in [`../surfaces.md`](../surfaces.md). Evidence labels are defined in [`../evidence.md`](../evidence.md).

## EAA-001 — Agent CLI invocation by adversary-controlled initiator

- **Surface:** Launcher
- **Tactics:** Execution
- **Maturity:** demonstrated
- **Evidence sources:** primary-artifact, incident-report, secondary-analysis
- **Seen in:** Nx s1ngularity, Trivy OpenVSX extension
- **Related:** EAA-002, EAA-015, EAA-016

Malware, package scripts, extensions, repository bootstrap code, or CI jobs launch an installed local AI agent and submit attacker-chosen instructions. Invocation is the observable action; it does not by itself prove that the agent completed the requested action or that downstream impact occurred.

```text
adversary-controlled initiator
  -> local agent CLI
  -> attacker-chosen instructions
  -> agent session and possible tool attempts
```

Examples:

- Nx malware enumerated local AI agents and submitted prompts for semantic filesystem reconnaissance.
- A malicious Trivy OpenVSX extension build contained logic to launch multiple local agents. Public reporting establishes the attempted agent use, but not successful agent-driven impact on every installation.

Hunt ideas:

- Package manager, installer, IDE extension host, repository setup script, or CI job starts an agent binary.
- Agent process has no TTY, runs detached, or starts outside normal interactive shell ancestry.
- Agent activity is followed by sensitive file reads, archiving, upload, or authenticated SaaS/cloud actions.

Sources: [Nx postmortem](https://nx.dev/blog/s1ngularity-postmortem), [Snyk Nx analysis](https://snyk.io/blog/weaponizing-ai-coding-agents-for-malware-in-the-nx-malicious-package/), [Aqua Trivy advisory](https://github.com/aquasecurity/trivy-vscode-extension/security/advisories/GHSA-8mr6-gf9x-j8qg), [Socket Trivy write-up](https://socket.dev/blog/unauthorized-ai-agent-execution-code-published-to-openvsx-in-aqua-trivy-vs-code-extension)

---

## EAA-002 — Permissive or unattended agent execution

- **Surface:** Launcher
- **Tactics:** Execution
- **Maturity:** demonstrated
- **Evidence sources:** primary-artifact, reproducible-research, secondary-analysis
- **Seen in:** Nx s1ngularity and Trivy attempted paths; Claude Code trust-bypass advisory; Dash Remote Control research
- **Related:** EAA-001, EAA-015

An attacker starts a local agent in a non-interactive mode, or uses flags or settings that reduce approval prompts, sandboxing, or trust checks. Unattended operation and permission bypass are distinct behaviors and should be recorded separately in procedure-level data.

```text
untrusted parent
  -> agent with approval-bypass / trust-all / sandbox-disabled mode
  -> agent executes tools with fewer interruptions
```

Examples:

- The Nx postinstall payload checked for local Claude Code, Gemini CLI, and Amazon Q binaries and invoked those it found with permissive and non-interactive flags. Public evidence establishes the attempt, not successful agent output on every affected host.
- The Trivy extension attempted multiple agents with permissive or non-interactive execution modes.
- In Claude Code versions before 2.1.53, a repository-controlled `permissions.defaultMode` value could set `bypassPermissions` before the workspace trust decision and suppress the trust dialog. This historical behavior was patched and should not be generalized to current versions.

Hunt ideas:

- Agent command line includes product- and version-specific approval-bypass, trust-all, sandbox-disabled, yolo, or similar flags.
- No TTY plus permissive flags.
- Permissive agent start from package lifecycle, extension host, or repo automation.

Sources: [Snyk Nx analysis](https://snyk.io/blog/weaponizing-ai-coding-agents-for-malware-in-the-nx-malicious-package/), [Socket Trivy write-up](https://socket.dev/blog/unauthorized-ai-agent-execution-code-published-to-openvsx-in-aqua-trivy-vs-code-extension), [Anthropic advisory GHSA-mmgp-wc2j-qcv7](https://github.com/anthropics/claude-code/security/advisories/GHSA-mmgp-wc2j-qcv7), [Dash Remote Control research](https://dash.security/blog/living-off-coding-agents-claude-as-a-c2-server)

---

## EAA-003 — Lifecycle hook planting

- **Surface:** Control Plane
- **Tactics:** Execution, Persistence
- **Maturity:** observed
- **Evidence sources:** official-documentation, reproducible-research, incident-report
- **Seen in:** Mini Shai-Hulud, Miasma, Immobiliare Labs; Cisco, Mitiga, and Check Point research
- **Related:** EAA-004, EAA-008, EAA-009, EAA-014

An attacker writes agent hook configuration intended to run attacker-controlled commands during session start, tool use, stop, or another lifecycle event. The scoped action is planting the hook, not the hook's later execution. Incident-confirmed planting therefore supports `observed`; execution still depends on the product, version, configuration scope, event, and applicable trust or approval state.

```text
malicious package/repo/extension
  -> writes agent hook config
  -> trust/approval and event conditions are satisfied
  -> hook launches attacker code
```

Examples:

- Mini Shai-Hulud planted project-scoped Claude Code `SessionStart` hooks in repositories it could modify. As with other project configuration, execution depends on the affected product version and trust state.
- Miasma planted project-scoped Claude and Gemini startup hooks. The malicious files establish planting; activation must be evaluated against the affected product version and workspace trust state.
- Current Gemini CLI documentation includes `SessionStart` and other lifecycle hook events. That establishes the product surface as verified on 2026-07-09; it does not establish that a Miasma-planted file activated on a victim or matched every historical Gemini CLI version.
- Current Codex documentation also defines `SessionStart` and other lifecycle hooks in user and project configuration. Project-local hooks load only for a trusted `.codex` layer, and non-managed command hooks require review and hash-bound trust; this documents a gated surface, not malicious use.
- This technique's `observed` maturity means that hook configuration was planted in real compromises. It does not claim that every planted hook fired.

Hunt ideas:

- Writes to agent hook files by package managers, extension hosts, repo scripts, or unknown processes.
- Hook command points to shell, package manager, network fetch, opaque script, or recently written binary.
- A configured hook fires before or immediately after an agent session starts; correlate the configuration write, trust decision, session start, and child process rather than treating file presence alone as execution.

Sources: [StepSecurity Mini Shai-Hulud](https://www.stepsecurity.io/blog/a-mini-shai-hulud-has-appeared), [StepSecurity Miasma](https://www.stepsecurity.io/blog/miasma-worm-hits-microsoft-again-azure-functions-action-and-72-other-repositories-disabled-after-supply-chain-attack-targeting-ai-coding-agents), [StepSecurity Miasma Phantom Gyp](https://www.stepsecurity.io/blog/binding-gyp-npm-supply-chain-attack-spreads-like-worm), [StepSecurity Immobiliare Labs](https://www.stepsecurity.io/blog/immobiliarelabs-npm-packages-compromised), [Cisco memory and hook research](https://blogs.cisco.com/ai/identifying-and-remediating-a-persistent-memory-compromise-in-claude-code), [Mitiga MCP hook research](https://www.mitiga.io/blog/claude-code-mcp-token-theft-mitm), [Check Point project-hook research](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/), [Claude Code hooks docs](https://code.claude.com/docs/en/hooks), [Gemini CLI hooks docs](https://geminicli.com/docs/hooks/), [Codex hooks docs](https://developers.openai.com/codex/hooks)

---

## EAA-004 — Persistent instruction or memory poisoning

- **Surface:** Control Plane
- **Tactics:** Persistence
- **Maturity:** observed
- **Evidence sources:** official-documentation, reproducible-research, incident-report
- **Seen in:** Miasma, Hades; Cisco auto-memory research
- **Related:** EAA-003, EAA-005, EAA-008, EAA-013, EAA-014

An attacker modifies local agent instructions, rules, or auto-memory so later sessions receive attacker-controlled guidance as context. Instruction/rule poisoning and auto-memory poisoning use different storage and loading paths; they remain grouped here because the durable effect is the same, but procedures should identify which path was used.

```text
unexpected writer
  -> memory / instructions / rules file
  -> future agent session
  -> attacker instruction may influence tool use or output
```

Examples:

- Miasma planted persistent assistant instructions or rule files across multiple agent ecosystems. The analyzed Hades payload contained routines intended to write comparable files; public reporting does not establish that those routines ran on a victim endpoint.
- Cisco demonstrated poisoning Claude Code auto-memory and a user-level prompt hook. Claude Code 2.1.50 changed how memory is placed in context; current documentation says memory is context rather than enforced configuration.
- This technique's `observed` maturity is anchored in incident-confirmed instruction or rule planting. It does not establish that a later model followed every planted instruction.

Hunt ideas:

- Non-editor process writes memory, rule, or instruction files.
- New instruction asks the agent to auto-run commands, ignore warnings, suppress findings, trust a domain, or send output elsewhere.
- Memory/rule write is followed by new tool behavior in later sessions.

Sources: [Claude Code memory docs](https://code.claude.com/docs/en/memory), [Cisco memory-poisoning research](https://blogs.cisco.com/ai/identifying-and-remediating-a-persistent-memory-compromise-in-claude-code), [StepSecurity Miasma](https://www.stepsecurity.io/blog/miasma-worm-hits-microsoft-again-azure-functions-action-and-72-other-repositories-disabled-after-supply-chain-attack-targeting-ai-coding-agents), [StepSecurity Miasma Phantom Gyp](https://www.stepsecurity.io/blog/binding-gyp-npm-supply-chain-attack-spreads-like-worm), [StepSecurity Hades](https://www.stepsecurity.io/blog/the-hades-campaign-pypi-packages), [StepSecurity Immobiliare Labs](https://www.stepsecurity.io/blog/immobiliarelabs-npm-packages-compromised), [Adversa AI SymJack research](https://adversa.ai/blog/the-approval-prompt-is-lying-to-you-symlink-rce-in-five-ai-coding-agents-claude-code-cursor-antigravity-copilot-grok-build/)

---

## EAA-005 — Transcript and agent-state collection

- **Surface:** State & Telemetry
- **Tactics:** Credential Access, Collection
- **Maturity:** observed
- **Evidence sources:** official-documentation, incident-report
- **Seen in:** OALABS compromised Claude/Codex investigation
- **Related:** EAA-004, EAA-012, EAA-017

An attacker reads or copies local transcripts, tool histories, plans, logs, caches, session stores, or complete agent profiles to recover credentials, tokens, secrets, internal context, repository details, identity material, or operational history. Credential Access applies only when authentication material is actually among the collected state.

```text
attacker or attacker-directed agent
  -> bulk reads agent state
  -> archives or filters content
  -> exfiltrates useful context/secrets
```

Examples:

- In the OALABS investigation, a compromised Claude installation and its session history were copied to attacker-controlled systems and reused. The researchers also found other archived copies of stolen Claude instances.
- Claude Code documentation confirms that an alternate configuration directory contains session history and, on Linux and Windows, credentials; macOS credentials remain in the system Keychain.
- Claude Code stores project transcripts as JSONL under `~/.claude/projects/<project>/`, with retention and non-persistence controls that affect artifact availability. This documents the local surface, not malicious collection.
- Codex stores local history under `CODEX_HOME` (for example, `~/.codex/history.jsonl`) when history persistence is enabled; `history.persistence = "none"` disables future local-history persistence and `history.max_bytes` can remove older entries. These are legitimate privacy and retention controls as well as forensic coverage conditions.

Hunt ideas:

- Any unexpected process, including the agent itself or one of its descendants, recursively reads transcript/history/cache directories.
- Bulk state reads followed by zip/tar/base64/curl/gh/cloud upload.
- Agent configuration and session state are copied together or appear on a new host.

Sources: [OALABS compromised Claude/Codex investigation](https://research.openanalysis.net/claude/codex/hacking/ai%20hacking/llm/redteam/policy%20violation/2026/06/16/compromised-claude-hacking.html), [Claude Code environment variables](https://code.claude.com/docs/en/env-vars), [Claude Code memory docs](https://code.claude.com/docs/en/memory), [Claude Code sessions docs](https://code.claude.com/docs/en/sessions), [Claude Code directory docs](https://code.claude.com/docs/en/claude-directory), [Codex advanced configuration](https://developers.openai.com/codex/config-advanced/)

---

## EAA-006 — MCP or tool configuration abuse

- **Surface:** Tools & Integrations
- **Tactics:** Execution, Persistence
- **Maturity:** demonstrated
- **Evidence sources:** official-documentation, reproducible-research
- **Seen in:** historical Claude Code MCP approval-bypass research; Mitiga MCP endpoint-rewrite research
- **Related:** EAA-009, EAA-010, EAA-011, EAA-014, EAA-015, EAA-016

An attacker adds or modifies local MCP or tool configuration so the agent connects to an attacker-selected server or gains a new filesystem, shell, browser, SaaS, or network capability. Project-scoped MCP definitions normally require product-specific trust or server approval; configuration presence alone is not proof of activation.

```text
malicious config write
  -> new MCP/tool capability
  -> applicable trust/approval gate is satisfied
  -> capability becomes available for agent use
```

Examples:

- Check Point demonstrated that older Claude Code versions could use repository-controlled settings to approve and start a project MCP server before the trust decision. The bypass was patched before public disclosure.
- Mitiga demonstrated same-user code rewriting an existing MCP endpoint and using a lifecycle hook to reassert the change. The proof of concept required prior local execution and a compatible OAuth-backed MCP server.
- Gemini CLI documents an MCP server `trust: true` setting that bypasses all tool-call confirmations for that server. It is an explicit high-risk configuration primitive, not evidence of a product vulnerability or malicious use.
- Poisoning the content of an already connected server's tool definitions is tracked separately in EAA-010.

Hunt ideas:

- New MCP server or tool config from an untrusted writer.
- Stdio MCP command uses shell, package manager, network fetch, or unpinned package execution.
- Capability appears shortly before sensitive file, browser, GitHub, Slack, or cloud activity.

Sources: [Claude Code MCP docs](https://code.claude.com/docs/en/mcp), [Check Point Claude Code project-configuration research](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/), [Mitiga MCP endpoint-rewrite research](https://www.mitiga.io/blog/claude-code-mcp-token-theft-mitm), [Adversa AI SymJack research](https://adversa.ai/blog/the-approval-prompt-is-lying-to-you-symlink-rce-in-five-ai-coding-agents-claude-code-cursor-antigravity-copilot-grok-build/), [Gemini CLI MCP server docs](https://geminicli.com/docs/tools/mcp-server/)

---

## EAA-007 — Hostile model/API gateway routing

- **Surface:** Runtime & Environment
- **Tactics:** Collection, Exfiltration
- **Maturity:** demonstrated
- **Evidence sources:** official-documentation, reproducible-research
- **Seen in:** historical Claude Code `ANTHROPIC_BASE_URL` research
- **Related:** EAA-008, EAA-011, EAA-012

An attacker changes provider routing so a trusted local agent talks to an attacker-controlled or unapproved model/API gateway.

```text
changed env/config
  -> agent connects to attacker gateway
  -> prompts/tool context exposed or responses steered
```

Examples:

- Check Point demonstrated that an older Claude Code version accepted a repository-controlled `ANTHROPIC_BASE_URL` early enough to expose authorization headers and startup API traffic to an attacker-controlled proxy. Anthropic patched the reported path before public disclosure.
- Claude Code documents legitimate custom gateways and provider routing. Product, provider, authentication mode, and version determine which credentials and content traverse a gateway; do not assume a single behavior across agents.
- Codex documents `openai_base_url` and custom model providers with `base_url` and `env_key`. Gemini CLI documents `GOOGLE_GEMINI_BASE_URL` for API-key authentication and `GOOGLE_VERTEX_BASE_URL` for Vertex AI authentication. Codex project-scoped `.codex/config.toml` files cannot override provider-routing keys, so the effective configuration scope is part of the activation condition.

Hunt ideas:

- Provider base URL points outside approved domains.
- Custom auth headers or tokens appear only in one agent launch environment.
- Gateway change is set by package script, repo bootstrap, extension host, or unknown process.

Sources: [Claude Code environment variables](https://code.claude.com/docs/en/env-vars), [Claude Code settings](https://code.claude.com/docs/en/settings), [Check Point Claude Code project-configuration research](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/), [Codex configuration reference](https://developers.openai.com/codex/config-reference/), [Gemini CLI configuration reference](https://geminicli.com/docs/reference/configuration/)

---

## EAA-008 — Shadow agent profile or config directory

- **Surface:** Runtime & Environment
- **Tactics:** Execution, Defense Evasion
- **Maturity:** demonstrated
- **Evidence sources:** official-documentation, reproducible-research
- **Seen in:** Dash Security Claude Remote Control research
- **Related:** EAA-003, EAA-004, EAA-007, EAA-009

An attacker launches an agent with an alternate profile or configuration directory containing attacker-controlled settings, state, trust decisions, plugins, or credentials. Exactly which assets move with an alternate directory is product- and platform-specific.

```text
agent start with alternate profile/config directory
  -> attacker-controlled state is selected
  -> profile settings and available components influence the session
```

Examples:

- Claude Code documents that `CLAUDE_CONFIG_DIR` relocates settings, session history, and plugins, as well as credentials on Linux and Windows. Credentials remain in the system Keychain on macOS.
- Codex documents `CODEX_HOME` as the root for its configuration, authentication, logs, sessions, and skills. Gemini CLI documents `GEMINI_CLI_HOME` as the root for its user-level configuration and storage. These product roots are not interchangeable with a path that overrides only one settings file.
- Dash Security demonstrated an isolated Claude configuration directory with seeded workspace trust and an attacker-controlled, full-scope Claude.ai login as part of a Remote Control C2 proof of concept. The proof of concept required valid account material and did not bypass the full-scope requirement.

Hunt ideas:

- Agent starts with config/profile directory outside expected user path.
- Alternate config directory was recently created by untrusted parent.
- Shadow profile contains seeded trust state, unexpected authentication material, plugins, hooks, or provider settings.

Sources: [Claude Code environment variables](https://code.claude.com/docs/en/env-vars), [Claude Code settings](https://code.claude.com/docs/en/settings), [Dash Security Claude Remote Control research](https://dash.security/blog/living-off-coding-agents-claude-as-a-c2-server), [Codex environment variables](https://developers.openai.com/codex/environment-variables/), [Gemini CLI configuration reference](https://geminicli.com/docs/reference/configuration/)

---

## EAA-009 — Remote plugin sideload or marketplace installation

- **Surface:** Control Plane
- **Tactics:** Execution, Persistence
- **Maturity:** feasible
- **Evidence sources:** official-documentation
- **Seen in:** no known public malicious use as of 2026-07-09
- **Related:** EAA-003, EAA-006, EAA-008, EAA-013

An attacker causes the agent to sideload a remote plugin archive or install or update a plugin from an attacker-controlled marketplace. Plugins can bring hooks, commands, skills, MCP servers, binaries, monitors, or other executable behavior.

```text
remote archive passed at startup or marketplace plugin installed
  -> plugin is loaded for one or later sessions
  -> new command/hook/MCP/skill becomes available
```

Examples:

- Claude Code fetches `--plugin-url` archives at startup and loads them for that session only.
- Marketplace registration, plugin installation, enablement, and update are separate state changes. Adding a marketplace alone does not establish that a plugin was installed or loaded.
- Managed policy can constrain plugin and marketplace sources. Claude Code 2.1.193 and later documents managed-only `disableSideloadFlags`, which rejects `--plugin-dir`, `--plugin-url`, `--agents`, and `--mcp-config`; applicable policy and product version are activation conditions.

Hunt ideas:

- Agent starts with remote plugin URL or unapproved plugin directory.
- New plugin marketplace appears in config, followed by installation or enablement of a plugin from that source.
- Plugin reload is followed by first-seen hook, MCP, command, monitor, or binary execution.

Sources: [Claude Code plugins](https://code.claude.com/docs/en/plugins), [Claude Code plugins reference](https://code.claude.com/docs/en/plugins-reference), [Claude Code plugin discovery and security](https://code.claude.com/docs/en/discover-plugins), [Claude Code settings](https://code.claude.com/docs/en/settings)

---

## EAA-010 — MCP tool poisoning or definition drift

- **Surface:** Tools & Integrations
- **Tactics:** Execution, Collection, Exfiltration
- **Maturity:** demonstrated
- **Evidence sources:** official-documentation, primary-artifact, reproducible-research
- **Seen in:** MCP rug-pull/tool-poisoning research
- **Related:** EAA-006, EAA-011

An MCP server embeds adversarial instructions in tool metadata or changes an advertised tool definition after an earlier benign presentation. This can steer the agent before a tool is selected, shadow another server's tool, or change how a capability is understood later.

```text
connected MCP server
  -> poisoned or changed tool metadata reaches the model
  -> agent may select or use a capability under attacker influence
```

Examples:

- Trail of Bits demonstrated that instructions in MCP tool descriptions can influence an agent before the user invokes the malicious tool.
- Invariant Labs published reproducible examples of direct tool poisoning, cross-server tool shadowing, and a sleeper server that presents a malicious interface on a later load.
- Claude Code supports MCP `list_changed` notifications and automatically refreshes advertised tools, prompts, and resources. The documentation proves live mutation is supported; it does not by itself demonstrate malicious use of that live path.

Hunt ideas:

- Tool metadata or the tool list changes after its first observation or approval.
- New write/network/admin capability appears mid-session.
- MCP tool metadata precedes an agent action without a matching user request or expected tool selection.

Sources: [MCP injection experiments](https://github.com/invariantlabs-ai/mcp-injection-experiments), [Trail of Bits MCP line-jumping](https://blog.trailofbits.com/2025/04/21/jumping-the-line-how-mcp-servers-can-attack-you-before-you-ever-use-them/), [Claude Code MCP docs](https://code.claude.com/docs/en/mcp)

---

## EAA-011 — Environment-variable manipulation of MCP activation

- **Surface:** Tools & Integrations
- **Tactics:** Execution
- **Maturity:** feasible
- **Evidence sources:** official-documentation
- **Seen in:** no known public malicious use as of 2026-07-09
- **Related:** EAA-006, EAA-007, EAA-010

An attacker who can influence the agent's effective launch environment sets or replaces a variable referenced by an MCP configuration, causing its command, arguments, environment, URL, or headers to resolve to an attacker-selected value. Required control is the ability to modify the relevant environment-variable source; environment expansion and a checked-in placeholder are not malicious by themselves. The server still faces the normal scope-specific trust and approval gates.

```text
attacker controls a referenced launch-environment value
  -> MCP command/url/header resolves differently
  -> normal trust/approval gate is satisfied
  -> attacker-selected MCP endpoint or executable activates
```

Examples:

- Claude Code documents project MCP configuration and env expansion in MCP command, args, env, URL, and headers.
- If an attacker already controls a referenced environment value, a repository-shipped config can resolve to an attacker-selected executable, endpoint, or credential-bearing header. If a required variable is unset and has no default, Claude Code fails to parse the configuration rather than activating it.

Hunt ideas:

- Project MCP config references sensitive or unusual env vars.
- The process environment supplies a referenced value from an unexpected parent, shell startup file, service definition, CI variable, or wrapper.
- Expanded command or URL differs from the literal checked-in file.
- MCP activation follows a repo checkout, install, or setup step.

Sources: [Claude Code MCP docs](https://code.claude.com/docs/en/mcp)

---

## EAA-012 — Telemetry redirection or sensitive logging

- **Surface:** State & Telemetry
- **Tactics:** Execution, Collection, Exfiltration
- **Maturity:** demonstrated
- **Evidence sources:** official-documentation, reproducible-research
- **Seen in:** Bloom Security OTel research
- **Related:** EAA-005, EAA-007, EAA-017

An attacker changes telemetry or logging settings so session metadata or explicitly enabled sensitive content is written locally or sent to an unapproved collector. Where supported, an executable telemetry-header helper can also become a command-execution surface.

```text
exporter and content-bearing telemetry settings changed
  -> agent emits selected sensitive fields
  -> collector receives sensitive data
```

Examples:

- Claude Code telemetry export is opt-in. Prompt text, assistant responses, tool details/content, and raw API bodies are redacted or disabled by default and require separate content-bearing settings.
- Claude Code's `otelHeadersHelper` is an executable command that runs at startup and periodically for HTTP-based exporters.
- Gemini CLI telemetry is disabled by default. When telemetry is enabled, its documented prompt-logging setting defaults to true and an OTLP endpoint can redirect export; defenders must therefore evaluate the effective combination, not a single flag in isolation.
- Codex exposes configurable OpenTelemetry exporters and opt-in `otel.log_user_prompt`, but project-scoped `.codex/config.toml` cannot override telemetry settings. This narrows repository-only abuse and makes configuration provenance important.
- Bloom Security demonstrated repository-controlled OTel redirection, sensitive-content settings, and header-helper execution. Treat the reported trust behavior as version-specific and reproduce it against the affected version before applying it to current releases.

Hunt ideas:

- `OTEL_*` collector endpoint points outside approved domains.
- Prompt/response text, tool details/content, or raw API-body logging is enabled unexpectedly.
- `otelHeadersHelper` changes or points to an unapproved executable or shell command.
- Telemetry change is scoped only to agent process launch.

Sources: [Claude Code monitoring docs](https://code.claude.com/docs/en/monitoring-usage), [Claude Code settings](https://code.claude.com/docs/en/settings), [Bloom Security OTel research](https://bloom.security/blog/welcome-to-otel-claudeifornia), [Codex configuration reference](https://developers.openai.com/codex/config-reference/), [Gemini CLI OpenTelemetry docs](https://geminicli.com/docs/cli/telemetry/)

---

## EAA-013 — Cloud-hosted skill poisoning and sync

- **Surface:** Control Plane
- **Tactics:** Execution, Persistence
- **Maturity:** feasible
- **Evidence sources:** official-documentation
- **Seen in:** no known public malicious use of cloud skill sync as of 2026-07-09
- **Related:** EAA-004, EAA-009

An attacker with permission or account-level access to modify an already enabled cloud-hosted skill changes its instructions or dynamic context, and the product later syncs that content into the local agent environment. Required control is the ability to modify the cloud skill or the victim account's enabled-skill state; synchronization by itself is benign. The sync path is delivery, and skill invocation is the activation condition that places the changed content in context.

```text
attacker modifies an enabled cloud-hosted skill
  -> local skill sync
  -> available skill content changes
  -> instructions enter context if the skill is invoked
```

Examples:

- Claude Code documents `CLAUDE_CODE_SYNC_SKILLS=1` for authenticated, non-interactive `-p` sessions. It downloads enabled claude.ai skills before the first query and resyncs every 10 minutes; claude.ai web sessions receive enabled skills automatically.
- Skills provide instructions and can include dynamic context commands or `allowed-tools`. Project-scope permission grants take effect only after workspace trust, but cloud/user skill provenance follows a different path.
- Public documentation establishes the sync and skill-execution surfaces, but the catalog has no public malicious implementation. The entry therefore remains `feasible` and does not assert a product-side trust bypass.

Hunt ideas:

- First-seen skill files appear under agent skill directories.
- Cloud audit, account, or skill-version history shows an unexpected editor or enablement change, where that telemetry is available.
- Skill sync is followed by new tool calls, hook execution, or changed agent behavior.
- Skill content includes network, credential, filesystem, or instruction-override patterns.

Sources: [Claude Code environment variables](https://code.claude.com/docs/en/env-vars), [Claude Code skills](https://code.claude.com/docs/en/skills)

---

## EAA-014 — Cross-agent control-plane fan-out planting

- **Surface:** Control Plane
- **Tactics:** Persistence
- **Maturity:** observed
- **Evidence sources:** incident-report
- **Seen in:** Miasma, Hades, Immobiliare Labs Backstage plugins
- **Related:** EAA-003, EAA-004, EAA-006

An attacker-controlled process writes equivalent hook, instruction, rule, skill, or tool-configuration artifacts for two or more local agent ecosystems during one fan-out operation. The atomic action is the multi-ecosystem write. Procedure records should also map the underlying hook, instruction, skill, or tool-configuration technique and separately record whether any product later activated the planted content.

```text
one attacker-controlled process
  -> writes control-plane artifacts for two or more agent ecosystems
  -> one or more compatible agents may later load the content
```

Examples:

- Miasma targeted Claude, Gemini, Cursor, and VS Code-style surfaces.
- The analyzed Hades payload contained workspace-traversal and multi-product planting logic; public reporting establishes the code path, not victim-side traversal or writes.
- Compromised Immobiliare Labs Backstage packages contained persistence routines targeting multiple AI assistant configuration ecosystems.
- This technique's `observed` maturity means that real malicious operations planted or committed cross-agent artifacts. It does not mean that every targeted agent loaded them.

Hunt ideas:

- One process writes several agent config/rule directories within a short window.
- Same payload string appears across multiple assistant config formats.
- Writes occur during package install, repo setup, or IDE extension activation.

Sources: [StepSecurity Miasma](https://www.stepsecurity.io/blog/miasma-worm-hits-microsoft-again-azure-functions-action-and-72-other-repositories-disabled-after-supply-chain-attack-targeting-ai-coding-agents), [StepSecurity Miasma Phantom Gyp](https://www.stepsecurity.io/blog/binding-gyp-npm-supply-chain-attack-spreads-like-worm), [StepSecurity Hades](https://www.stepsecurity.io/blog/the-hades-campaign-pypi-packages), [StepSecurity Immobiliare Labs report](https://www.stepsecurity.io/blog/immobiliarelabs-npm-packages-compromised)

---

## EAA-015 — Inherited authority abuse

- **Surface:** Identity & Authority
- **Tactics:** Execution, Collection, Exfiltration
- **Maturity:** observed
- **Evidence sources:** reproducible-research, incident-report, secondary-analysis
- **Seen in:** OALABS compromised Claude/Codex investigation; Trivy attempted path; Mitiga and Dash research
- **Related:** EAA-001, EAA-002, EAA-006, EAA-016

An attacker uses the agent's existing access to local shell, filesystem, authenticated CLIs, browser or session state, MCP servers, or SaaS/cloud tools. These authority sources have different audit and revocation semantics and should be identified separately at procedure level.

```text
agent session
  -> authenticated local tool or MCP
  -> GitHub/Slack/cloud/package/browser action
```

Examples:

- The Trivy extension attempted to use local agents and authenticated GitHub tooling as part of its collection/exfiltration path.
- OALABS recovered sessions showing an attacker using local Claude and Codex agents with their available shell, filesystem, and network access to conduct real intrusions and data exfiltration.

Hunt ideas:

- Agent process or descendant invokes `gh`, cloud CLIs, package managers, browser automation, or Slack/GitHub MCP.
- Agent action uses existing logged-in identity rather than attacker-supplied credentials.
- SaaS/cloud audit event correlates to an unusual local agent session.
- Distinguish an agent using delegated authority from direct credential theft; the same downstream service event may otherwise appear to be an ordinary human action.

Sources: [OALABS compromised Claude/Codex investigation](https://research.openanalysis.net/claude/codex/hacking/ai%20hacking/llm/redteam/policy%20violation/2026/06/16/compromised-claude-hacking.html), [Socket Trivy write-up](https://socket.dev/blog/unauthorized-ai-agent-execution-code-published-to-openvsx-in-aqua-trivy-vs-code-extension), [Mitiga MCP authority research](https://www.mitiga.io/blog/claude-code-mcp-token-theft-mitm), [Dash Remote Control research](https://dash.security/blog/living-off-coding-agents-claude-as-a-c2-server)

---

## EAA-016 — Agent environment discovery

- **Surface:** Runtime & Environment
- **Tactics:** Discovery
- **Maturity:** demonstrated
- **Evidence sources:** incident-report, secondary-analysis
- **Seen in:** Nx s1ngularity, Trivy OpenVSX extension, Hades
- **Related:** EAA-001, EAA-006, EAA-015

An attacker enumerates installed agent binaries or agent-related configuration, tools, authority, state, or capabilities to choose a later abuse path. Procedures should distinguish binary discovery from configuration, capability, authority, and state discovery.

```text
malware/package/extension
  -> enumerate agent installs and config
  -> choose available agent/tools
  -> invoke, poison, or collect
```

Examples:

- Nx malware contained and ran post-install logic that checked for local AI-agent CLIs before deciding which invocation paths to attempt. Public reporting does not provide victim runtime evidence showing which specific agent binaries were found.
- Trivy extension code attempted multiple local agent families and supplied prompts that asked about available tools or access.
- The analyzed Hades payload contained directory-tree traversal logic for locating rule files or configuration directories belonging to many agent ecosystems; public reporting does not confirm that traversal on a victim endpoint.
- These inspectable discovery paths establish `demonstrated`. They do not meet the catalog's `observed` threshold because the public cases do not confirm a specific agent binary, configuration, or capability was found on a victim endpoint.

Hunt ideas:

- Non-agent process lists known agent config directories across many vendors.
- Process checks for multiple agent binaries in quick succession.
- Recon is followed by agent launch, config write, or state collection.

Sources: [Snyk Nx analysis](https://snyk.io/blog/weaponizing-ai-coding-agents-for-malware-in-the-nx-malicious-package/), [Socket Trivy write-up](https://socket.dev/blog/unauthorized-ai-agent-execution-code-published-to-openvsx-in-aqua-trivy-vs-code-extension), [StepSecurity Hades](https://www.stepsecurity.io/blog/the-hades-campaign-pypi-packages)

---

## EAA-017 — Agent-native evidence tampering

- **Surface:** State & Telemetry
- **Tactics:** Defense Evasion
- **Maturity:** observed
- **Evidence sources:** official-documentation, incident-report
- **Seen in:** OALABS compromised Claude/Codex investigation
- **Related:** EAA-005, EAA-012

An attacker alters, truncates, replaces, or deletes agent-native transcripts or audit state to conceal prior activity. The attacker may modify the files directly or direct the agent to locate and edit its own records.

```text
attacker or attacker-directed agent
  -> identifies current session evidence
  -> truncates, replaces, or deletes records
  -> native history no longer reflects the full activity
```

Examples:

- In the OALABS investigation, the operator asked Claude to locate the active Claude Code transcript, remove all content after a selected point, and replace the live JSONL file with the truncated copy. The recovered sequence showed both the request and the subsequent file operations.
- Claude Code 2.1.124 and later documents `claude project purge`, which can delete project transcripts, memory, tasks, debug logs, file history, prompt history, and metadata. This is a legitimate privacy operation and a forensic coverage condition; its existence does not imply malicious use. The OALABS incident remains the observed anchor for this technique.

Hunt ideas:

- An agent process or descendant reads and then rewrites, truncates, renames over, or deletes a transcript associated with the current or recent session.
- Transcript size, hashes, event ordering, or sequence identifiers regress or contain gaps while independent process, file, network, or service audit evidence continues.
- A session-history file is replaced from a temporary or working path shortly after sensitive activity.
- Native project-purge invocation or retention changes occur immediately before or after sensitive activity; distinguish authorized privacy deletion from concealment by requiring an independent contradiction.
- Treat a missing record as an evidence-gap signal, not proof of tampering: normal retention, compaction, non-persistent modes, crashes, and delayed flushing can produce gaps too.

Sources: [OALABS compromised Claude/Codex investigation](https://research.openanalysis.net/claude/codex/hacking/ai%20hacking/llm/redteam/policy%20violation/2026/06/16/compromised-claude-hacking.html), [Claude Code directory docs](https://code.claude.com/docs/en/claude-directory)
