# Evidence

Catalog entries need a public anchor.

| Label | Meaning |
|---|---|
| `observed` | Reported in a real incident or campaign. |
| `malicious-artifact` | Present in malicious code, package, extension, or repo. |
| `documented-surface` | Official docs prove the local surface exists. Abuse may still be theoretical. |
| `research` | Credible public research demonstrates the mechanism. |
| `candidate` | Plausible, but not enough public evidence for the catalog. |

## Rules

- `documented-surface` is enough when the local agent surface is explicit and abuse follows directly from it.
- If the surface exists but agent-specific abuse is unclear, keep it in [`candidates.md`](candidates.md).
- Do not promote a technique just because it is clever or likely.
- Keep wording conservative: separate what was observed from what is possible.
