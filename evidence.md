# Evidence model

Every catalog entry needs a public anchor, but the kind of source and the maturity of a technique are separate facts. A malicious artifact can demonstrate a technique without proving that it executed on a victim. An incident report can confirm execution without confirming every claimed downstream impact.

## Technique maturity

| Maturity | Meaning | Minimum requirement |
|---|---|---|
| `feasible` | A product surface and an agent-specific abuse path are publicly established, but no public implementation is known. | Official documentation, product source, or another authoritative description of the required behavior. |
| `demonstrated` | Public research or a malicious artifact implements the technique. This does not by itself prove victim-side execution. | Reproducible research, a public proof of concept, or inspectable malicious code/configuration. |
| `observed` | A public incident or campaign report establishes that the technique's scoped attacker action occurred in a real environment. | An incident-context case maps the technique to `planted`, `executed`, or `impact-confirmed`. `present` and `attempted` are insufficient. |

Maturity follows the action in the technique definition, not an assumed downstream result. For a hook-planting technique, an incident-confirmed hook write can support `observed` even when no public evidence shows that the hook later fired. The entry and case must state that limit explicitly.

`candidate` is not a maturity value. Ideas that do not yet meet the `feasible` threshold stay in [`candidates.md`](candidates.md).

## Evidence source types

Technique and case records may cite more than one source type. Classify what the cited URL is, not what claim it is being used to support; outcome and support-claim fields carry the latter meaning.

| Source type | What it establishes |
|---|---|
| `official-documentation` | A vendor documents the feature, configuration, default, or security boundary. |
| `primary-artifact` | Source code, a vendor advisory, package, extension, commit, configuration, log, or other directly inspectable primary material. |
| `reproducible-research` | Public research provides enough product/version detail or a proof of concept to validate the mechanism. |
| `malicious-artifact` | The cited source is the malicious code, configuration, package, extension, or another directly inspectable malicious artifact. A report describing an artifact is not itself a malicious artifact. |
| `incident-report` | A first-party or investigating organization reports activity in a real incident or campaign. |
| `secondary-analysis` | Reporting or analysis interprets primary material. Use it to supplement, not replace, an available primary source. |

## Evidence support claims

Each structured evidence assertion binds one source to one support claim and one confidence value. Do not treat a source citation as support for every stage of a procedure.

| Support claim | What the cited source establishes |
|---|---|
| `surface-documented` | The required product feature, configuration, default, or security boundary is documented. |
| `mechanism-demonstrated` | A public implementation or controlled test establishes the abuse mechanism, without by itself assigning a case outcome. |
| `artifact-present` | The relevant code or configuration is present in an inspected artifact. |
| `procedure-planted` | The procedure was written or deployed to its target surface. |
| `execution-attempted` | Invocation or activation was initiated, but successful execution is not established. |
| `execution-confirmed` | The scoped procedure ran in the stated incident, advisory, or controlled-research context. |
| `impact-confirmed` | The stated downstream result was confirmed in that context. |

## Procedure outcomes

Cases describe what happened at each step. Use the most specific supported outcome:

| Outcome | Required technique-evidence support | Meaning |
|---|---|---|
| `present` | `artifact-present` | The relevant code or configuration exists in an artifact. |
| `planted` | `procedure-planted` | The attacker or payload wrote/deployed it to the target surface. |
| `attempted` | `execution-attempted` | Invocation or activation was attempted, but successful execution is not established. |
| `executed` | `execution-confirmed` | The procedure ran in the target environment. |
| `impact-confirmed` | `impact-confirmed` | A downstream result such as collection, exfiltration, persistence, or SaaS action is confirmed. |

Every source cited by a case step must carry the matching support assertion for that technique in the structured catalog. Source presence alone is insufficient. This keeps a case outcome from silently exceeding the claim-level evidence used to support it.

Do not infer a later outcome from an earlier one. In particular:

- malicious code containing an agent command establishes `present`, not necessarily `executed`;
- a planted project hook establishes `planted`, not necessarily that the hook fired;
- an attempted authenticated action does not establish successful access or exfiltration;
- an absent transcript is an evidence gap, not proof of deletion or tampering.

## Confidence

| Confidence | Meaning |
|---|---|
| `high` | Direct artifact, telemetry, or independently corroborated reporting supports the claim. |
| `medium` | The source supports the claim, but an important artifact, product detail, or outcome is unavailable. |
| `low` | A source asserts the behavior, but the public material is insufficient to validate it independently. |

Confidence applies to a specific evidence-to-claim assertion or case step, not to an entire technique or campaign by default. In structured data, each evidence assertion records confidence in its support claim. Case steps record confidence separately because a source can strongly establish artifact presence while leaving activation or impact uncertain. A case step's confidence must not exceed the strongest matching source/support assertion cited by that step.

## Inclusion and promotion rules

- Promote a candidate to `feasible` only when the agent-specific mechanism, prerequisites, and security consequence are concrete.
- Promote to `demonstrated` only with public research, a proof of concept, or an inspectable artifact that implements the mechanism.
- Promote to `observed` only when an incident-context case establishes that the scoped attacker action was planted, executed, or produced confirmed impact. Do not use artifact presence or an unconfirmed attempt.
- Record product, version, operating system, configuration scope, trust/approval gate, and activation event whenever they affect feasibility.
- Prefer official documentation and primary artifacts. Use secondary reporting to add context, not as a substitute when primary evidence is available.
- Map cases at the procedure-step level. Do not map a whole case to every technique that appears theoretically possible.
- Separate attacker action from product behavior. For example, environment expansion is product behavior; attacker-controlled interpolation is the abuse procedure.
- Separate state presence, activation, execution, and impact in both prose and structured data.
- Date-stamp negative claims such as “no known public campaign” and recheck them before a release.
- Treat mutable documentation as version-sensitive. Record a `verified_on` date and the tested or affected version when known.
- Keep wording conservative when vendors and researchers disagree about a security boundary. Describe the demonstrated behavior, prerequisites, version, and vendor position without silently choosing a characterization.

## Entry checklist

Before adding or changing a technique, verify that the entry answers:

1. What exact attacker action is the technique?
2. Which endpoint-agent surface is affected, and what is the adversary's objective?
3. What access, trust decision, configuration, or product state is required?
4. What triggers activation?
5. Which products, versions, and operating systems are actually supported by the sources?
6. What was present, attempted, executed, and impact-confirmed?
7. Which source supports each material claim?
8. What telemetry could distinguish the behavior from legitimate use?
9. What common false positives and evidence gaps remain?
