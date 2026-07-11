# Candidates

Plausible ideas that are not yet catalog entries.

Candidates are worth tracking, but they should not sit beside catalog techniques until they meet the promotion rules in [`evidence.md`](evidence.md).

## EAA-C001 — Runtime code preload into an agent process

A local attacker may be able to abuse language-runtime or operating-system loader features so attacker code runs inside an agent process before normal agent work begins.

For Node/Electron-style agents, this could involve runtime options that preload modules or attach loaders. Python-based agents have analogous import-path and startup-hook mechanisms. Certificate, proxy, and API-endpoint manipulation belongs under EAA-007 unless it also causes code to load inside the agent process.

This candidate assumes that the attacker can already influence the agent's launch environment, executable resolution, or runtime files. That prerequisite is often close to ordinary same-user code execution. The research question is therefore not whether generic preloading works, but whether running inside a named agent process produces a distinct security or forensic advantage.

Why it matters:

- agent processes are expected to read sensitive project context;
- injected code may observe transient in-process state or inherit the same environment and network path;
- activity may blend into a process users and defenders already expect to be active.

Questions to answer before promotion:

- Does the preload expose agent-specific state that is not already available through files, environment variables, or ordinary same-user access?
- Does it cross a meaningful boundary such as a sandbox, OS privacy grant, process allowlist, or agent-specific credential store, rather than merely sharing a process name?
- Is the behavior reproducible on a named product, version, operating system, and installation type?
- Which process, module-load, file, and network artifacts distinguish the injected run from a normal agent session?

Why it is not promoted yet:

No public, agent-specific incident or reproducible demonstration is currently cited for runtime preloading Claude Code, Gemini CLI, Codex, Cursor, Kiro, Windsurf, or a similar local agent. Promote this only after a product-specific demonstration shows an agent-specific gain beyond generic same-user code execution.

## EAA-C002 — Live agent process memory access or tampering

A local attacker may target a running agent process to read memory or alter runtime state. Process-memory read, process-memory write or code injection, debugger attachment, and local control-channel hijacking are different procedures with different prerequisites and should be evaluated separately.

Potential target data includes prompts, tool results, transient secrets, provider tokens, MCP session state, conversation context, or decrypted configuration. These values are not guaranteed to reside in readable process memory: they may be held in another process, an OS credential store, encrypted storage, or short-lived buffers. A demonstration must identify the actual data location rather than infer it from product features.

Why it matters:

- endpoint agents may hold useful state that is not available on disk, although this must be measured;
- memory access can bypass file-based monitoring;
- malicious activity may be harder to triage if it occurs in or around a trusted agent process.

Caveats:

- same-user memory access is constrained by OS protections, sandboxing, hardened runtime, integrity levels, TCC, ptrace settings, EDR, and process architecture;
- this is not automatically easier than stealing files or modifying config;
- many realistic attacks would already require local code execution or elevated debugging rights;
- success for memory reading does not establish feasibility of state tampering, code injection, or control-channel hijacking.

Questions to answer before promotion:

- Which agent-specific values are recoverable from memory but absent from ordinary on-disk or environment acquisition?
- Can tampering change a tool decision, approval state, model request, or audit record in a controlled and repeatable way?
- Does the technique produce an agent-specific privilege, stealth, or attribution advantage over direct same-user actions?
- What independent endpoint artifacts remain after native agent evidence is modified or absent?

Why it is not promoted yet:

Adjacent campaigns that scrape other trusted processes do not establish agent-specific feasibility. Keep this as a candidate until a named product and version are tested reproducibly. If promoted, split memory collection, runtime tampering, and control-channel hijacking into separate techniques rather than treating one result as proof of all three.
