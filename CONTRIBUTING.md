# Help write A New Shape for Work

We have a [rough first draft](paper/manuscript.md), a working prototype, and [data you can download](research-data/). We're looking for collaborators who can improve the argument, check the evidence, or tell us where our model of an occupation misses the work. You don't need to code, have cluster access, or review the whole paper to help.

**If you have an hour:** read one section and [open an issue](https://github.com/nikbearbrown/a-new-shape-for-work/issues/new) with one claim you would keep, change, or qualify. Name the section, explain why, and include a source or example if you have one. For a copy edit, you can also propose the wording directly in a pull request.

## Getting started

Follow these steps in order. Steps 1 to 3 get you access. Steps 4 to 8 take one contribution from start to finish.

1. **Read first.** Read the [README](README.md), then the [working draft](paper/manuscript.md). Allow about an hour. You don't need to follow every detail, but you should know what the paper claims and what it does not.
2. **Choose one thing to do.** Pick one row from the table under [Pick a way to help](#pick-a-way-to-help), and narrow it to one section, one occupation, one source or one result. If you can't decide, review one section of the draft.
3. **Email Nik** at bear@bearbrown.co with the subject "A New Shape for Work: contributor". Include:
   - your name and your GitHub username;
   - the contribution you chose and what exactly you will look at;
   - whether you hope to become an author or want to help without authorship.

   Nik will add you to the repository as a collaborator. GitHub then emails you an invitation, which you must accept within seven days.
4. **Claim the work.** Check the [open issues](https://github.com/nikbearbrown/a-new-shape-for-work/issues) to make sure nobody is already doing it. Then [open an issue](https://github.com/nikbearbrown/a-new-shape-for-work/issues/new) that says what you are taking on, and assign it to yourself.
5. **Make a branch.** Clone the repository and create a branch named `your-name/short-description`, for example `priya/qa-tester-phase-tags`. Do not commit to `main`. If you don't use git, edit the file on GitHub with the pencil button and choose "Create a new branch" when you save.
6. **Do the work.** Follow the "What to send" column for the row you chose. Keep one branch to one piece of work.
7. **Open a pull request.** Say what you changed, how you checked it, and where you used an AI tool. Write "Closes #" and your issue's number so the two are linked, and request a review from `nikbearbrown`.
8. **Respond to the review.** Nik or another author will comment. Revise on the same branch until it is agreed, and it will be merged.
9. **Keep your record.** Your issues and pull requests are the record of what you did. If you hope to be an author, keep a list of them, because the paper's contribution statement is drawn from it.
10. **Take the next step.** Pick another piece of work. If you want to be an author, tell Nik early and read [Credit and what we expect from authors](#credit-and-what-we-expect-from-authors).

You can also help without access. Anyone can open an issue on this repository without emailing first.

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

**Running an AI agent on it?** Use [replication/](replication/) instead of editing `tags/`. The agent tags a list on its own, without seeing the repository's draft or anyone else's answers, and hands in a folder; the comparison across models then tells reviewers where to look first.

## How to submit

For a discussion, open an issue with the section or finding, your evidence, and a proposed next step. For an edit, open a focused pull request from a branch (collaborators) or from a fork (everyone else). Say what you changed and how you checked it. Keep manuscript, tag, and code changes separate when they can be reviewed independently. If you use an AI-generated answer, verify the citations and claims before submitting it.

If you want to collaborate on the paper beyond a single contribution, open an issue describing what you'd like to take on, and read [Credit and what we expect from authors](#credit-and-what-we-expect-from-authors) first.

## Credit and what we expect from authors

The author list isn't decided yet. We follow [Yale's guidance on authorship](https://provost.yale.edu/policies/academic-integrity/guidance-authorship-scholarly-or-scientific-publications). Under it, an author has done **all four** of these:

1. **Contributed to a component of the work:** its conception, design, conduct, analysis, or interpretation of at least part of the results.
2. **Helped write the paper:** drafted part of it, or revised it for substance, not just copy edits.
3. **Approved the final version** before submission.
4. **Agreed to be accountable** for the work, including helping answer questions about its accuracy or integrity.

Some contributions are valuable but don't by themselves make someone an author: a single issue or copy edit, helping collect or assemble data, or reviewing a finished draft to offer suggestions. Everyone who contributes that way is thanked by name in the acknowledgments, unless they ask not to be. To be an author, take on a component, such as reproducing a result, auditing a whole set of tags or title matches, or testing the method on an occupation family you know, and then do the writing, approval and accountability steps too. An AI model can't be an author, since it can't approve the paper or answer for it.

If you want to be an author, we expect you to:

- **Read the whole paper,** not just your section. You're putting your name on all of it.
- **Think about it, then give feedback.** Does the method answer the question? Are the comparisons fair? Do the figures show what the text claims, and would a different figure show it better? Do the numbers in the text match the tables, figures and data?
- **Suggest changes when they matter.** Don't make a suggestion just to have made one. If you find nothing to change, say so; that's a useful answer. A real problem, raised clearly with a proposed fix, is the most valuable thing you can give.
- **Disclose AI assistance.** AI tools are fine for code and drafting, but say where you used them. You stay accountable for everything you contribute.
- **Keep a record of what you did:** what, when, and where it lives (issue, pull request, commit, figure). The paper's contribution statement is drawn from it and lists each author's [CRediT roles](https://credit.niso.org/).
- **Sign off only when you can stand behind it.** Before submission, every author confirms in writing that they have read the full paper, agree with it, and accept accountability for it. If something is wrong or unclear, say so before approval, not after publication.

Raise authorship early, and we'll revisit it as roles change. Author order follows contribution. If you think your work merits authorship and it isn't reflected, say so before the final draft. Sending an issue or pull request does not by itself settle authorship.

## Licence

Code is MIT ([LICENSE](LICENSE)); project data, tags, documentation and screenshots are CC BY 4.0 ([LICENSE-CC-BY.md](LICENSE-CC-BY.md)). Upstream data retains its own terms. By opening a pull request you agree that your contribution is licensed under the applicable project licence.
