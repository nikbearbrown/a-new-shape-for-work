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

**Claim.** A task with no exact text match in the Anthropic file contributes zero to the AI overlay ([`scripts/build_profiles.py` line 110](https://github.com/nikbearbrown/a-new-shape-for-work/blob/main/scripts/build_profiles.py#L110), `pen or 0`). The manuscript notes this ([line 66](https://github.com/nikbearbrown/a-new-shape-for-work/blob/main/paper/manuscript.md#L66)). Some of the 157 are reworded versions of tasks the Anthropic file does score, so a few occupations are understated.

**What the 157 are.** None involve encoding problems. Grouped by similarity to the closest Anthropic wording (`missing-ai-joins-review.csv`): about 23–33 differ by a letter or word (depending on the matching method), about 30 are reworded, and about 90 are new or unrelated. Of the near-identical group, only one has a nonzero score (Database Architects, 0.82), so the headline values do not move.

**Reworded examples that need a human decision.**

| Occupation | Current O*NET wording | Anthropic file wording | Score | My judgment |
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

Hydrologists' Produce AI share is 0.0 for the same reason ([`activity-profiles.csv` line 3946](https://github.com/nikbearbrown/a-new-shape-for-work/blob/main/research-data/activity-profiles.csv#L3946)).

**Proposed change.**

1. A reviewed crosswalk for the reworded group, with a reason for each match or non-match. No fuzzy matching at run time.
2. Report unmatched tasks as unavailable rather than zero, with each occupation's share of unavailable task weight, as Section 3.5 suggests.

## 4. Ad-side coverage across all occupations [section 5]

Across the 429 occupations with 50 or more retained ads, the median share of top skill mentions that are phase-diagnostic is 16.1% (min 2.2%, max 41.8%); 87 occupations are under 10%. The manuscript reports 18–42% for the eight featured occupations. Showing this coverage beside each posting profile would let readers see which profiles rest on thin evidence. This is a share of mentions, not a share of ads.

## Open questions for Nik

1. Can I get the per-occupation phrase counts from the cluster run (counts only) to measure the clearance fix?
2. For the reworded-task review, should the crosswalk live in `tags/` with `reviewed_by`, or stay in this folder until reviewed?

Journal options are covered in Mayank's venue recommendation (`notes/mayank-bhadrasen/`, on the `mayank/notes-folder` branch), so I have not repeated them here.
