# Contributing

This is a first pass at the data behind a paper, *A New Shape for Work: How AI is Affecting Jobs*. Most of what it needs now is people checking judgments, not new code. Every phase tag and title decision in `tags/` is an unreviewed draft, and a reviewed tag is worth more to the paper than a new chart.

Start with [docs/METHOD.md](docs/METHOD.md) (what the analysis does and where it breaks) and the screenshots in the [README](README.md).

## Ways to help

You can do the first five without any special access: clone the repo, read a TSV, and open a pull request.

| Task | Where | What a good contribution looks like |
|---|---|---|
| **Review phase tags** for an occupation you know | `tags/dwa-phase-tags.tsv` (2,087 detailed work activities), `tags/iwa-phase-tags.tsv` (332 intermediate) | Change `phase` where it is wrong, put your reason in `note`, set `status` to `reviewed` and your GitHub handle in `reviewed_by`. Rows you checked and left alone count too: mark them reviewed. |
| **Decide ambiguous job titles** | `tags/title-decisions.tsv`; the list of high-volume unassigned titles is in docs/GATHERING-DATA.md, step 7 | One row per title: the O*NET occupation code it mostly means in job postings (or `-` to exclude it), and why. |
| **Check the skill-phrase tags** | `tags/skill-phrase-phase-tags.tsv` | Flag phrases that are boilerplate or tagged to the wrong phase. The rules that produce them are `PHRASE_RULES` in `scripts/build_postings.py`. |
| **Fix the title normaliser** | `cluster/title_norm.py` | Known gap: titles ending in "-ft" or "-pt" (full-time, part-time) are not cleaned, so "sales associate-ft" matches nothing. |
| **Improve the page** | `page/index.html` | Plain HTML and D3 reading three JSON files; serve `page/` with any static server. After a visible change, run `scripts/take_screenshots.py` so the README stays current. |
| **Run the posting extraction** | `cluster/`, docs/GATHERING-DATA.md steps 4–6 | Needs an account on Northeastern's Explorer cluster, where the posting archives live. The extractor is plain Python, so it can be adapted to another allow-listed posting dataset. |

If you are unsure where to start, open an issue that names an occupation you know well, and review its tags.

## Rules

- **Judgments live in `tags/`, each with a reason.** A tag without a reason will not be merged. Leave `status` as `draft` unless you have checked the row yourself.
- **No posting text in the repo.** Commit counts and shares only, never job-description text or per-posting rows. The cluster jobs are built so that only counts leave the cluster.
- **Only openly licensed posting data** (CC0, CC BY, ODC-By, MIT, Apache 2.0). Say which dataset and version you used.
- **Downloaded and intermediate files stay out of git.** `source/` and `data/` are ignored; `scripts/fetch_sources.sh` and the build scripts recreate them.
- **Label estimates as estimates.** Effort figures are models built from O*NET's ordinal ratings, not measured time, and the page says so on every effort chart.
- **AI coverage is observed use, not capability or job loss.** Keep that wording wherever the overlay appears.

## Pull requests

Fork, branch, and open a pull request that says what you changed and how you checked it. Keep tag reviews and code changes in separate pull requests. If a change moves a published number, rerun the affected build step and say which figures changed.

## Licence

Code is MIT ([LICENSE](LICENSE)); data, tags, documentation and screenshots are CC BY 4.0 ([LICENSE-CC-BY.md](LICENSE-CC-BY.md)). By opening a pull request you agree that your contribution is licensed the same way.
