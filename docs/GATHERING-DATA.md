# Gathering the data for every job title

This is the procedure for running the Job Shape analysis on every job title, not just the eight in the prototype. It is written for a person or an agent with this repository on a Mac and an account on Northeastern's Explorer cluster (`ssh explorer`, `/projects/aiskunks`), where the posting archives live. Steps 1–3 and 7 need no cluster access.

## What "every job title" means here

The Skills Lexicon does not yet hold a list of job titles. It holds skills, tools, knowledge areas and credentials, and O*NET's skill, knowledge and ability ratings for 894 occupations. Its job-title-to-occupation pilot (`docs/handoff/prompts/06-job-title-pilot.md` in the lexicon) has not been run. So this procedure uses **O*NET's own title tables** as the title list: 1,016 occupation titles, 54,269 alternate titles and 8,189 titles reported by workers, which normalise to 47,839 distinct titles once singular forms of the plural occupation names are added. When the lexicon gains its own title list, add those titles to `scripts/make_title_map.py` and rerun from step 3.

The three layers cover titles differently:

| Layer | Source | Coverage | Needs per-title work? |
|---|---|---|---|
| Activity (effort estimate) | O*NET 31.0 task ratings | all 911 rated occupations | no |
| AI overlay | Anthropic Economic Index task coverage | 18,680 of 18,838 O*NET tasks | no |
| Emphasis (what postings ask for) | job postings on the cluster | only titles that map to an occupation | **yes: the title map** |

So for the first two layers, "every job title" means every O*NET occupation, and the work is already done once steps 1–2 run. The posting layer is where titles matter, and most of this document is about it.

## Rules

