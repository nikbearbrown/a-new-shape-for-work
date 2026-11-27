# Findings

Checked against `main` on 2026-11-22 (manuscript draft v0.2) and re-run against `main` at commit 40eae5e on 2026-11-26; the referenced files had not changed. Line links point to `main`; if a file has changed since, a line may have moved. Every number here is printed by `verify_findings.py` (section numbers in brackets).

## 1. The deposit reproduces [sections 1–2]

- All six files in `research-data/SHA256SUMS` match.
- Re-running `research-data/export-profiles.py` and `paper/figures/build-ai-overlay.py` in a scratch copy gives byte-identical `activity-profiles.csv`, `posting-emphasis.csv` and `ai-overlay-developers.svg`.
- The headline values in the manuscript table reproduce (e.g. software developers, Coordinate: 36.10% activity vs 8.02% posting emphasis).

Scope: this shows the published tables match the dashboard data. It does not test the cluster steps that produced the posting counts.

## 2. "Security clearance" is tagged Sustain [section 7]

**Claim.** The Sustain keyword rule matches `security` anywhere in a phrase ([`scripts/build_postings.py` line 33](https://github.com/nikbearbrown/a-new-shape-for-work/blob/main/scripts/build_postings.py#L33)), so a clearance requirement is counted as Sustain work. Credentials are meant to be neutral ([`docs/METHOD.md` line 52](https://github.com/nikbearbrown/a-new-shape-for-work/blob/main/docs/METHOD.md#L52)).

**Evidence.**

- 182 of the 186 tagged phrases containing "clearance" are Sustain, e.g. `security clearance` ([`tags/skill-phrase-phase-tags.tsv` line 39007](https://github.com/nikbearbrown/a-new-shape-for-work/blob/main/tags/skill-phrase-phase-tags.tsv#L39007)).
- `secret clearance` and `ts/sci clearance` are absent from the tag file, so they are neutral. Same requirement, different wording, different phase.
- The rules are first-match-wins, and `background check` and `drug test` are already in the neutral rule ([lines 22–26](https://github.com/nikbearbrown/a-new-shape-for-work/blob/main/scripts/build_postings.py#L22-L26)).

**Where it shows.** From `page/data/by-occupation.json` (Chart 5, "Not in the lexicon yet"):

| Occupation | Phrase | Share of ads | Phase given | Occupation's Sustain share |
| --- | --- | --- | --- | --- |
| Interpreters and Translators (27-3091.00) | security clearance | 17.2% | Sustain | 18.4% |
| Control and Valve Installers and Repairers, Except Mechanical Door (49-9012.00) | faa security clearance | 9.7% | Sustain | 31.4% |
| Penetration Testers (15-1299.04) | ts/sci clearance | 8.7% | neutral | 39.8% |
| Career/Technical Education Teachers, Postsecondary (25-1194.00) | secret clearance | 8.1% | neutral | 14.0% |

For Interpreters and Translators, my estimate from the rounded dashboard shares is that this one phrase accounts for nearly all of the 18.4% Sustain share (about 31 of roughly 31 Sustain mentions). For Control and Valve Installers it is about 14 of roughly 111. This is an estimate: the dashboard stores shares, not the per-occupation phrase counts.

**Proposed change.** Add `clearance` to the neutral rule so it matches before Sustain, re-run the affected occupations, and report original vs revised shares and coverage.

**Needed.** The per-occupation phrase counts from the cluster run (`data/postings/by-occupation.json.gz`, counts only) to measure the effect exactly.

## 3. Reworded tasks among the 157 missing AI joins [section 6]

**Claim.** A task with no exact text match in the Anthropic file contributes zero to the AI overlay ([`scripts/build_profiles.py` line 110](https://github.com/nikbearbrown/a-new-shape-for-work/blob/main/scripts/build_profiles.py#L110), `pen or 0`). The manuscript notes this ([line 66](https://github.com/nikbearbrown/a-new-shape-for-work/blob/main/paper/manuscript.md#L66)). Some of the 157 look like reworded versions of tasks the Anthropic file does score. If they are the same tasks, a few occupations are understated.

**What the 157 are.** None involve encoding problems. Grouped by similarity to the closest Anthropic wording (`missing-ai-joins-review.csv`): about 23–33 differ by a letter or word (depending on the matching method), about 30 are reworded, and about 90 are new or unrelated. Of the near-identical group, only one has a nonzero score (Database Architects, 0.82), so the headline values do not move.

**Reworded examples that need a human decision.** The judgments below are my proposals, not confirmed matches.

| Occupation | Current O*NET wording | Anthropic file wording | Score | My proposed judgment (not confirmed) |
| --- | --- | --- | --- | --- |
| Paralegals and Legal Assistants (23-2011.00) | Prepare, edit, or review legal documents, including legislation, briefs, pleadings… | Prepare legal documents, including briefs, pleadings… ([line 12565](https://github.com/nikbearbrown/a-new-shape-for-work/blob/main/research-data/sources/anthropic-task-penetration.csv#L12565)) | 0.7341 | Same core task, broadened. Likely a match |
| Hydrologists (19-2043.00) | Prepare reports or presentations describing research results… | Prepare written and oral reports describing research results… ([line 12846](https://github.com/nikbearbrown/a-new-shape-for-work/blob/main/research-data/sources/anthropic-task-penetration.csv#L12846)) | 0.943 | Same task. Likely a match |
| Epidemiologists (19-1041.00) | Write articles for publication in professional journals. | Review manuscripts for publication in professional journals. ([line 15065](https://github.com/nikbearbrown/a-new-shape-for-work/blob/main/research-data/sources/anthropic-task-penetration.csv#L15065)) | 0.7239 | Different task (writing vs reviewing). Not a match |

Older O*NET releases used the shorter paralegal wording (e.g. a 2012 archived My Next Move profile); the current O*NET page uses the longer one. I have not confirmed which release changed it.

**Effect for paralegals.** Recomputing from `page/data/onet.json` (reproduces the published values to within rounding):

| Paralegals, ordinal model | Published | If the reworded task used 0.7341 |
| --- | --- | --- |
| Produce AI-weighted share | 0.0% | 12% |
| Total AI index | 11% | 24% |

Hydrologists' Produce AI share is also 0.0, and the unmatched reports task is one reason ([`activity-profiles.csv` line 3946](https://github.com/nikbearbrown/a-new-shape-for-work/blob/main/research-data/activity-profiles.csv#L3946)).

**How the proposed matches could be confirmed.**

1. **O*NET Task IDs.** O*NET gives every task statement a Task ID. If the old wording (in the Anthropic file) and the new wording (in O*NET 31.0) carry the same Task ID across releases, O*NET itself treats them as one task that was reworded. I have not yet checked whether O*NET keeps the ID when it rewords a task, or which release the Anthropic file used.
2. **A second, independent reviewer**, as the manuscript proposes for phase tags, with disagreements adjudicated.
3. **A stated rule for each pair:** match only when the action, the object and the purpose are the same. A different action (writing vs reviewing) is a different task, however similar the wording.

**Proposed change.**

1. A reviewed crosswalk for the reworded group, with the evidence and reason for each match or non-match. No fuzzy matching at run time.
2. Report unmatched tasks as unavailable rather than zero, with each occupation's share of unavailable task weight, as Section 3.5 suggests.

## 4. Ad-side coverage across all occupations [section 5]

Across the 429 occupations with 50 or more retained ads, the median share of top skill mentions that are phase-diagnostic is 16.1% (min 2.2%, max 41.8%); 87 occupations are under 10%. The manuscript reports 18–42% for the eight featured occupations. Showing this coverage beside each posting profile would let readers see which profiles rest on thin evidence. This is a share of mentions, not a share of ads.

## 5. Dashboard summary wording on posting coverage

**Claim.** The executive summary says the posting layer "covers every occupation O*NET names a title for" ([`page/index.html` line 122](https://github.com/nikbearbrown/a-new-shape-for-work/blob/main/page/index.html#L122)). The same sentence goes on to give the 35% assignment rate, so it is not wrong, but the opening reads as full coverage.

**Evidence.** The page's own "Title ambiguity" note says title matching assigned 35% of US postings, 19% had ambiguous titles and 45% matched nothing ([line 260](https://github.com/nikbearbrown/a-new-shape-for-work/blob/main/page/index.html#L260)). The README gives the coverage that results: 915 codes received postings, 429 met the 50-ad cutoff, and 409 of the 911 rated occupations can be shown side by side ([README line 40](https://github.com/nikbearbrown/a-new-shape-for-work/blob/main/README.md#L40)).

**Proposed change.** Lead with the coverage readers will see, for example: "Title matching assigned 35% of 1.15 million US LinkedIn postings to an occupation, enough for posting charts for 429 occupations (409 of the 911 that O*NET rates)." Wording only; no numbers change.

## Open questions for Nik

1. Can I get the per-occupation phrase counts from the cluster run (counts only) to measure the clearance fix?
2. For the reworded-task review, should the crosswalk live in `tags/` with `reviewed_by`, or stay in this folder until reviewed?
3. Would you like a second reviewer for the proposed matches, and is the O*NET Task ID check the evidence you would accept?

My venue recommendation is in its own issue: [#5 Venue recommendation: Work, Employment and Society](https://github.com/nikbearbrown/a-new-shape-for-work/issues/5). Mayank's recommendation (Big Data & Society) is in `notes/mayank-bhadrasen/` on the `mayank/notes-folder` branch.
