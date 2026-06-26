# Candidates

Plausible ideas that are not yet catalog entries.

Candidates are worth tracking, but they should not sit beside observed or documented techniques until there is stronger public evidence.

## EAA-C001 — Runtime preload into agent process

A local attacker may be able to abuse runtime-level preload or loader features so code runs inside the agent process before the agent starts normal work.

For Node/Electron-style agents, this could involve environment or runtime options that preload modules, alter module resolution, attach loaders, or change certificate/proxy behavior. For Python-based agents, similar issues could come from import-path or startup-hook manipulation. The interesting part is not the generic preload trick; it is that the code may run under a trusted local agent process that normally touches prompts, tool results, project files, provider credentials, and local integrations.

Why it matters:

- agent processes are expected to read sensitive project context;
- injected code may inherit the same environment, network path, and local auth material;
- activity may blend into a process users and defenders already expect to be active.

Why it is not promoted yet:

I have not found a public, agent-specific incident or research case showing runtime preload against Claude Code, Gemini CLI, Codex, Cursor, Kiro, Windsurf, or similar local agents. Generic runtime preload is real; the catalog needs stronger evidence for this specific endpoint-agent framing.

## EAA-C002 — Live agent process memory read or injection

A local attacker may target a running agent process to read memory, tamper with runtime state, inject code, or hijack local control channels.

The potential target data is agent-specific: prompts, tool results, transient secrets, provider tokens, MCP session state, local auth material, conversation context, or decrypted configuration. The potential benefit is stealth and context: the attacker is not merely stealing a file, but reaching into a process already trusted to handle sensitive local agent activity.

Why it matters:

- endpoint agents may hold useful state that is not available on disk;
- memory access can bypass file-based monitoring;
- malicious activity may be harder to triage if it occurs in or around a trusted agent process.

Caveats:

- same-user memory access is constrained by OS protections, sandboxing, hardened runtime, integrity levels, TCC, ptrace settings, EDR, and process architecture;
- this is not automatically easier than stealing files or modifying config;
- many realistic attacks would still need local code execution first.

Why it is not promoted yet:

Adjacent campaigns have scraped memory from trusted processes, but I have not found public evidence of local AI agent process memory being targeted specifically. Keep this as a candidate until agent-specific evidence appears.