- Download nothing without the project owner's OK. Steps 1 and 6 list every download with its size.
- Heavy reading runs as Slurm jobs, never on the login node. Python on Explorer: `module load python/3.13.5`.
- Use only posting datasets on the allow-list (`kaggle-allowlist.tsv` in the lexicon's `replication/` folder: CC0, CC BY, ODC-By, MIT, Apache 2.0). The prototype uses one of them for every title (asaniczka LinkedIn 2024, ODC-By) and one more for the dated data-analyst series.
- No description text and no per-posting rows leave the cluster in the every-title run. Only counts come back.
- Every judgment (a phase tag, a title decision) goes in `tags/` with a reason and `status: draft` until a named person reviews it.

## Step 1. Fetch the public inputs (Mac)

```bash
bash scripts/fetch_sources.sh
```

- O*NET 31.0 text database (CC BY 4.0), 13.2 MB zip. On the cluster it is already at `/projects/aiskunks/onet/31.0/db_31_0_text`; the script copies 13 files from there when `ssh explorer` works.
- Anthropic Economic Index `labor_market_impacts/task_penetration.csv`, 1.9 MB, pinned to dataset commit `4e5f69f`. One row per O*NET task statement: `task, penetration` (0 for 16,644 tasks; above 0 for 1,354).

Check the printed sha256 values against the ones in the script.

## Step 2. Build the occupation layers (Mac, a minute)

```bash
python3 -I scripts/phase_tags.py      # tags/iwa-phase-tags.tsv  (332 intermediate work activities)
python3 -I scripts/dwa_tags.py        # tags/dwa-phase-tags.tsv  (2,087 detailed work activities)
python3 -I scripts/build_profiles.py  # data/onet-profiles.json  (911 occupations: effort profiles + AI coverage)
```

The two tag files are the judgments. Edit them, not the scripts' output: `dwa_tags.py` has a `MANUAL` table for one-off DWA decisions, and `phase_tags.py` has the GWA defaults and IWA overrides, each with a reason.

## Step 3. Build the title map (Mac)

```bash
git clone https://github.com/nikbearbrown/skills-lexicon ../skills-lexicon
python3 -I scripts/export_lexicon_forms.py ../skills-lexicon       # data/lexicon-forms.json (skill classes)
python3 -I scripts/make_title_map.py                                 # data/title-map.tsv
```

`make_title_map.py` normalises every O*NET title with `cluster/title_norm.py` (the same function the cluster uses on posting titles: lower case, drop brackets, cut at " - ", drop work-mode and level words) and records, for each normalised title:

| status | meaning |
|---|---|
| `unique` | one occupation |
| `rolled-up` | a base occupation and its own sub-occupations (29-1141.00 and 29-1141.03): counted for the base |
| `decided` | a hand decision in `tags/title-decisions.tsv` |
| `ambiguous` | several unrelated occupations: postings are counted but not assigned |

`make_title_map.py` also adds the singular of each occupation name ("Data Scientists" → "data scientist") where no other O*NET title claims it, because O*NET names occupations in the plural and postings use the singular. A decision with occupation `-` marks a title as `excluded`: posting usage doesn't match any occupation O*NET lists it under ("account executive" is listed only under advertising managers but is mostly a sales title).

On O*NET 31.0: 40,924 unique, 135 rolled up, 5 decided, 1 excluded, 6,774 ambiguous. Ambiguous titles include some of the most common in postings ("data analyst" lists 8 occupations, "customer service representative" 2, "store manager" several).

## Step 4. Run the posting extraction for every title (cluster)

Copy the scripts and the map, then submit:

```bash
W=/projects/aiskunks/skills-lexicon-work/a-new-shape-for-work
scp cluster/postings.py cluster/postings_by_occupation.py cluster/title_norm.py cluster/by-occupation.sbatch \
    data/title-map.tsv explorer:$W/
ssh explorer "cd $W && sbatch by-occupation.sbatch"
```

The job (1 CPU, 32 GB, about 20 minutes) reads the LinkedIn archive in place (`/projects/aiskunks/kaggle/jobs/kaggle-data/asaniczka/1-3m-linkedin-jobs-and-skills-2024/v2/dataset.zip`, 2.0 GB, three CSVs) and, for each US posting:

1. normalises the title and looks it up: exact first, then the longest leading or trailing run of 2+ words that resolves ("registered nurse icu" → "registered nurse"; "backend software engineer" → "software engineer");
2. drops repeats of the same company, title and location, then repeats of the same summary text within an occupation (agency reposts);
3. reads the level from the title (entry, mid, senior, lead, or none), the model-extracted skill list, the first stated "N years … experience", and six draft phase cue flags from the summary.

On the 2026-11-21 run (Slurm job 12056013) the title lookup gave, for 1,149,342 US postings: 206,923 exact unique, 47,653 rolled up, 17,191 decided, 47,552 by leading words, 86,853 by trailing words (35% assigned in all), 216,975 ambiguous (19%), 4,863 excluded and 521,332 with no match (45%). After the two dedup steps, 277,976 postings remain across 915 occupations; 429 occupations have 50 or more. The leading- and trailing-word matches are the least certain: sample them before relying on an occupation.

It writes `$W/out-by-occupation/by-occupation.json.gz`: per occupation, counts by level, the top 400 skill phrases with counts by level, experience histograms, cue counts and dates, plus the 500 most common titles it could not assign. A smoke test: `sbatch by-occupation.sbatch --limit 50000` (the postings pass stops early; the skills and summary passes still stream their whole files).

## Step 5. Bring back the counts and build the posting layer (Mac)

```bash
scp explorer:$W/out-by-occupation/by-occupation.json.gz data/postings/
python3 -I scripts/build_postings_by_occupation.py   # data/postings-by-occupation.json
```

Shares are taken over the phrases the cluster kept (each occupation's 400 most common, about half of all mentions), since only those are tagged. This applies the draft phrase-to-phase rules (`scripts/build_postings.py`, `PHRASE_RULES`) and the lexicon classes to each occupation with 50 or more postings: posting emphasis profile, seniority ladder, requirement stack, experience by level. It prints how many US postings were assigned.

## Step 6. Optional: the dated series (cluster)

The LinkedIn set is one snapshot (January 2024). The only dated set used so far is data-analyst postings from Google Jobs, Nov 2022 to Apr 2025 (`lukebarousse/data-analyst-job-postings-google-search` v744, Apache 2.0, 87 MB zip, on the cluster). `cluster/gsearch.sbatch` runs it. For other titles over time, look for allow-listed sets with a date column in the lexicon's job-fields survey (`/projects/aiskunks/skills-lexicon-work/job-fields-survey-20261106/full/summary.json`) and add a reader to `cluster/postings.py` on the same pattern.

## Step 7. Review, then publish

1. **Unassigned titles.** Read `top_unresolved_titles` in `data/postings-by-occupation.json`. On the 2026-11-21 run the largest were "manager" (9,611, ambiguous), "travel allied health professional" (9,151, no match), "assistant manager" (8,384), "sales associate-ft" (7,305: the normaliser does not yet strip "-ft" and "-pt"), "store manager", "shift manager" and "physician". For each high-volume ambiguous title, add a row to `tags/title-decisions.tsv` (title, occupation, reason, `draft`), then rerun steps 3–5.
2. **Phase tags.** Sample `tags/dwa-phase-tags.tsv` rows for the occupations you will publish (the page's task strip shows which DWAs set each task's phase) and record a reviewer in `reviewed_by`.
3. **Phrase tags.** `tags/skill-phrase-phase-tags.tsv` lists every phrase that counted as phase-diagnostic. Check the high-count ones; boilerplate ("401(k) plan") must stay neutral.
4. **Rebuild the page:** `python3 -I scripts/build_page_data.py`, then open `page/` through a static server.

## Known limits of this procedure

- Exact title matching leaves many postings unassigned or ambiguous. That is deliberate: it shows the gap instead of hiding it in a model's guesses. A model-assisted title step should be measured against hand-labelled samples first, as the lexicon's pilot plan says.
- The LinkedIn skill lists were extracted by the dataset author's own model, so they are not employer text, and required and preferred are not separated.
- One snapshot cannot show change over time. Charts 2, 4 and 6 exist for data analysts only.
- AI coverage is observed Claude use from August and November 2025, not capability, and not job loss.
