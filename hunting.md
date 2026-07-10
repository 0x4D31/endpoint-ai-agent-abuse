# Hunting

These are correlation hypotheses, not production-ready rules. Validate them against pinned agent versions, operating systems, normal developer workflows, and the telemetry actually available in your environment.

For each analytic, record the product/version, enabled controls, required fields, correlation window, benign baselines, and known blind spots. A configuration write is not proof that the configuration loaded; an agent launch is not proof that a requested action completed; and missing agent-native evidence is not proof of tampering.

## H1 — Agent launched by an unexpected initiator

**Techniques:** EAA-001, EAA-002, EAA-016

**Required telemetry:** process start and ancestry, full command line, executable path/signer/hash, user/session, TTY or interactive-session context, container/CI context, and an inventory of expected agent launchers.

Where agent-native fields are available, preserve them as correlation keys. Claude Code documents `session.id`, `prompt.id`, and `tool_use_id`; when tracing is active, Bash and PowerShell subprocesses inherit W3C `TRACEPARENT`. With a custom `ANTHROPIC_BASE_URL`, `CLAUDE_CODE_PROPAGATE_TRACEPARENT=1` enables that propagation path. These identifiers strengthen a temporal/process join but are not cryptographic proof of intent, and tracing plus content-bearing fields are not enabled by default. See the [Claude Code monitoring documentation](https://code.claude.com/docs/en/monitoring-usage).

Look for package managers, installers, IDE extension hosts, repository setup scripts, CI jobs, or document handlers launching a local agent, then require a downstream effect.

```text
unexpected initiator -> agent process -> sensitive read or SaaS/cloud action
```

**Limitations:** shells, task runners, IDEs, wrappers, and CI legitimately launch agents. Parent process alone is weak evidence, and ancestry may be lost across services, containers, or detached processes.

## H2 — Permissive or unattended agent execution

**Techniques:** EAA-002

**Required telemetry:** full command line and process environment, agent product/version, TTY/session context, and a versioned dictionary of permissive flags and equivalent configuration fields.

```text
agent process + permissive setting + no TTY + unexpected initiator
```

**Limitations:** flag names and semantics change. A wrapper can hide arguments, and equivalent behavior may be set in files or managed policy rather than the command line. Non-interactive execution is normal in approved CI automation.

## H3 — Control-plane write followed by activation

**Techniques:** EAA-003, EAA-004, EAA-009, EAA-013, EAA-014

**Required telemetry:** file create/write/rename events with writer provenance, hashes or content diffs, product-specific control-plane path inventory, repository provenance, agent start/reload events, and hook/plugin/tool child-process events.

```text
unexpected writer -> agent control-plane file -> trust/load condition -> agent start/reload -> effect
```

Track project, user, and managed scopes separately. Include hooks, instruction/memory files, rules, plugins, skills, marketplaces, and trust-state files.

**Limitations:** editors, sync clients, installers, and agent self-maintenance legitimately change these files. A write does not prove that the relevant version loaded it or that workspace trust was granted. Content-only sensors may miss atomic rename or replace operations.

## H4 — Transcript and agent-state collection

**Techniques:** EAA-005

**Required telemetry:** product/version-specific state paths, file-read telemetry where available, process identity, read volume and breadth, archive/encoding process activity, and outbound upload or remote-storage events.

```text
bulk or cross-project state read -> archive/filter -> network or remote-storage write
```

Include reads by the agent itself: an operator can ask an agent to find and process its own histories, so a `claude`, `codex`, or similar reader should not be automatically allowlisted.

**Limitations:** file-read telemetry is expensive and often unavailable. Backup, indexing, migration, support, and forensic tools legitimately read state in bulk. Some credentials are stored in OS credential stores rather than the agent directory.

## H5 — Hostile gateway or shadow profile

**Techniques:** EAA-007, EAA-008

**Required telemetry:** process environment variable names and values where policy permits, full command line, effective config/profile path, configuration snapshots, DNS/TLS/network destination, and approved gateway/profile baselines.

```text
base URL / custom header / alternate config directory -> agent start -> first-seen destination or control plane
```

Prefer capturing normalized domains and secret-safe hashes over ingesting raw credential-bearing environment variables.

**Limitations:** enterprise gateways, development proxies, test profiles, and portable installations are legitimate. Effective configuration can come from several precedence layers, and endpoint telemetry may not expose encrypted traffic content or OS credential-store use.

## H6 — Capability or tool-definition drift

**Techniques:** EAA-006, EAA-010, EAA-011

**Required telemetry:** MCP/tool configuration snapshots, effective environment expansion, server command or URL, server identity, tool-list and description snapshots, protocol `list_changed` events when exposed, and tool-call outcomes.

```text
new or changed capability -> agent reload/event -> sensitive tool or network action
```

Differentiate a tool that changed during a live session from one that presented differently on a later connection. Record description-only changes as well as schema and command changes.

**Limitations:** dynamic tool discovery and environment-specific configuration are legitimate. Many clients do not expose complete tool definitions or update events, and a first-seen capability may simply reflect a new project.

## H7 — Observability export to an unapproved collector

**Techniques:** EAA-012

**Required telemetry:** effective agent settings and environment, OpenTelemetry exporter endpoint and headers in secret-safe form, DNS/network flows to collectors, sensitive-content flag state, `otelHeadersHelper` or equivalent helper configuration, and managed-policy precedence.

```text
telemetry enabled or redirected -> sensitive logging option/helper -> unapproved collector connection
```

Alert separately on a new collector, newly enabled sensitive-content options, and a helper command. Sensitive prompt, tool-content, and raw-body options in Claude Code are disabled by default; the risk changes when they are explicitly enabled.

**Limitations:** custom collectors and dynamic header helpers are common enterprise patterns. Telemetry settings are version-sensitive, managed settings can override lower scopes, and collecting raw exported content for detection can create a second privacy problem.

## H8 — Inherited authority abuse

**Techniques:** EAA-015

**Required telemetry:** agent session boundaries, child-process and network activity, authenticated CLI/browser/MCP identity, remote service audit logs, request or correlation IDs where available, and a baseline of approved agent-to-service delegation.

```text
agent session -> authenticated local tool/session -> GitHub/SaaS/cloud/package action
```

Prioritize destructive, administrative, bulk-read, token-management, and public-publishing actions, especially when the preceding user request or repository provenance does not explain them.

**Limitations:** downstream services frequently attribute the action only to the human account. Shared tokens and provider egress obscure origin, and semantic intent may not be recoverable. Treat attribution as confidence-weighted unless independent endpoint and service evidence agree.

## H9 — Agent environment reconnaissance

**Techniques:** EAA-016

**Required telemetry:** process execution, directory and file enumeration where available, command line, product path inventory, and later agent launch, control-plane write, or state-read events.

```text
multi-product enumeration -> agent launch / control-plane write / state collection
```

Look for one process probing many agent binaries, config roots, MCP files, skills, hooks, rules, trust stores, or transcript paths in a short window.

**Limitations:** inventory agents, security scanners, backup software, IDEs, dotfile managers, and migration tools can produce the same enumeration. Require unusual provenance or a later action.

## H10 — Cross-plane evidence gap

**Techniques:** EAA-005, EAA-012, EAA-015, EAA-017

**Required telemetry:** at least one agent-native plane plus an independent endpoint or remote-service plane, clock normalization, known retention/flush behavior, effective persistence/retention configuration, native purge or privacy-deletion invocation where available, and explicit coverage status for both planes.

```text
sensitive endpoint or SaaS effect -> expected agent record absent or incomplete
```

Examples include a remote repository creation, cloud change, or local sensitive write with no matching transcript/tool event, or an agent tool event with no corresponding endpoint effect.

**Limitations:** absence is not evidence of compromise. Crashes, product-specific history-size compaction or retention cleanup, disabled telemetry, authorized privacy deletion, unsupported tools, clock skew, offline operation, and sensor loss all create benign gaps. Emit a coverage or contradiction finding, not a malicious verdict.

## H11 — Agent-native transcript or state anti-forensics

**Techniques:** EAA-005, EAA-017

**Required telemetry:** file write/rename/delete events for session and state paths, file identity/inode where available, size and hash history, active agent session metadata, process ancestry, effective persistence/retention configuration, native purge or privacy-deletion invocation, independent endpoint events, and remote-service audit logs.

Look for an active agent or its descendants locating and then editing its own evidence, especially around sensitive actions.

```text
agent/session activity
  -> enumerate transcript/state paths
  -> truncate, replace, delete, or rewrite live state
  -> sequence/timestamp gap or cross-plane contradiction
```

Useful signals include sudden size regression, atomic replacement of a live transcript, deletion followed by recreation, session IDs that disappear while the process continues, sequence or timestamp discontinuities, and state edits followed by resume of the same session. Preserve an early copy and compare it with filesystem journal, backup, EDR, and remote-service evidence.

Claude Code 2.1.124 and later documents `claude project purge`; Codex documents `history.persistence = "none"` and history-size cleanup. Those legitimate controls can explain missing state, but an invocation or configuration change tightly coupled to sensitive activity is worth correlating with independent telemetry. See [Claude Code application-data documentation](https://code.claude.com/docs/en/claude-directory) and [Codex advanced configuration](https://developers.openai.com/codex/config-advanced/).

**Limitations:** normal history-size compaction, retention cleanup, session reset, application migration, crash recovery, privacy deletion, and user editing can look similar. The agent process may legitimately write its own state. Require timing plus an independent contradiction; do not infer hidden content from the gap.

## H12 — Shadow identity or Remote Control session

**Techniques:** EAA-002, EAA-008, EAA-015

**Required telemetry:** agent command line, config-directory selection, trust/auth state creation, user/session and TTY context, long-lived outbound agent connections, Remote Control administrative policy, and—where available—the owning organization/account identity.

```text
new alternate profile or auth state -> unattended Remote Control start -> remote-directed local effect
```

Prioritize isolated profiles created immediately before launch, pre-seeded workspace trust, background starts without a local interactive session, and agents authenticated to accounts outside the organization's control.

**Limitations:** Remote Control is a legitimate feature and uses expected vendor infrastructure. Endpoint network data may not reveal the controlling account, and legitimate users may create alternate profiles. Account ownership and organizational policy are stronger signals than destination allowlisting alone.
