# Sources

Only sources directly used by the catalog are listed. Incident and artifact reporting supports the procedure actually observed in that source; it does not automatically prove every later activation or impact stage. Controlled research supports feasibility for the tested product and version, not in-the-wild use or current-version exploitability.

## Incidents / malicious artifacts

- Nx s1ngularity postmortem — https://nx.dev/blog/s1ngularity-postmortem
- Snyk analysis of Nx agent abuse — https://snyk.io/blog/weaponizing-ai-coding-agents-for-malware-in-the-nx-malicious-package/
- Aqua Trivy VS Code extension advisory — https://github.com/aquasecurity/trivy-vscode-extension/security/advisories/GHSA-8mr6-gf9x-j8qg
- Socket.dev Trivy extension write-up — https://socket.dev/blog/unauthorized-ai-agent-execution-code-published-to-openvsx-in-aqua-trivy-vs-code-extension
- StepSecurity Mini Shai-Hulud — https://www.stepsecurity.io/blog/a-mini-shai-hulud-has-appeared
- StepSecurity Miasma repository injection — https://www.stepsecurity.io/blog/miasma-worm-hits-microsoft-again-azure-functions-action-and-72-other-repositories-disabled-after-supply-chain-attack-targeting-ai-coding-agents
- StepSecurity Miasma Phantom Gyp — https://www.stepsecurity.io/blog/binding-gyp-npm-supply-chain-attack-spreads-like-worm
- StepSecurity Hades campaign — https://www.stepsecurity.io/blog/the-hades-campaign-pypi-packages
- StepSecurity Immobiliare Labs compromise — https://www.stepsecurity.io/blog/immobiliarelabs-npm-packages-compromised
- OALABS copied-agent and transcript-tampering investigation — https://research.openanalysis.net/claude/codex/hacking/ai%20hacking/llm/redteam/policy%20violation/2026/06/16/compromised-claude-hacking.html

## Vendor documentation and advisories

- Claude Code memory — https://code.claude.com/docs/en/memory
- Claude Code hooks — https://code.claude.com/docs/en/hooks
- Claude Code settings — https://code.claude.com/docs/en/settings
- Claude Code environment variables — https://code.claude.com/docs/en/env-vars
- Claude Code skills — https://code.claude.com/docs/en/skills
- Claude Code plugins — https://code.claude.com/docs/en/plugins
- Claude Code plugins reference — https://code.claude.com/docs/en/plugins-reference
- Claude Code plugin discovery and security — https://code.claude.com/docs/en/discover-plugins
- Claude Code MCP — https://code.claude.com/docs/en/mcp
- Claude Code monitoring and OpenTelemetry — https://code.claude.com/docs/en/monitoring-usage
- Claude Code bypass-permissions workspace-trust advisory, CVE-2026-33068 — https://github.com/anthropics/claude-code/security/advisories/GHSA-mmgp-wc2j-qcv7

## Controlled research

- Trail of Bits MCP line-jumping — https://blog.trailofbits.com/2025/04/21/jumping-the-line-how-mcp-servers-can-attack-you-before-you-ever-use-them/
- Invariant Labs MCP injection experiments — https://github.com/invariantlabs-ai/mcp-injection-experiments
- Cisco persistent Claude Code memory compromise — https://blogs.cisco.com/ai/identifying-and-remediating-a-persistent-memory-compromise-in-claude-code
- Check Point Claude Code project-file research, CVE-2025-59536 and CVE-2026-21852 — https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/
- Mitiga MCP endpoint rewrite and token interception — https://www.mitiga.io/blog/claude-code-mcp-token-theft-mitm
- Dash Security Claude Code Remote Control as C2 — https://dash.security/blog/living-off-coding-agents-claude-as-a-c2-server
- Bloom Security Claude Code OpenTelemetry redirection — https://bloom.security/blog/welcome-to-otel-claudeifornia
- Adversa AI SymJack agent-mediated configuration overwrite — https://adversa.ai/blog/the-approval-prompt-is-lying-to-you-symlink-rce-in-five-ai-coding-agents-claude-code-cursor-antigravity-copilot-grok-build/
