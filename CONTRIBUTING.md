# Help write A New Shape for Work

We have a [rough first draft](paper/manuscript.md), a working prototype, and [data you can download](research-data/). We're looking for collaborators who can improve the argument, check the evidence, or tell us where our model of an occupation misses the work. You don't need to code, have cluster access, or review the whole paper to help.

**If you have an hour:** read one section and [open an issue](https://github.com/nikbearbrown/a-new-shape-for-work/issues/new) with one claim you would keep, change, or qualify. Name the section, explain why, and include a source or example if you have one. For a copy edit, you can also propose the wording directly in a pull request.

## Pick a way to help

| Contribution | Where to start | What to send |
|---|---|---|
| **Review or write a section** | [Rough manuscript](paper/manuscript.md) | Identify a missing argument, alternative explanation, or claim the data don't support. For a larger addition, open an issue first with a short outline so people can coordinate. |
| **Check a citation or add literature** | The manuscript's related work and references | Give a primary source link, page or table, and the claim it supports or contradicts. Worker interviews, task diaries, and time-use studies are particularly useful. Tell us which population and years the source covers. |
| **Review an occupation you know** | [Methods](docs/METHOD.md) and [work-activity tags](tags/dwa-phase-tags.tsv) | Name the occupation and code if known. Pick a task and explain when it belongs in a different phase. For example, analyzing data might help someone decide what to do, or it might be the deliverable. State when your example applies. |
| **Reproduce a result** | [Data deposit](research-data/) and [gathering guide](docs/GATHERING-DATA.md) | Pick one number or figure. Report the data version, method, numerator and denominator, expected and observed values, and how to reproduce the comparison. Null and negative results are useful. |
| **Audit title matches or skill phrases** | [Title decisions](tags/title-decisions.tsv), [skill-phrase tags](tags/skill-phrase-phase-tags.tsv) | Give a reason and evidence. If a title means different things in different settings, document the ambiguity rather than forcing a single code. |
| **Improve the prototype or data tooling** | [Dashboard](page/) and [build instructions](README.md#reproduce-the-prototype) | Explain what a reader or researcher can do better after the change. If it changes a published number, show the old and new numbers and why they differ. |

## What makes a review useful

- **Start with a specific claim, file, or row.** Show the evidence, and say what you would change. A short issue is enough; you do not have to submit a patch.
- **Keep the measures separate.** A modeled activity share is not working time, a share of diagnostic mentions is not a share of ads, and the Claude-based overlay does not measure all AI use or job loss.
- **Use the review fields.** For a checked tag, add your reason in `note`, mark it `reviewed`, and put your GitHub handle in `reviewed_by` where that field exists. Checked rows that stay unchanged are useful too. Keep unverified suggestions marked `draft`.
- **Protect the source material.** Do not post raw job ads, job-description text, per-posting rows, or identifiable worker examples. Cite the source and version; submit aggregates and redistributable evidence. See [data credits and rights](research-data/README.md#source-versions-and-rights).

## How to submit

For a discussion, open an issue with the section or finding, your evidence, and a proposed next step. For an edit, fork, branch, and open a focused pull request. Say what you changed and how you checked it. Keep manuscript, tag, and code changes separate when they can be reviewed independently. If you use an AI-generated answer, verify the citations and claims before submitting it.

If you want to collaborate on the paper beyond a single contribution, open an issue describing what you'd like to take on. Authorship is not yet decided. Discuss authorship or acknowledgment early if you plan to contribute substantial writing or research; sending an issue or pull request does not settle authorship.

## Licence

Code is MIT ([LICENSE](LICENSE)); project data, tags, documentation and screenshots are CC BY 4.0 ([LICENSE-CC-BY.md](LICENSE-CC-BY.md)). Upstream data retains its own terms. By opening a pull request you agree that your contribution is licensed under the applicable project licence.
