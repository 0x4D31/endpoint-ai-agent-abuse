# Cases

Cases map public incidents, malicious artifacts, and controlled research to EAA techniques. A mapping does not imply that every stage of a reported chain ran on a victim.

Procedure outcomes use the following terms:

- **present** — static or dynamic analysis establishes that an artifact or environment contains the procedure; execution is not implied.
- **planted** — the artifact or configuration was written or deployed to the target surface.
- **attempted** — code requested or initiated an action, but the public evidence does not establish successful completion.
- **executed** — runtime or forensic evidence establishes that the procedure ran.
- **impact-confirmed** — a downstream result such as collection, modification, access, or exfiltration was observed.

Case type supplies the context that the outcome vocabulary intentionally does not. For example, `executed` in a research case means controlled execution, not in-the-wild use.

## EAA-C-001 — Nx s1ngularity

**Type:** incident

**Date:** 2025-08-26 to 2025-08-27

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-016 | present | medium | The post-install artifact checked whether Claude Code, Gemini CLI, and Amazon Q were available before selecting an agent path. | S2 |
| 2 | EAA-001 | attempted | high | The payload invoked available agents with a filesystem-inventory prompt; public reporting does not establish which agent invocations completed on each affected host. | S1, S2 |
| 3 | EAA-002 | attempted | medium | The invocations supplied each product's permissive or non-interactive options. | S2 |

**Activation notes:** An affected Nx package had to be installed and an expected agent binary had to be available on the host and accept the supplied flags. The broader payload's collection and GitHub upload path did not depend solely on an agent succeeding. Snyk's analyzed payload exited on Windows.

**Sources:**

