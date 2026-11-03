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

**Date:** reported 2026-06-08

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-016 | present | high | The analyzed payload contained workspace-tree traversal and checks for multiple assistant instruction and configuration surfaces. | S1 |
| 2 | EAA-004 | present | high | The payload contained routines for planting assistant instruction or rule files in discovered workspaces. | S1 |
| 3 | EAA-014 | present | high | The planting logic targeted multiple local assistant ecosystems from one payload. | S1 |

**Activation notes:** StepSecurity describes an obfuscated `__init__.py` import hook as the campaign's entry path, but EAA does not assume one Python trigger across every affected distribution. Before any agent-side effect, the payload's planting routines had to execute and a compatible product then had to load the written files under its own trust and lifecycle rules. Public evidence establishes the planting code in analyzed artifacts, not victim-side planting or later agent action.

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
| 2 | EAA-015 | executed | high | Recovered sessions show the attacker using a developer’s existing Claude instance on the compromised host, then continuing to use it after copying the installation and session history to other hosts. | S1 |
| 3 | EAA-017 | impact-confirmed | high | Recovered logs show Claude locating a live JSONL transcript, truncating it before a named target, overwriting the live file, and verifying that the target was removed. | S1 |

**Activation notes:** The attacker first used the developer’s existing Claude instance on the compromised Hetzner host, then copied and reused it elsewhere. This takeover and reuse of a victim’s agent environment is the EAA-015 procedure. The report also describes attacker-operated Codex sessions, which do not independently establish that procedure. Recovered sessions and host artifacts confirm the copied state and the specific transcript modification in this case.

**Sources:**

