# A New Shape for Work: tag the work on your own

**What this is.** You are one of several language models making the same judgments for *A New Shape for Work* **independently**, so the answers can be compared afterwards. [README.md](README.md) says which way in fits what you can do; this page is the task itself. You get a list of items, tag each one under the instructions below, check your answers, and hand in one folder.

**First written 2026-11-22.** Claude (Opus 5.5, effort high) tagged the three pilot lists first, under these same instructions. Its answers stay private until every model has handed in.

## 1. Independence rules (read first)

- **Work alone.** Do not read, search for, or ask for any other model's answers, including Claude's. Do not ask another AI to do any part of this for you, and do not contact the other agents doing it.
- **Read only this folder** (`replication/`) and the public sources it names (the O*NET database, for way A). The rest of the repository holds a rule-based draft of the same judgments: `tags/`, `data/`, `page/`, `docs/`, `scripts/`, `cluster/` and the top-level README. **Don't open them**, and don't open `replication/coordinator/`, which turns that draft into answers.
- If you come across a folder or file from another run (any `shape-*` folder that isn't yours, any `answers*.jsonl` or `reply-*.json` you didn't write), **don't open it.**
- Don't edit the repository, don't push to GitHub (not even your hand-in), and don't publish anything.

## 2. The analysis and the three tasks

The paper estimates where each job's work sits across six phases (understand, plan, produce, check, sustain, coordinate), from O*NET's task ratings, and sets that beside what job postings ask for. Three judgments decide the results, and each is one task here:

| Task | Item | Your answer | What it decides |
|---|---|---|---|
| `dwa` | an O*NET detailed work activity, with where O*NET files it and up to three task statements that use it | one of the six phases | how every occupation's estimated effort divides across the phases |
| `titles` | a job title from US LinkedIn postings (January 2024) that couldn't be matched to one occupation | an O*NET-SOC occupation code, or `-` for none | which occupation those postings count for |
| `phrases` | a skill phrase from those postings' skill lists | one of the six phases, or `neutral` | which phrases count when postings are summarised by phase |

Every answer also gives a second choice (`alt`, or null), a confidence (high, medium or low) and a one-sentence reason.

## 3. The lists

Each task is split into a **pilot** list, which every model does so the models can be compared, and **batches**, which cover everything else and can be shared out across agents.

| List | Items | What's in it |
|---|---|---|
| `dwa-pilot` | 175 | every activity used by a task of the 13 job-family occupations on the page (software developers, QA analysts, web developers, database administrators, network administrators, information security analysts, computer systems analysts, data scientists, business intelligence analysts, project management specialists, registered nurses, accountants, electricians) |
| `dwa-batch-01` to `dwa-batch-08` | 239 each | the other 1,912 activities, in O*NET id order |
| `titles-pilot` | 100 | the 100 most common unmatched titles (210,345 postings) |
| `titles-batch-01`, `titles-batch-02` | 200, 199 | the next 399 (111,542 postings) |
| `phrases-pilot` | 300 | the 300 most mentioned skill phrases (about half of all mentions) |
| `phrases-batch-01` to `phrases-batch-04` | 300 each | the next 1,200 |

**Do the list or lists you were given.** If you were given none, do the three pilot lists. Each list is one hand-in folder (section 7), so agents working in parallel never touch the same files.

The items are in `items/<list>.jsonl`, one JSON object per line. The occupation list for the `titles` task (every O*NET-SOC code and title) is `items/occupations.tsv`; it is also written into the titles instructions.

## 4. The instructions (use them exactly)

The instructions for each task are in `prompts/assembled/<task>.txt`: `dwa.txt`, `titles.txt` and `phrases.txt`. Use the text word for word as your instructions (as the system prompt, if your model has one). It is built from the pieces in `prompts/` (`system-<task>.txt` with `phases.txt` and `answer-format.txt` filled in), and `scripts/render_prompts.py --assembled` rebuilds it.

Send the items in messages of 30 (`dwa`), 25 (`titles`) or 50 (`phrases`), in file order, each in a **fresh conversation** with no memory of the others. The message text is fixed:

```text
Here are N items. Each line is one item, as JSON.

<the items, one JSON object per line>

Return the JSON object described in your instructions, with one answer for each of the N items.
```

`scripts/render_prompts.py` writes every message for a list. Chat-only agents get bigger slices in fewer messages (README, way C); that is the one allowed difference.

## 5. What an answer looks like

Each reply is one JSON object, `{"answers": [...]}`, with one entry per item:

```json
{"id": "4.A.1.a.1.b.7", "answer": "understand", "alt": null, "confidence": "high", "reason": "One sentence."}
```

Save all of a list's answers in `answers.jsonl`, one entry per line. You may add a `_meta` object to each line (model, attempts, anything else useful); everything else stays as above.

## 6. Check every answer

`python3 -I replication/scripts/check_answers.py items/<list>.jsonl answers.jsonl report.json` runs these checks:

- every item has exactly one answer, under its own id, and there are no answers for ids that weren't sent;
- `answer` is allowed for the task: a phase (`dwa`); a phase or `neutral` (`phrases`); a code from the occupation list or `-` (`titles`);
- `alt` is null or allowed for the task (a phase for `dwa` and `phrases`), and differs from `answer`;
- `confidence` is high, medium or low, and `reason` is not empty.

A message whose answers fail gets **one** retry, sent with its list of errors. If it still fails, keep what passed, leave the rest out, and record the errors. More retries mostly teach a model to satisfy the checker rather than the task.

## 7. What to hand in

One folder per list, named `shape-<list>-<your model name>-<the date you started, YYYYMMDD>`, for example `shape-dwa-pilot-gpt-5-codex-20261122`, holding:

- `answers.jsonl`: section 5.
- `report.json`: the checker's output, section 6.
- `manifest.json`, if you used the scripts (`run_batch.sh` writes it; otherwise `scripts/write_manifest.py`).
- `RUN.md`:
  - the model and version, and any reasoning or effort setting;
  - the date and time you started and finished;
  - which way in you used (README) and how you sent the messages;
  - anything you could not do, or did differently from this page, with the reason.

When it is done and you have Explorer access, copy the folder to `/projects/aiskunks/skills-lexicon-work/a-new-shape-for-work/replication-runs/` (for example: `tar czf - <folder> | ssh explorer 'cd /projects/aiskunks/skills-lexicon-work/a-new-shape-for-work/replication-runs && tar xzf -'`), then tell Bear it is there. Without Explorer access, send the folder to Bear. **Explorer rules:** nothing heavy runs on the login node, ask Bear before any Slurm job (none is needed for this), and never delete anything on the cluster. Don't open the other folders in `replication-runs/`, and don't push your folder to this repository.

## 8. What happens next

Once every model has handed in, the coordinator runs `coordinator/compare_runs.py`. It measures agreement between models (pairwise and overall), shows how much the job-family effort profiles move when a different model does the tagging, and writes a review queue for each list with the items the models disagree on first. People review that queue; reviewed answers then replace the draft tags in `tags/`.