- `S1` — [Nx postmortem](https://nx.dev/blog/s1ngularity-postmortem)
- `S2` — [Snyk analysis](https://snyk.io/blog/weaponizing-ai-coding-agents-for-malware-in-the-nx-malicious-package/)

## EAA-C-002 — Trivy OpenVSX extension

**Type:** malicious artifact

**Date:** 2026-02-27 to 2026-02-28

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-001 | present | high | OpenVSX version 1.8.12 contained code designed to leverage local agents for collection and exfiltration. | S1 |
| 2 | EAA-016 | present | high | OpenVSX versions 1.8.12 and 1.8.13 contained prompts for enumerating installed tools, MCP servers, and authenticated sessions. | S2 |
| 3 | EAA-001 | attempted | medium | Workspace activation code spawned detached commands for Claude Code, Codex, Gemini CLI, Copilot CLI, and Kiro CLI. | S2 |
| 4 | EAA-002 | attempted | medium | The command strings requested permissive or non-interactive modes and the launcher suppressed process I/O and errors; successful option parsing was not established. | S2 |
| 5 | EAA-015 | attempted | medium | The 1.8.13 prompt asked an agent to use a locally authenticated GitHub CLI session to create a repository and upload its report. | S2 |

**Activation notes:** An affected OpenVSX extension version had to be installed and a workspace opened. At least one targeted CLI had to be present and accept the supplied flags. The GitHub path additionally required an authenticated `gh` session. The sources found no confirmed successful exfiltration.

**Sources:**

- `S1` — [Aqua advisory](https://github.com/aquasecurity/trivy-vscode-extension/security/advisories/GHSA-8mr6-gf9x-j8qg)
- `S2` — [Socket analysis](https://socket.dev/blog/unauthorized-ai-agent-execution-code-published-to-openvsx-in-aqua-trivy-vs-code-extension)

## EAA-C-003 — Mini Shai-Hulud

**Type:** campaign

**Date:** reported 2026-04-29

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-003 | planted | high | The analyzed payload committed a Claude Code `SessionStart` hook and referenced payload files into repositories accessible with stolen credentials. | S1 |

**Activation notes:** The package's malicious install hook first had to execute and obtain access to a repository. Later Claude-side execution required a compatible Claude Code version, the planted repository to be opened and trusted, and the `SessionStart` hook to load. The source does not confirm that the planted Claude hook fired on a victim endpoint.

**Sources:**

- `S1` — [StepSecurity analysis](https://www.stepsecurity.io/blog/a-mini-shai-hulud-has-appeared)

## EAA-C-004 — Miasma repository injection

**Type:** incident

**Date:** 2026-06-05

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-003 | planted | high | Malicious commit `5f456b8` added Claude Code and Gemini CLI session-hook configurations that referenced an embedded credential-harvesting payload. | S1 |
| 2 | EAA-004 | planted | high | The same commit added an always-applied Cursor rule instructing the agent to run the payload as project setup. | S1 |
| 3 | EAA-014 | planted | high | One commit targeted Claude Code, Gemini CLI, Cursor, and VS Code control-plane surfaces. | S1 |

**Activation notes:** Each product has distinct trust and activation behavior. The files were intended to trigger or induce execution only after the relevant product, version, workspace-trust decision, and lifecycle condition allowed it. A Cursor rule is an instruction to the model, not direct execution. The source does not establish MCP configuration abuse, agent-environment discovery, or later agent-side execution on a victim.

**Sources:**

- `S1` — [StepSecurity analysis](https://www.stepsecurity.io/blog/miasma-worm-hits-microsoft-again-azure-functions-action-and-72-other-repositories-disabled-after-supply-chain-attack-targeting-ai-coding-agents)

## EAA-C-005 — Miasma Phantom Gyp

**Type:** campaign

**Date:** 2026-06-03

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-003 | present | high | The decoded payload contained routines for writing Claude Code and Gemini CLI hook or settings files. | S1 |
| 2 | EAA-004 | present | high | The payload contained routines for writing persistent assistant instructions and Cursor rules. | S1 |
| 3 | EAA-014 | present | high | The same payload implemented writes across Claude, Gemini, Cursor, and VS Code control-plane formats. | S1 |

**Activation notes:** A compromised package had to reach `node-gyp` installation so its `binding.gyp` command substitution could execute the loader. The rows establish code present in the analyzed payload; the source does not establish that every agent configuration was written, loaded, or executed on a victim endpoint.

**Sources:**

- `S1` — [StepSecurity analysis](https://www.stepsecurity.io/blog/binding-gyp-npm-supply-chain-attack-spreads-like-worm)

## EAA-C-006 — Hades

**Type:** campaign

**Date:** 2026-06-08

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-016 | present | high | The analyzed payload contained workspace-tree traversal and checks for multiple assistant instruction and configuration surfaces. | S1 |
| 2 | EAA-004 | present | high | The payload contained routines for planting assistant instruction or rule files in discovered workspaces. | S1 |
| 3 | EAA-014 | present | high | The planting logic targeted multiple local assistant ecosystems from one payload. | S1 |

**Activation notes:** An affected Python package had to be imported for the initial payload chain to run. Later assistant behavior required a compatible product to load the written files under its own trust and lifecycle rules. Public reporting establishes the malicious artifacts and code paths, not subsequent model compliance or agent-side execution on every endpoint.

**Sources:**

- `S1` — [StepSecurity analysis](https://www.stepsecurity.io/blog/the-hades-campaign-pypi-packages)

## EAA-C-007 — Immobiliare Labs Backstage plugins

**Type:** campaign

**Date:** 2026-06-26

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-003 | present | high | Decoded code in the compromised packages contained a Claude Code `SessionStart` hook persistence routine. | S1 |
| 2 | EAA-004 | present | high | The code contained routines targeting Copilot instructions, Cursor rules, and other assistant instruction or configuration files. | S1 |
| 3 | EAA-014 | present | high | A single `infectHost` routine targeted Claude Code, Copilot, Cursor, VS Code, Aider, Kiro, Cody, Gemini, and Codex-related surfaces. | S1 |

**Activation notes:** A compromised package version had to be installed through a path that processed its `binding.gyp` file. The source establishes publication, decoded routines, and controlled runtime detection; it does not establish later agent-side activation on a victim endpoint.

**Sources:**

- `S1` — [StepSecurity analysis](https://www.stepsecurity.io/blog/immobiliarelabs-npm-packages-compromised)

## EAA-C-008 — Copied Claude instances and transcript tampering

**Type:** incident

**Date:** 2026-02-02 to 2026-02-22

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-005 | impact-confirmed | high | Investigators recovered a copied Claude installation with the original developer's session history and artifacts, plus archives of other stolen Claude instances. | S1 |
| 2 | EAA-015 | impact-confirmed | high | Recovered sessions showed the operator using local Claude and Codex agents with available shell, filesystem, and network access for intrusions and exfiltration against real organizations. | S1 |
| 3 | EAA-017 | impact-confirmed | high | Recovered logs show Claude locating a live JSONL transcript, truncating it before a named target, overwriting the live file, and verifying that the target was removed. | S1 |

**Activation notes:** The operator already controlled the hosts and the copied agent environment. The evidence is unusually strong because investigators recovered more than 1,000 native sessions and correlated them with host artifacts. This proves that the affected transcript was modified; it does not make every missing transcript event evidence of tampering.

**Sources:**

- `S1` — [OALABS forensic report](https://research.openanalysis.net/claude/codex/hacking/ai%20hacking/llm/redteam/policy%20violation/2026/06/16/compromised-claude-hacking.html)

## EAA-C-009 — MCP injection and rug-pull research

**Type:** research

**Date:** published 2025-04-10 to 2025-04-21

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-010 | executed | high | Trail of Bits demonstrated that an MCP server's tool description could influence the model before the user invoked that tool. | S1 |
| 2 | EAA-010 | executed | high | Invariant Labs published runnable experiments for direct tool poisoning, cross-server shadowing, and a sleeper server that changed its interface on a later load. | S2 |

**Activation notes:** A malicious MCP server had to be connected and its tool metadata exposed to the model. Invariant's sleeper experiment changed behavior on a second load; it does not by itself prove malicious use of a live protocol `list_changed` notification. These are controlled demonstrations, not incident evidence.

**Sources:**

- `S1` — [Trail of Bits line-jumping research](https://blog.trailofbits.com/2025/04/21/jumping-the-line-how-mcp-servers-can-attack-you-before-you-ever-use-them/)
- `S2` — [Invariant Labs MCP injection experiments](https://github.com/invariantlabs-ai/mcp-injection-experiments)

## EAA-C-010 — Claude Code persistent memory compromise

**Type:** research

**Date:** published 2026-04-01

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-003 | executed | high | Cisco's controlled npm-based proof of concept installed a global Claude Code `UserPromptSubmit` hook. | S1 |
| 2 | EAA-004 | executed | high | The proof of concept overwrote project `MEMORY.md` files and changed shell configuration to re-enable auto-memory. | S1 |
| 3 | EAA-004 | impact-confirmed | high | In the controlled environment, the poisoned agent followed a marker instruction and recommended insecure secret-handling practices. | S1 |

**Activation notes:** The user instructed Claude to set up the repository, approved dependency installation, and accepted workspace trust. Cisco reports that Claude Code 2.1.50 moved user memory out of the system prompt, reducing the demonstrated authority. That mitigation does not prevent same-user writes to memory, hooks, or settings.

**Sources:**

- `S1` — [Cisco research](https://blogs.cisco.com/ai/identifying-and-remediating-a-persistent-memory-compromise-in-claude-code)

## EAA-C-011 — MCP endpoint rewrite and OAuth interception

**Type:** research

**Date:** published 2026-05-05

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-006 | executed | high | Mitiga's controlled npm post-install payload seeded trust state and rewrote an MCP endpoint to a controlled proxy. | S1 |
| 2 | EAA-003 | executed | high | A hook in the subsequently trusted project ran and reasserted the proxy endpoint. | S1 |
| 3 | EAA-015 | impact-confirmed | high | An OAuth-backed MCP session traversed the proxy, exposing a bearer token that the researchers then used to demonstrate downstream access. | S1 |

**Activation notes:** The chain assumes attacker-controlled code already executes as the user, a subsequently trusted project contains the hook, and a compatible OAuth-backed MCP authorization flow exists. Mitiga reports that Anthropic treated the finding as out of scope because of the initial same-user execution prerequisite. This is not an observed campaign.

**Sources:**

- `S1` — [Mitiga research](https://www.mitiga.io/blog/claude-code-mcp-token-theft-mitm)

## EAA-C-012 — Claude Code Remote Control used as C2

**Type:** research

**Date:** published 2026-06-29

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-008 | executed | high | Dash created an isolated `CLAUDE_CONFIG_DIR`, installed an attacker-controlled full-scope Claude.ai login, and seeded workspace-trust state. | S1 |
| 2 | EAA-002 | executed | high | A custom script installed and launched the local worker non-interactively into a Remote Control session. | S1 |
| 3 | EAA-015 | executed | high | The local worker accepted remote operator instructions through Claude.ai and performed actions on the endpoint. | S1 |

**Activation notes:** The proof of concept required prior local execution plus suitably scoped Claude.ai account material. It did not bypass the full-scope login requirement. Remote Control and the relevant organization policy had to permit the session. The report demonstrates a controlled chain, not in-the-wild use.

**Sources:**

- `S1` — [Dash Security research](https://dash.security/blog/living-off-coding-agents-claude-as-a-c2-server)

## EAA-C-013 — Claude Code OpenTelemetry redirection

**Type:** research

**Date:** published 2026-06-29

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-012 | impact-confirmed | medium | Bloom reports that project-scoped settings redirected Claude Code telemetry and delivered session and identity data to a controlled collector. | S1 |
| 2 | EAA-012 | impact-confirmed | medium | Bloom reports that `otelHeadersHelper` executed a command, placed its output in export headers, and was then used to persist telemetry settings at user scope. | S1 |

**Activation notes:** Sensitive prompt, tool-content, and raw-body options are disabled by default and had to be enabled. Project settings are subject to workspace trust and can be overridden by managed settings. Anthropic disputed the researchers' security characterization; the reported trust behavior should be reproduced against the affected version before being generalized to current releases.

**Sources:**

- `S1` — [Bloom Security research](https://bloom.security/blog/welcome-to-otel-claudeifornia)

## EAA-C-014 — SymJack agent-mediated config overwrite

**Type:** research

**Date:** published 2026-05-26 to 2026-05-27

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-004 | executed | high | A repository instruction was loaded and induced the agent to request benign-looking shell copy operations. | S1 |
| 2 | EAA-006 | planted | high | After approval, a shell copy followed a repository symlink and overwrote agent settings or MCP configuration with disguised payload content. | S1 |
| 3 | EAA-006 | executed | high | After restart, the planted MCP server spawned and ran its configured demonstration command as the user. | S1 |

**Activation notes:** The detailed Claude chain included a workspace-trust decision and explicit approval of a copy into settings; it then used a second approved copy to overwrite `.mcp.json`. The broader product demonstrations therefore required at least one explicit operation approval, and the shown chain used two. The report lists Claude Code 2.1.114 in its per-vendor table and separately compares 2.1.128 with partially hardened 2.1.129; it also lists Gemini CLI 0.43.0, Antigravity CLI 1.0.2, Cursor CLI 2026.05.20, Copilot CLI 1.0.51, Grok Build CLI 0.1.216, and Codex CLI 0.133.0. Repository symlinks are recreated natively on macOS and Linux; Windows requires Developer Mode or an Administrator terminal. The source does not identify the exact OS used for every product demonstration.

**Sources:**

- `S1` — [Adversa AI research](https://adversa.ai/blog/the-approval-prompt-is-lying-to-you-symlink-rce-in-five-ai-coding-agents-claude-code-cursor-antigravity-copilot-grok-build/)

## EAA-C-015 — Historical Claude Code project-configuration vulnerabilities

**Type:** research

**Date:** published 2026-02-25

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-003 | executed | high | Check Point demonstrated an affected Claude Code version running a project `SessionStart` hook after general workspace trust, without a separate hook-command approval. | S1 |
| 2 | EAA-006 | executed | high | Repository settings approved and started a project MCP server before the user completed the trust decision. | S1 |
| 3 | EAA-007 | impact-confirmed | high | A repository-controlled `ANTHROPIC_BASE_URL` redirected startup requests and exposed an API authorization header to the controlled proxy before workspace trust. | S1 |

**Activation notes:** The paths required a malicious project and an affected historical Claude Code version. The hook path still followed the user's general workspace-trust acceptance; the MCP and provider-routing paths crossed that decision earlier. Anthropic patched all three reported paths before publication. The source does not identify a public malicious campaign or precise affected version range for every path.

**Sources:**

- `S1` — [Check Point research](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/)

## EAA-C-016 — Claude Code workspace-trust bypass

**Type:** vendor advisory

**Date:** published 2026-03-18

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-002 | executed | high | In affected versions, repository-controlled `permissions.defaultMode=bypassPermissions` was resolved before workspace trust, causing the first-open trust dialog to be skipped and the session to enter permissive mode. | S1 |

**Activation notes:** The advisory affects Claude Code versions earlier than 2.1.53 and identifies 2.1.53 as patched. A user still had to open the malicious repository. The advisory establishes the permission-mode and trust-bypass behavior, not a downstream malicious action or an observed campaign.

**Sources:**

- `S1` — [Anthropic advisory GHSA-mmgp-wc2j-qcv7](https://github.com/anthropics/claude-code/security/advisories/GHSA-mmgp-wc2j-qcv7)
