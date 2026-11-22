# Replicating the judgments behind A New Shape for Work

**Summary.** This folder has everything an agent needs to make the paper's three judgment calls on its own: which phase each O*NET work activity belongs to, which occupation an unmatched job title belongs to, and which posting skill phrases point to a phase. Several models do the same pilot lists so they can be compared, and the rest is split into batches that agents can work through in parallel. Agents never see each other's answers or talk to each other. Pick the way in below that fits what your agent can do, follow [INSTRUCTIONS.md](INSTRUCTIONS.md), and hand in one folder per list. Never push your answers to this repository.

Why it matters: every phase tag in the repository is an unreviewed draft made by rules. Independent answers from several models show where the tags are solid (the models agree) and where a person needs to look (they don't), and how much the published effort profiles move with the tagger.

## Pick your way in

| Your agent can... | Way | What it does |
|---|---|---|
| run code and reach the internet | **A. Full replication** | Downloads O*NET 31.0, rebuilds the work-activity lists with `scripts/make_items.py` and checks they match, then tags. |
| run code, but not fetch anything | **B. Tagging only** | Tags the shared lists in `items/`. |
| only chat (no code, no fetching) | **C. Hand-out messages** | Gets the pilot lists as the messages in `handout/`, one at a time. |

All three give every model the same items, so the comparison is about the judgments alone.

## What's here

| Path | What it is |
|---|---|
| [INSTRUCTIONS.md](INSTRUCTIONS.md) | The task: independence rules, the three tasks, the lists, the instructions, the answer format, the checks, and what to hand in. |
| `prompts/assembled/` | The instructions for each task, exactly as every model gets them (`dwa.txt`, `titles.txt`, `phrases.txt`). |
| `prompts/` | The pieces they are built from: one template per task, the shared phase definitions (`phases.txt`) and the answer format. |
| `items/` | The lists to tag (one JSON object per line) and `occupations.tsv`, every O*NET-SOC code and title. |
| `handout/` | The pilot lists as complete chat messages (way C). |
| `scripts/` | Item builder, prompt renderer, Claude Code tagger, checker, hand-out writer, reply merger, manifest writer. Python 3 standard library only. |
| `run_batch.sh` | Tags one list end to end with Claude Code. |
| `coordinator/` | Comparison tools for after everyone has handed in. **Agents don't open this folder** (INSTRUCTIONS.md, section 1). |
| [DATA-NOTICES.md](DATA-NOTICES.md) | Where the items come from and their licences. |

## Way A: rebuild the work-activity lists

Download the O*NET 31.0 text database (CC BY 4.0, 13.2 MB, sha256 `6883548a…16b23a9`) from https://www.onetcenter.org/dl_files/database/db_31_0_text.zip, unzip it into a new empty folder, and rebuild:

```bash
python3 -I replication/scripts/make_items.py db_31_0_text my-items
for f in my-items/*; do cmp "$f" "replication/items/$(basename "$f")" && echo "same: $(basename "$f")"; done
```

The `dwa-*` lists and `occupations.tsv` should be byte-identical. If they aren't, say so in RUN.md and tag the shared lists. The `titles-*` and `phrases-*` lists come from the posting counts of the cluster run (`docs/GATHERING-DATA.md`) and can't be rebuilt without it; tag the shared ones. Then go on as for way B.

## Tagging (ways A and B)

**With any model:** render the exact messages, send each one in a fresh conversation, and save the answers:

```bash
python3 -I replication/scripts/render_prompts.py replication/items/dwa-pilot.jsonl prompts-dwa-pilot.jsonl
```

Each line holds `system`, `user` and the `ids` it covers. Put every answer from every reply into one `answers.jsonl` (one per line), then check:

```bash
python3 -I replication/scripts/check_answers.py replication/items/dwa-pilot.jsonl answers.jsonl report.json
```

A failed message gets one retry, sent with its list of errors (INSTRUCTIONS.md, section 6).

**With Claude Code:** `run_batch.sh` tags with headless `claude -p` on your own Claude plan, not an API key. Each call has no tools, no project files and no memory, and runs from an empty folder. It retries once on failed checks, then checks the whole list and writes the manifest:

```bash
replication/run_batch.sh replication/items/dwa-pilot.jsonl shape-dwa-pilot-claude-opus-5-5-20261122
```

`SHAPE_MODEL` and `SHAPE_EFFORT` pick the model and effort (default `claude-opus-5-5`, `high`), and `WORKERS` the parallel calls (default 2). An interrupted run picks up where it stopped.

## Way C: hand-out messages

Send `handout/dwa-pilot-1.md`, then `-2`, then `-3`; then the two `titles-pilot` messages; then the two `phrases-pilot` messages. Attach each file or paste it in, in a fresh chat each time. Save each reply as the message says (`reply-<list>-<n>.json`), then whoever has a computer merges and checks them:

```bash
python3 -I replication/scripts/merge_replies.py answers.jsonl reply-dwa-pilot-1.json reply-dwa-pilot-2.json reply-dwa-pilot-3.json
python3 -I replication/scripts/check_answers.py replication/items/dwa-pilot.jsonl answers.jsonl report.json
```

To rebuild the messages, run `python3 -I replication/scripts/make_handout.py replication/handout`.

## Working in parallel

Every list is independent: one agent, one list, one folder. A coordinator hands out lists (for example: every model gets the three pilots; eight agents take `dwa-batch-01` to `-08`), and nobody needs to know who else is working. Two agents given the same list by mistake produce two folders, and both count as runs.

## Hand in

Hand in one folder per list, `shape-<list>-<model>-<YYYYMMDD>`, laid out as INSTRUCTIONS.md section 7 describes. Copy it to `/projects/aiskunks/skills-lexicon-work/a-new-shape-for-work/replication-runs/` on the Explorer cluster if you have access, or send it to Bear. Don't push it here. Answers stay private until every model has handed in.

## Compare (coordinator, once everyone has handed in)

```bash
python3 -I replication/coordinator/export_baseline.py runs/          # the repository's rule-based draft, as one more run
python3 -I replication/coordinator/compare_runs.py comparison/ runs/shape-* --onet db_31_0_text
```

`comparison.md` gives, per list, each run's answers, pairwise agreement and Cohen's kappa, and Fleiss' kappa over all runs. For `dwa-pilot` it also recomputes the 13 job-family effort profiles under each run's tags, the same way the page does, and shows the spread between runs. `review-<list>.tsv` is the review queue: one row per item with the majority answer and every run's answer and reason, least agreement first.
