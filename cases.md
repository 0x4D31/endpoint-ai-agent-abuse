# Cases

Cases map public incidents, malicious artifacts, and research-reported classes to EAA techniques.

## Nx s1ngularity

**Type:** observed incident  
**Techniques:** EAA-001, EAA-002, EAA-015, EAA-016

Malicious npm packages discovered local AI agents and used available agents for semantic filesystem reconnaissance. Conventional malware handled collection and exfiltration.

Sources: [Nx postmortem](https://nx.dev/blog/s1ngularity-postmortem), [Snyk analysis](https://snyk.io/blog/weaponizing-ai-coding-agents-for-malware-in-the-nx-malicious-package/)

## Trivy OpenVSX extension

**Type:** malicious artifact  
**Techniques:** EAA-001, EAA-002, EAA-015, EAA-016

A compromised VS Code extension attempted to launch several local agents in permissive modes and use local authenticated tooling.

Sources: [Aqua advisory](https://github.com/aquasecurity/trivy-vscode-extension/security/advisories/GHSA-8mr6-gf9x-j8qg), [Socket write-up](https://socket.dev/blog/unauthorized-ai-agent-execution-code-published-to-openvsx-in-aqua-trivy-vs-code-extension)

## Mini Shai-Hulud

**Type:** observed incident / malicious package payload  
**Techniques:** EAA-003

A malicious package payload planted Claude Code `SessionStart` hook persistence.

Source: [StepSecurity write-up](https://www.stepsecurity.io/blog/a-mini-shai-hulud-has-appeared)

## Miasma repo injection

**Type:** observed incident / malicious repository payload  
**Techniques:** EAA-003, EAA-004, EAA-006, EAA-014, EAA-016

A malicious commit planted configuration files that executed a credential-harvesting payload when opened in Claude Code, Gemini CLI, Cursor, or VS Code.

Source: [StepSecurity write-up](https://www.stepsecurity.io/blog/miasma-worm-hits-microsoft-again-azure-functions-action-and-72-other-repositories-disabled-after-supply-chain-attack-targeting-ai-coding-agents)

## Miasma Phantom Gyp

**Type:** observed incident / malicious package payload  
**Techniques:** EAA-003, EAA-004, EAA-014

A package-install payload injected AI coding assistant configuration files such as Claude Code hooks, Cursor rules, Gemini settings, and VS Code folder-open tasks into repositories reachable by stolen GitHub tokens.

Source: [StepSecurity write-up](https://www.stepsecurity.io/blog/binding-gyp-npm-supply-chain-attack-spreads-like-worm)

## Hades

**Type:** observed incident / malicious packages  
**Techniques:** EAA-004, EAA-014, EAA-016

Payloads walked workspace trees and targeted many assistant/rule/config surfaces.

Source: [StepSecurity write-up](https://www.stepsecurity.io/blog/the-hades-campaign-pypi-packages)

## MCP injection and rug-pull research

**Type:** public research  
**Techniques:** EAA-006, EAA-010

Research showing tool-description injection, dynamic tool mutation, and post-approval tool drift in MCP-style systems.

Sources: [Trail of Bits line-jumping](https://blog.trailofbits.com/2025/04/21/jumping-the-line-how-mcp-servers-can-attack-you-before-you-ever-use-them/), [MCP injection experiments](https://github.com/invariantlabs-ai/mcp-injection-experiments)

## Memory poisoning research

**Type:** public research / documented class  
**Techniques:** EAA-004

Research and defensive work around persistent memory poisoning. This supports the class; it is not evidence that `MEMORY.md` abuse has been seen in malware.

Source: [OWASP Agent Memory Guard](https://github.com/OWASP/www-project-agent-memory-guard)
