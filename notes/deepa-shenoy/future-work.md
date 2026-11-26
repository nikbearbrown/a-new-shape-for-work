# Future work I'd like to help with

Proposals, not commitments. Each would get its own issue and branch once Nik agrees. Ordered by how directly it follows from `findings.md`.

| # | Work | Why (where the repo asks for it) | What I would deliver |
| --- | --- | --- | --- |
| 1 | **Title-match validation** | The manuscript calls validating title links "the immediate priority" ([Section 5, line 110](https://github.com/nikbearbrown/a-new-shape-for-work/blob/main/paper/manuscript.md#L110)). | Act as a human reviewer on the replication queue, starting with titles. I have already read the draft tags, so I can review but not tag independently. |
| 2 | **Missing joins shown separately** | Section 3.5 says future versions should show missing joins separately from matched zero scores ([line 66](https://github.com/nikbearbrown/a-new-shape-for-work/blob/main/paper/manuscript.md#L66)). | Report unmatched tasks as "unavailable" rather than zero, with each occupation's share of unavailable task weight shown on the dashboard. Follows finding 3. |
| 3 | **Phase by purpose for data work** | METHOD.md flags "Analyzing Data or Information" (tagged Understand) as contested; CONTRIBUTING gives it as the example of a task whose phase depends on purpose. | From my own analyst roles: analysis sometimes informs a decision (Understand) and sometimes is the deliverable (Produce). Re-run the activity profiles for data occupations with alternative labels, from public O*NET data, and report before/after shares. |
| 4 | **Automated consistency checks** | Figures appear in the paper, dashboard, README and CSVs, and can drift apart. | Turn `verify_findings.py` into a check that runs whenever the deposit is rebuilt. |
| 5 | **A small reader test of the dashboard** | The manuscript says the screenshots are "not evidence from a user evaluation" ([line 39](https://github.com/nikbearbrown/a-new-shape-for-work/blob/main/paper/manuscript.md#L39)). | Ask a few people what they think a chart says, to check that "estimated" and "not hours" come across. |
| 6 | **Worker evidence** | The manuscript says the strongest test would compare job ads, worker accounts and task diaries ([line 112](https://github.com/nikbearbrown/a-new-shape-for-work/blob/main/paper/manuscript.md#L112)). | Help pilot a small task-diary study for data occupations, if Nik thinks it is worth doing and with whatever approval research with people needs. Results would be anonymous and reported only as aggregates. |

## What I need

- The per-occupation phrase counts from the cluster run (`data/postings/by-occupation.json.gz`, counts only, no ad text), to measure the clearance fix in finding 2 exactly.
