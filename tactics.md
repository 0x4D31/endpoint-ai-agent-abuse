# Tactics

Tactics describe **why** an adversary performs an endpoint-agent technique. They are independent of the affected [`surface`](surfaces.md), and a technique can support more than one tactic.

| Tactic | Objective | Techniques |
|---|---|---|
| Discovery | Learn which agents, configuration, tools, state, or authority are available. | EAA-016 |
| Execution | Cause an agent, hook, plugin, helper, or connected tool to perform an attacker-selected action. | EAA-001, EAA-002, EAA-003, EAA-006, EAA-008, EAA-009, EAA-010, EAA-011, EAA-012, EAA-013, EAA-015 |
| Persistence | Make attacker-controlled behavior or context survive a turn, reload, session, restart, or project change. | EAA-003, EAA-004, EAA-006, EAA-009, EAA-013, EAA-014 |
| Credential Access | Obtain credentials, tokens, or authentication material. | EAA-005 |
| Collection | Gather agent state, local data, tool context, or other information of interest. | EAA-005, EAA-007, EAA-010, EAA-012, EAA-015 |
| Exfiltration | Move collected data or agent context to an attacker-controlled or unapproved destination. | EAA-007, EAA-010, EAA-012, EAA-015 |
| Defense Evasion | Reduce visibility, select a less-monitored profile, or alter evidence used for investigation. | EAA-008, EAA-017 |

## Modeling rules

- Tactics describe objectives; they do not imply that impact was achieved.
- Assign only tactics supported by the technique definition. Record case-specific objectives in procedure data rather than expanding the generic technique.
- Discovery of an authenticated integration is different from using that integration. The first is EAA-016; the latter may be EAA-015.
- Collection and exfiltration are separate. Reading a transcript does not prove that its contents left the endpoint.
- EAA-005 has Credential Access only when the collected agent state contains credentials, tokens, or authentication material. Do not infer credential access from transcript collection alone.
- Defense-evasion findings require corroboration. Missing native evidence can result from normal retention, disabled persistence, crashes, or collection gaps.