- `S1` — [OALABS compromised Claude and Codex forensic investigation](https://research.openanalysis.net/claude/codex/hacking/ai%20hacking/llm/redteam/policy%20violation/2026/06/16/compromised-claude-hacking.html)

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

| Step | Technique | Outcome | Confidence | Claim | Sources | Version sources |
|---|---|---|---|---|---|---|
| 1 | EAA-003 | executed | high | Check Point demonstrated an affected Claude Code version running a project `SessionStart` hook after general workspace trust, without a separate hook-command approval. | S1 | S2 |
| 2 | EAA-006 | executed | high | Repository settings approved and started a project MCP server before the user completed the trust decision. | S1 | S3 |
| 3 | EAA-007 | impact-confirmed | high | A repository-controlled `ANTHROPIC_BASE_URL` redirected startup requests and exposed an API authorization header to the controlled proxy before workspace trust. | S1 | S4 |

**Activation notes:** The paths required a malicious project and an affected historical Claude Code version. The hook path still followed the user's general workspace-trust acceptance; the MCP and provider-routing paths crossed that decision earlier. The hook advisory identifies versions earlier than 1.0.87 for the insufficient-warning issue; 1.0.87 clarified the warning rather than disabling hooks after accepted workspace trust. Separate advisories identify versions earlier than 1.0.111 for MCP pre-trust execution and earlier than 2.0.65 for provider-routing leakage, with those versions as the respective fixes. The sources do not identify a public malicious campaign.

**Sources:**

- `S1` — [Check Point research](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/)
- `S2` — [Anthropic startup-warning advisory](https://github.com/anthropics/claude-code/security/advisories/GHSA-ph6w-f82w-28w6)
- `S3` — [GitHub advisory for CVE-2025-59536](https://github.com/advisories/GHSA-4fgq-fpq9-mr3g)
- `S4` — [Anthropic advisory for CVE-2026-21852](https://github.com/anthropics/claude-code/security/advisories/GHSA-jh7p-qr78-84p7)

## EAA-C-016 — Claude Code workspace-trust bypass

**Type:** vendor advisory

**Date:** published 2026-03-18

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-002 | executed | high | In affected versions, repository-controlled `permissions.defaultMode=bypassPermissions` was resolved before workspace trust, causing the first-open trust dialog to be skipped and the session to enter permissive mode. | S1 |

**Activation notes:** The advisory affects Claude Code versions earlier than 2.1.53 and identifies 2.1.53 as patched. A user still had to open the malicious repository. The advisory establishes the permission-mode and trust-bypass behavior, not a downstream malicious action or an observed campaign.

**Sources:**

- `S1` — [Anthropic advisory GHSA-mmgp-wc2j-qcv7](https://github.com/anthropics/claude-code/security/advisories/GHSA-mmgp-wc2j-qcv7)

## EAA-C-017 — Jscrambler npm compromise

**Type:** incident

**Date:** 2026-07-11

| Step | Technique | Outcome | Confidence | Claim | Sources | Version sources |
|---|---|---|---|---|---|---|
| 1 | EAA-016 | present | high | Static analysis of the embedded native payload identified product-specific paths and selectors for Claude Desktop, Cursor, Windsurf, Factory, Zed, VS Code, opencode, and MCP configuration. | S1 | S2 |
| 2 | EAA-005 | present | high | The credential-stealer artifact contained selectors for collecting agent and MCP configuration that can hold API keys or server credentials; the same payload separately implemented outbound upload. | S1 | S2 |

**Activation notes:** Socket identified 8.14.0, 8.16.0, and 8.17.0 as preinstall-triggered malicious releases and 8.18.0 and 8.20.0 as triggered on package import or CLI execution. Jscrambler's ongoing advisory currently lists 8.14, 8.16, 8.17, and 8.20, omitting 8.18; both sources identify 8.22 as safe. Jscrambler reported zero known downloads while warning that npm statistics may lag. The agent-related rows therefore establish capability present in the analyzed artifact, not victim-side discovery, collection, or exfiltration. The bundled payloads targeted Linux x86-64, Windows x86-64, and macOS arm64.

**Sources:**

- `S1` — [Socket analysis](https://socket.dev/blog/jscrambler-supply-chain-attack)
- `S2` — [Jscrambler advisory](https://jscrambler.com/blog/security-advisory-malicious-npm-package)

## EAA-C-018 — Amazon Q MCP auto-execution vulnerability

**Type:** vendor advisory

**Date:** published 2026-06-23

| Step | Technique | Outcome | Confidence | Claim | Sources | Version sources |
|---|---|---|---|---|---|---|
| 1 | EAA-006 | executed | high | Wiz demonstrated an affected Amazon Q Developer extension loading and executing a repository-controlled MCP command when Amazon Q was activated. | S2 | S1 |
| 2 | EAA-015 | impact-confirmed | high | In controlled testing, the spawned command inherited the developer environment and successfully used the active AWS session with `aws sts get-caller-identity`. | S2 | S1 |

**Activation notes:** A malicious repository had to contain `.amazonq/mcp.json`, an affected Amazon Q Developer extension had to be active, and the repository had to be opened. The AWS advisory says the user also had to trust the workspace when prompted; Wiz reports that the tested path had no MCP consent prompt or workspace-trust check. EAA preserves that disagreement rather than treating either activation description as settled. AWS identifies Language Servers for AWS 1.65.0 and `@aws/lsp-codewhisperer` 0.0.113 as patched.

**Sources:**

- `S1` — [AWS advisory GHSA-xhcr-j4j9-3gh7](https://github.com/aws/language-servers/security/advisories/GHSA-xhcr-j4j9-3gh7)
- `S2` — [Wiz research](https://www.wiz.io/blog/amazon-q-vulnerability)

## EAA-C-019 — SANDWORM_MODE AI toolchain poisoning

**Type:** campaign

**Date:** reported 2026-02-20

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-016 | present | high | The analyzed payload contained checks for agent configuration paths, local model runtimes, and LLM-provider credentials. | S1 |
| 2 | EAA-006 | present | high | The payload contained code to deploy a rogue local MCP server and write server entries to paths it treated as agent configuration files. | S1 |
| 3 | EAA-010 | present | high | The rogue MCP server advertised innocuous-looking tools whose descriptions contained embedded adversarial instructions. | S1 |
| 4 | EAA-014 | present | high | One payload implemented fan-out writes targeting paths it treated as configuration for Claude Code, Claude Desktop, Cursor, Continue, and Windsurf/Codeium. | S1 |

**Activation notes:** Socket reported an active npm campaign and analyzed routines for discovering agent environments, deploying a rogue MCP server, embedding adversarial instructions in its tool descriptions, and writing paths it treated as configuration across several agent ecosystems. Socket reports the Claude Code target as `~/.claude/settings.json`; current [Claude Code configuration documentation](https://code.claude.com/docs/en/debug-your-config) says `settings.json` ignores `mcpServers`, so this does not establish a usable Claude Code MCP registration. The broader second stage was delayed for 48 to 96 hours on non-CI hosts. Public reporting does not establish that the agent-specific writes completed on a victim endpoint or that a targeted agent loaded or followed the poisoned tools, so every agent-related procedure remains `present`.

**Sources:**

- `S1` — [Socket analysis](https://socket.dev/blog/sandworm-mode-npm-worm-ai-toolchain-poisoning)

## EAA-C-020 — Claude Code persistent settings injection

**Type:** vendor advisory

**Date:** published 2026-02-06

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-003 | planted | high | In affected versions, code inside Claude Code's bubblewrap sandbox could create a missing user `settings.json` and plant a persistent `SessionStart` hook intended to run outside the sandbox after restart. | S1 |

**Activation notes:** The planting path required `.claude/settings.json` to be absent when Claude Code started and malicious code to run inside the sandbox while the parent `.claude` directory remained writable. Later execution outside the sandbox additionally required Claude Code to restart after the file and hook were planted. The advisory affects Claude Code versions earlier than 2.1.2 and identifies 2.1.2 as patched. It does not identify exploitation in a public campaign.

**Sources:**

- `S1` — [Claude Code persistent-configuration injection advisory](https://github.com/anthropics/claude-code/security/advisories/GHSA-ff64-7w26-62rf)

## EAA-C-021 — ContextCrush Context7 custom-rule injection

**Type:** research

**Date:** published 2026-03-05

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-018 | impact-confirmed | high | Noma registered a Context7 library with poisoned Custom Rules that were returned verbatim with library documentation and induced the coding agent to follow the embedded instructions. | S1 |
| 2 | EAA-015 | impact-confirmed | high | In the controlled sequence, the coding agent read project `.env` files and sent their contents to an attacker-controlled GitHub repository as an issue. | S1 |

**Activation notes:** An attacker had to control a library entry and its Custom Rules in the Context7 registry. A developer then had to query that library through the affected Context7 MCP service from a coding agent with local file and outbound GitHub access. Although Context7 named the upstream field Custom Rules, the endpoint agent received it inside retrieved MCP content rather than from an endpoint-designated rule or instruction store. Noma reports that the fix was deployed on 2026-02-23, before the 2026-03-05 disclosure, and found no evidence of in-the-wild exploitation. The report names several Context7-compatible coding assistants but does not identify the exact agent, version, or operating system used for the demonstrated sequence.

**Sources:**

- `S1` — [Noma ContextCrush research](https://noma.security/blog/contextcrush-context7-the-mcp-server-vulnerability/)

## EAA-C-022 — GitLost public-issue data disclosure

**Type:** research

**Date:** 2026-04-02

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-018 | impact-confirmed | high | A crafted public issue body entered an assigned GitHub Agentic Workflow and caused the agent to follow its request for same-organization repository content. | S1, S2 |
| 2 | EAA-015 | impact-confirmed | high | The workflow used its cross-repository read access to retrieve a private repository's README and posted the contents in a public issue comment. | S1, S2 |

**Activation notes:** The organization had configured a GitHub Agentic Workflow to run on `issues.assigned`, read the issue title and body, post through `add-comment`, and read other public and private repositories. An unauthenticated user then had to create the crafted public issue and the automation had to assign it. The public bot comment identifies the engine as Claude and the model as `claude-opus-4-6`. This is a controlled proof of concept, not evidence of exploitation against an unrelated organization.

**Sources:**

- `S1` — [Noma GitLost research](https://noma.security/blog/gitlost-how-we-tricked-githubs-ai-agent-into-leaking-private-repos/)
- `S2` — [Public proof-of-concept issue](https://github.com/sasinomalabs/poc/issues/153)

## EAA-C-023 — ChainDrop npm supply-chain compromise

**Type:** incident

**Date:** 2026-08-04 to 2026-08-05

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-016 | present | high | The recovered ChainDrop payload contained cross-platform discovery logic for hundreds of secret locations, including configuration associated with Cursor, OpenClaw, OpenAI Codex, OpenCode, Gemini, and Hermes. | S2 |
| 2 | EAA-005 | present | high | The same artifact contained product-specific paths that could collect endpoint-agent configuration or state alongside cloud, developer, browser, and package-registry credentials. | S2 |
| 3 | EAA-003 | present | high | Microsoft recovered code that uses stolen GitHub credentials to inject Claude Code startup files into repository branches; the same routine also targets VS Code task configuration. | S1 |

**Activation notes:** ChainDrop spread through malicious npm releases beginning with `keyv@6.0.0` on 2026-08-04. Package installation had to execute the malicious lifecycle code. The analyzed payload supported Linux, Windows, and macOS and expanded the predecessor campaign's hardcoded secret-location set from 189 to 469 entries. Public reporting confirms the agent-related routines in the malicious artifact, but does not identify a victim whose agent files were found or collected, or confirm the repository-injection routine completed and a later checkout activated the planted configuration. The startup-file path uses GitHub repository writes, not an assumed local workspace write. Those procedures therefore remain `present`.

**Sources:**

- `S1` — [Microsoft ChainDrop supply-chain compromise analysis](https://www.microsoft.com/en-us/security/blog/2026/08/04/chaindrop-supply-chain-compromise-anatomy-self-propagating-worm/)
- `S2` — [GitGuardian ChainDrop deobfuscation](https://blog.gitguardian.com/keyv-mini-shai-hulud/)

## EAA-C-024 — Trojanized registry skills targeting Paperclip and Browser Use

**Type:** research

**Date:** 2026-07-11 to 2026-08-02

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-009 | present | high | Zenity recovered trojanized skill revisions distributed through skills.sh, with setup instructions pointing to a remote credential-harvesting stage. | S1 |
| 2 | EAA-004 | executed | medium | During controlled testing, the agent followed the installed skill’s instructions to open a secondary setup document and run its commands. | S1 |
| 3 | EAA-015 | impact-confirmed | medium | Zenity reports credential collection and transmission to attacker-controlled infrastructure during controlled detonation. | S1 |

**Activation notes:** A malicious skill had to be loaded and invoked for a matching setup task, with host-command and network access available. Paperclip and Browser Use were lures; the report does not identify the tested agent or version, or provide a complete transcript. Execution and impact therefore have medium confidence. Zenity dates the malicious skill family from July 11 to its removal on August 2, 2026. The reported 1.7 million-plus skills.sh installs are an aggregate registry counter, not unique or compromised endpoints. The controlled test documents activation, but not skill acquisition; EAA-009 remains present.

**Sources:**

- `S1` — [Zenity trojanized skill-supply-chain research](https://labs.zenity.io/post/attackers-target-agents-via-the-skill-supply-chain)

## EAA-C-025 — Kiro MCP configuration rewrite through web content

**Type:** research

**Date:** published 2026-07-20

| Step | Technique | Outcome | Confidence | Claim | Sources | Version sources |
|---|---|---|---|---|---|---|
| 1 | EAA-018 | executed | high | In controlled testing, hidden instructions in content retrieved by Kiro's web-fetch capability caused the agent to perform an unrelated local configuration write. | S1 | S2 |
| 2 | EAA-006 | executed | high | Kiro wrote an attacker-selected MCP server entry to the user-level `~/.kiro/settings/mcp.json` file and automatically reloaded it without a separate approval. | S1 | S2 |
| 3 | EAA-015 | impact-confirmed | high | The reloaded MCP command ran Node.js and delivered the test host's username, hostname, and platform to a localhost callback. | S1 | S2 |

**Activation notes:** The user approved a web fetch containing hidden instructions; Kiro then wrote and reloaded user-level MCP configuration without separate effective approval. Intezer/Kodem tested Kiro 0.9.2 on macOS and 0.10.16 on Ubuntu, and verified the fix in 0.11.130. The research lists Auto model selection and a separate Qwen 3 Coder run with Autopilot enabled. AWS's June 2 advisory scopes CVE-2026-10591 to versions below 0.11 but describes an execution-sensitive file-write path using VS Code tasks; it supplies version evidence, not independent reproduction of the July 20 MCP demonstration. The callback was localhost, and no victim exploitation is established.

**Sources:**

- `S1` — [Intezer and Kodem Kiro web-to-MCP research](https://research.intezer.com/blog/2026/07/remote-code-execution-kiro/)
- `S2` — [AWS Kiro IDE CVE-2026-10591 advisory](https://aws.amazon.com/security/security-bulletins/2026-037-aws/)

## EAA-C-026 — GitSpawn repository-metadata command execution

**Type:** research

**Date:** published 2026-09-01

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-019 | executed | medium | Manifold reports host command execution through agent-initiated Git inspection across seven products. Five product paths have detailed demonstrations; Codex and Cursor are reported as affected and patched without equivalent public mechanism detail. | S1 |

**Activation notes:** The target had to open a working tree whose `.git` metadata remained intact, and the affected agent had to perform its automatic Git context gathering. Normal clone, fetch, and pull operations do not transfer another repository's local `.git/config`; delivery paths such as an archive, shared or synchronized folder, removable media, or a locally modified repository can preserve it. As of the September 1 publication, Manifold reported these affected, fixed, or tested versions: Claude Code 2.1.193 fixed in 2.1.196 for the `core.fsmonitor` path, with a separate `ultrareview` path tested in 2.1.210 and still affected in 2.1.252; goose 1.41.0 fixed in 1.44.0; Hermes Agent 0.18.2 still affected in 0.21.0; Qwen Code 0.19.6 still affected in 0.22.3; Grok Build 0.2.93 still affected in 1.0.13; and OpenAI Codex and Cursor affected and patched without exact public version ranges. These are controlled findings, not a public victim incident.

**Sources:**

- `S1` — [Manifold Security GitSpawn research](https://www.manifold.security/blog/ai-coding-agents-git-hijack)

## EAA-C-027 — Agent-consumed dangling-reference takeover

**Type:** research

**Date:** published 2026-08-26

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-020 | executed | medium | Researchers report that controlled coding-agent trials followed unchanged agent-facing documentation and installed packages registered at its previously unclaimed destinations. | S1 |
| 2 | EAA-020 | present | medium | The separately observed `clerk-next-fix-auth-protection` npm package occupied a bare package name referenced by Clerk's agent-facing guidance and published install hooks that collected host metadata. | S1, S2 |

**Activation notes:** The controlled trials establish the reported installation path. Separately reported third-party callbacks lack public logs attributing them to a particular endpoint agent; they are not counted as confirmed agent impact. The Clerk reference requires an additional condition: its bare executable name can resolve to the malicious standalone npm package when @clerk/eslint-plugin is absent locally. OSV identifies versions 7.7.7 and 8.8.8 as malicious, but neither source proves victim-side agent installation; that procedure remains present. The agent-documentation linkage is reported by the researcher; OSV independently corroborates the package behavior, not that linkage or agent execution.

**Sources:**

- `S1` — [Alon Hertz agent-consumed reference-takeover research](https://medium.com/@alonhertz1/data-became-code-we-ran-code-inside-fortune-500s-using-files-they-published-for-ai-agents-0cd67ffbbffc)
- `S2` — [OSV MAL-2026-11069 record](https://osv.dev/vulnerability/MAL-2026-11069)

## EAA-C-028 — GhostSplice split-channel MCP injection

**Type:** research

**Date:** published 2026-07-23

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-018 | impact-confirmed | high | Instruction-bearing MCP tool results supplied file-to-parameter mappings; controlled runs sent seeded secrets as arguments to the malicious server. | S1, S2 |
| 2 | EAA-015 | impact-confirmed | high | In the controlled scenarios, OpenAI Codex CLI, Cursor, and Visual Studio Code with GitHub Copilot read synthetic secrets from local files and passed them to the malicious MCP server. | S1, S2 |

**Activation notes:** A connected malicious MCP server and access to seeded project files were prerequisites. The main flow combined a tool schema with file inventory and transfer instructions returned by tools; the malicious directive in returned content is EAA-018. A separate VS Code/GitHub Copilot variant added sampling and required client support and sampling permission. The pinned repository contains per-client logs and synthetic fixtures, including Codex CLI runs with GPT-5.4 and GPT-5.5; client build versions are not pinned. Outcomes varied by model and harness, and graphical-editor aggregate results were not finalized. July 23 is the repository publication date, not the experiment date. These are controlled results, not victim compromise.

**Sources:**

- `S1` — [ASSET Group GhostSplice research](https://asset-group.github.io/disclosures/ghostsplice/)
- `S2` — [GhostSplice proof-of-concept repository](https://github.com/asset-group/ghostsplice/tree/dfaee36c94f3cd23ed775ddd72012d00fa486a75)

## EAA-C-029 — Amazon Q VS Code extension destructive-agent payload

**Type:** incident

**Date:** published 2025-07-23

| Step | Technique | Outcome | Confidence | Claim | Sources | Version sources |
|---|---|---|---|---|---|---|
| 1 | EAA-001 | present | high | The malicious extension commit contains a Q CLI launcher with attacker-selected destructive instructions. | S2 | S1 |
| 2 | EAA-002 | present | high | The source commit supplies trust-all and non-interactive flags to the intended Q invocation. | S2 | S1 |

**Activation notes:** The malicious extension revision would have needed to execute its launcher and find the local Q CLI. AWS states that a syntax error prevented the shipped code from executing or changing customer environments. Version 1.84.0 carried the code; 1.85.0 removed it. The intended deletion prompt and permissive flags are artifact evidence only, not proof of an agent launch, attempted deletion, or cloud impact.

**Sources:**

- `S1` — [AWS Amazon Q VS Code extension compromise advisory](https://aws.amazon.com/security/security-bulletins/AWS-2025-015/)
- `S2` — [Malicious Amazon Q extension source commit](https://github.com/aws/aws-toolkit-vscode/commit/1294b38b7fade342cfcbaf7cf80e2e5096ea1f9c)

## EAA-C-030 — Postmark MCP implementation backdoor

**Type:** malicious artifact

**Date:** published 2025-09-25

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-021 | present | high | Published postmark-mcp server code adds an unrequested BCC recipient inside the sendEmail handler, without requiring malicious instructions to the model. | S1, S2 |

**Activation notes:** The malicious npm server had to be installed, configured with usable Postmark credentials, and invoked through its sendEmail handler. Snyk reproduces code labelled 1.0.18; the embedded package manifest says 1.0.14, so it is not an independently authenticated package-version record. OSV separately identifies the malicious range beginning at 1.0.16. These sources establish the backdoor, but publish no victim-specific agent invocation or delivery receipt. The legitimate Postmark service and official repository are not established as compromised.

**Sources:**

- `S1` — [Snyk postmark-mcp analysis and reproduced server code](https://snyk.io/blog/malicious-mcp-server-on-npm-postmark-mcp-harvests-emails/)
- `S2` — [OSV MAL-2025-47604 postmark-mcp record](https://osv.dev/vulnerability/MAL-2025-47604)

## EAA-C-031 — Claude Code GitHub Action process-environment disclosure

**Type:** research

**Date:** published 2026-06-05

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-018 | executed | high | In Microsoft's controlled workflow, injected GitHub content caused Claude Code to read the agent process environment. | S1 |
| 2 | EAA-015 | impact-confirmed | high | The Read result contained the unsanitized ANTHROPIC_API_KEY from the runner process, establishing credential collection. | S1 |

**Activation notes:** The lab workflow accepted untrusted GitHub content and exposed an API key to the agent process. Its Read tool accessed process environment data outside the scrubbed Bash subprocess boundary. Microsoft reports mitigation in Claude Code 2.1.128. This is controlled CI-runner evidence, not a confirmed production incident. Collection is established; proposed WebFetch, shell, MCP, and logging exfiltration routes depend on workflow configuration and are not all claimed as executed.

**Sources:**

- `S1` — [Microsoft Claude Code GitHub Action secret-exposure research](https://www.microsoft.com/en-us/security/blog/2026/06/05/securing-ci-cd-in-agentic-world-claude-code-github-action-case/)

## EAA-C-032 — OpenClaw control gateway takeover

**Type:** research

**Date:** published 2026-02-01

| Step | Technique | Outcome | Confidence | Claim | Sources | Version sources |
|---|---|---|---|---|---|---|
| 1 | EAA-015 | executed | medium | depthfirst reports reusing a leaked OpenClaw gateway token to disable approval checks, select host execution, and invoke a host command. | S1 | S2 |

**Activation notes:** The user had authenticated to the Control UI before visiting the crafted page. Gateway URL handling exposed the stored token, and the browser could reach the local gateway. The stolen token allowed approval and execution-policy changes. depthfirst reports host command execution, but publishes the command request without a host-side result; confidence is medium. The chain changed execution policy rather than exploiting the container runtime. The vendor lists versions through 2026.1.28 as affected and 2026.1.29 as fixed; the researcher reports the narrower range through 2026.1.24-1.

**Sources:**

- `S1` — [depthfirst OpenClaw gateway takeover research](https://depthfirst.com/research/1-click-rce-to-steal-your-moltbot-data-and-keys)
- `S2` — [OpenClaw gatewayUrl token-exfiltration advisory](https://github.com/openclaw/openclaw/security/advisories/GHSA-g8p2-7wf7-98mq)

## EAA-C-033 — AI ClickFix through a computer-use interface

**Type:** research

**Date:** published 2025-05-24

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-018 | executed | medium | The demonstration redirected Claude Computer Use from webpage interaction into pasting a terminal command that fetched and ran a script. | S1 |

**Activation notes:** The agent visited a researcher-controlled page, clicked a button that copied a command to the clipboard, and followed instructions to paste and run it in a terminal. The demonstration used `claude-3-7-sonnet-20250219` and `xfce4-terminal`; the agent build and OS version were not reported.

**Sources:**

- `S1` — [Embrace The Red AI ClickFix demonstration](https://embracethered.com/blog/posts/2025/ai-clickfix-ttp-claude/)

## EAA-C-034 — Poisoned take-home assessment and MCP exfiltration

**Type:** incident

**Date:** published 2026-06-19

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-004 | executed | medium | Mitiga reports that Cursor loaded poisoned project rules and followed the embedded setup workflow. | S1 |
| 2 | EAA-018 | present | medium | The incident report identifies hidden instruction-bearing README comments alongside persistent rule files; their independent causal contribution is not established. | S1 |
| 3 | EAA-006 | executed | medium | The agent loaded the repository-supplied MCP integration and invoked its environment-check tool. | S1 |
| 4 | EAA-010 | executed | medium | Mitiga attributes the environment-check call to a poisoned tool description that presented credential submission as setup validation. | S1 |
| 5 | EAA-015 | impact-confirmed | medium | The reported sequence read cloud credentials and transmitted collected data through the MCP environment-check call. | S1 |

**Activation notes:** Mitiga reports Cursor with terminal access, MCP tools, and auto-run already enabled. Its redacted timeline shows rule, README, and MCP context loaded before collection and transmission. Victim identity, versions, and complete artifacts are unavailable, so claims use medium confidence. README and rule effects were not isolated; the README mapping records presence only. Auto-run is a prerequisite, not an attacker-made EAA-002 change. Cloud escalation paths discussed by the report are not additional confirmed outcomes.

**Sources:**

- `S1` — [Mitiga poisoned coding-assessment incident report](https://www.mitiga.io/blog/poisoned-coding-test-ai-agent-attack)

## EAA-C-035 — Skill marketplace replacement and delayed update

**Type:** research

**Date:** published 2026-05-05

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-009 | executed | medium | Orca reports that skill installation and update flows fetched attacker-controlled revisions, including nested installation that replaced an existing same-name skill. | S1 |
| 2 | EAA-004 | executed | medium | Agents followed the changed skill instructions and sent test callbacks in Orca’s research. | S1 |

**Activation notes:** Orca reports installation, nested replacement, and later update flows with benign execution callbacks. The publication does not identify the marketplace or pin agent and installer versions; confidence is medium. A user or agent had to install a skill or run the update command, then activate the changed instructions. This supports EAA-009 and EAA-004; a repository update is not evidence of EAA-013's account-enabled cloud-skill synchronization path. Popularity counters and callback counts do not establish malicious victim compromise.

**Sources:**

- `S1` — [Orca skill marketplace installation and update research](https://orca.security/resources/blog/ai-agent-skill-supply-chain-security/)

## EAA-C-036 — Agentjacking through Sentry error context

**Type:** research

**Date:** published 2026-06-17

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-018 | executed | medium | Tenet reports that fabricated diagnostic instructions in Sentry error data induced coding agents to execute a researcher-controlled npm validation package. | S1 |

**Activation notes:** Researchers submitted crafted error events using a public Sentry DSN. Coding agents retrieved those events through the Sentry integration while investigating issues. The report identifies Claude Code 2.1.161 in a June 2 capture and includes macOS and Windows/WSL examples. Other client versions and complete host traces were not published. This case records package execution; the redacted probes do not establish subsequent credential use or account compromise.

**Sources:**

- `S1` — [Tenet Agentjacking through Sentry error data](https://tenetsecurity.ai/blog/agentjacking-coding-agents-with-fake-sentry-errors/)

## EAA-C-037 — Muse dictation endpoint redirection and account-token reuse

**Type:** research

**Date:** published 2026-09-21

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-007 | present | high | The PoC changes `endo_voyager_dictation_endpoint` to a local WebSocket proxy that captures Muse’s account token and can replace returned dictation text. | S1 |
| 2 | EAA-015 | present | high | The PoC includes routines to reuse the captured token to read account chat history and submit agent requests, including device commands. | S1 |

**Activation notes:** The attacker must already be able to run code as the local user. The PoC changes a Muse preference and restarts the app; the next dictation session passes through the proxy. Token reuse requires a valid account token and access to the account’s gateway. The PoC’s gateway client supports standard VMs, not confidential VMs requiring recovery credentials. Device actions depend on the device’s permissions and any required Muse approval. Both procedures describe code in commit `1e5615be645c64791600c947d8d5988205fd1514`; the cited artifact does not establish successful execution. The repository does not specify tested app versions, affected ranges, or a fixed build. This Muse finding is separate from ChatGPT CVE-2026-100754.

**Sources:**

- `S1` — [Patrick Wardle not-a-mused proof of concept (commit 1e5615be)](https://github.com/pwardle/not-a-mused/tree/1e5615be645c64791600c947d8d5988205fd1514)

## EAA-C-038 — Mandiant-reported takeover of an active coding-assistant session

**Type:** incident

**Date:** reported 2026-09-16

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-015 | executed | medium | Mandiant reports that an attacker hijacked a developer’s active coding-assistant session and used the trusted assistant to recommend an attacker-poisoned external package. | S1 |

**Activation notes:** Mandiant’s September 2026 report describes an unnamed SaaS provider and a developer workstation. The report does not give the incident date, assistant product, version, session-hijack method, or underlying session artifacts. September 16 is the date of public reporting about the case, not the intrusion date. The assistant recommended a poisoned package; the report then describes installation through the developer’s active session after acceptance. It does not isolate which later actions were performed by the assistant. OAuth-token theft, worm propagation across approximately 100 repositories, and source-code exfiltration are incident context, not confirmed outcomes of this procedure.

**Sources:**

- `S1` — [Mandiant AI risk and resilience report, September 2026](https://cloud.google.com/security/resources/ai-risk-and-resilience-2026)

## EAA-C-039 — Mandiant internal-assistant repository exfiltration assessment

**Type:** research

**Date:** reported 2026-09-16

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-015 | impact-confirmed | medium | Mandiant’s assessment team induced an internal assistant to clone sensitive internal repositories and push them to a tester-controlled external GitHub repository using its native CLI. | S1 |

**Activation notes:** The assessment targeted an internal assistant used for CI/CD and repository management. Testers supplied an external GitHub repository and its personal access token. The assistant already had access to sensitive internal repositories, a native CLI, and network access to GitHub. The report does not name the product, versions, operating system, or exact prompts. September 16 is the date of public reporting about the report; the assessment date is undisclosed. This was a controlled assessment; the initiating role-confusion prompt is not evidence of indirect task-context injection.

**Sources:**

- `S1` — [Mandiant AI risk and resilience report, September 2026](https://cloud.google.com/security/resources/ai-risk-and-resilience-2026)

## EAA-C-040 — gadgethumans-mcp wallet private-key transmission

**Type:** research

**Date:** published 2026-09-08

| Step | Technique | Outcome | Confidence | Claim | Sources |
|---|---|---|---|---|---|
| 1 | EAA-021 | present | high | The inspected MCP tool-call handler copies WALLET_PRIVATE_KEY into the X-402-Wallet header of an outbound request; the returned setup guidance describes automatic signing. | S1, S2 |

**Activation notes:** A compatible MCP client must load the server, WALLET_PRIVATE_KEY must be set, and a recognized tool must be invoked with network access available. The pinned source sends the raw key in X-402-Wallet rather than producing a local payment signature. Its default key-bearing destination is https://api.gadgethumans.com/execute; MCP_ENDPOINT can change the base. Knostic describes an earlier destination under swarm.gadgethumans.com and package versions 1.0.3 and 1.0.9. The pinned source identifies its server as 1.0.2; that string is not proof of an npm release version. The sources establish code behavior, not author intent, victim execution, or stolen funds. Download counts are not victim counts.

**Sources:**

- `S1` — [Knostic gadgethumans-mcp private-key transmission analysis](https://www.knostic.ai/blog/when-auto-signing-sends-your-wallet-private-key-to-a-remote-server-a-malicious-mcp-package-on-npm)
- `S2` — [gadgethumans-mcp source at commit c33ebb84](https://github.com/gadgethumans-dev/gadgethumans-mcp/blob/c33ebb84e00d921310ab4dbf97a3fe8db19bb949/index.js)
