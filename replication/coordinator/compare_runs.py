#!/usr/bin/env python3
"""Compare hand-in folders once every agent has finished. Coordinator only: agents never run this.

    python3 -I replication/coordinator/compare_runs.py OUT_DIR RUN_DIR [RUN_DIR ...] [--onet ONET_DIR]

RUN_DIR is a hand-in folder named shape-<list>-<model>-<YYYYMMDD> holding answers.jsonl. Folders are grouped by list
(dwa-pilot, titles-batch-01, ...). For every list with two or more runs it writes, in OUT_DIR:

  comparison.md      per list: answers by run, pairwise agreement and Cohen's kappa, Fleiss' kappa over the items
                     every run answered, and (for dwa-pilot, given --onet) the job-family effort profiles under each
                     run's tags, with the spread between runs for each phase
  review-<list>.tsv  one row per item: the majority answer, how many runs gave it, and every run's answer and reason,
                     least agreement first. This is the queue for human review.
"""
import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "scripts"))
from common import KIT, PHASES, load_jsonl  # noqa: E402
from profiles_from_tags import FAMILY, load_tasks, profiles  # noqa: E402

NAME = re.compile(r"^shape-((?:dwa|titles|phrases)-(?:pilot|batch-\d\d))-(.+)$")
LABEL = {"dwa": "dwa", "titles": "title", "phrases": "phrase"}


def kappa_pair(a, b):
    n = len(a)
    if not n:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in ca) / (n * n)
    return None if pe == 1 else (po - pe) / (1 - pe)


def kappa_fleiss(rows):
    """rows: list of answer lists, one per item, every list the same length (the number of runs)."""
    if not rows or len(rows[0]) < 2:
        return None
    m, N = len(rows[0]), len(rows)
    cats = Counter(x for r in rows for x in r)
    P = [(sum(c * c for c in Counter(r).values()) - m) / (m * (m - 1)) for r in rows]
    pbar = sum(P) / N
    pe = sum((c / (N * m)) ** 2 for c in cats.values())
    return None if pe == 1 else (pbar - pe) / (1 - pe)


def fmt(x):
    return "n/a" if x is None else f"{x:.2f}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("runs", nargs="+"); ap.add_argument("--onet")
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    groups = defaultdict(dict)
    for r in a.runs:
        r = Path(r)
        m = NAME.match(r.name)
        if not m or not (r / "answers.jsonl").exists():
            print(f"skipped {r}: not shape-<list>-<model>-<date> with answers.jsonl")
            continue
        groups[m.group(1)][m.group(2)] = {x["id"]: x for x in load_jsonl(r / "answers.jsonl")}
    md = ["# Replication comparison", ""]
    for lst, runs in sorted(groups.items()):
        if len(runs) < 2:
            md += [f"## {lst}", "", f"Only one run ({', '.join(runs)}); nothing to compare.", ""]
            continue
        items = {i["id"]: i for i in load_jsonl(KIT / f"items/{lst}.jsonl")}
        names = sorted(runs)
        common = [i for i in items if all(i in runs[n] for n in names)]
        md += [f"## {lst}", "", f"{len(items)} items; {len(common)} answered by all {len(names)} runs.", "",
               "| run | answered | " + " | ".join(["answers by value"]) + " |", "|---|---|---|"]
        for n in names:
            c = Counter(x["answer"] for x in runs[n].values())
            md.append(f"| {n} | {len(runs[n])} | " + ", ".join(f"{k} {v}" for k, v in c.most_common(8)) + " |")
        md += ["", "| pair | agreement | Cohen's kappa |", "|---|---|---|"]
        for x, y in combinations(names, 2):
            ax = [runs[x][i]["answer"] for i in common]
            ay = [runs[y][i]["answer"] for i in common]
            agree = sum(p == q for p, q in zip(ax, ay)) / len(common) if common else 0
            md.append(f"| {x} vs {y} | {agree:.0%} | {fmt(kappa_pair(ax, ay))} |")
        fk = kappa_fleiss([[runs[n][i]["answer"] for n in names] for i in common])
        unanimous = sum(len({runs[n][i]["answer"] for n in names}) == 1 for i in common)
        md += ["", f"Fleiss' kappa over all runs: {fmt(fk)}. Unanimous on {unanimous} of {len(common)} items.", ""]

        # review queue: least agreement first, then the heaviest items
        task = lst.split("-")[0]
        weight = {"dwa": "n_tasks", "titles": "postings", "phrases": "mentions"}[task]
        text = {"dwa": "dwa", "titles": "title", "phrases": "phrase"}[task]
        rows = []
        for i, it in items.items():
            got = [runs[n][i]["answer"] for n in names if i in runs[n]]
            if not got:
                continue
            top, k = Counter(got).most_common(1)[0]
            rows.append([i, it[text], it.get(weight, ""), top, f"{k}/{len(got)}"]
                        + [f"{runs[n][i]['answer']} ({runs[n][i].get('confidence')}): {runs[n][i].get('reason', '')}"
                           if i in runs[n] else "" for n in names])
        rows.sort(key=lambda r: (int(r[4].split("/")[0]) / int(r[4].split("/")[1]), -(r[2] or 0)))
        with open(out / f"review-{lst}.tsv", "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f, delimiter="\t")
            w.writerow(["id", LABEL[task], weight, "majority", "runs_agreeing"] + names)
            w.writerows(rows)
        md += [f"Review queue: `review-{lst}.tsv` ({sum(1 for r in rows if r[4].split('/')[0] != r[4].split('/')[1])} "
               "items without full agreement).", ""]

        if lst == "dwa-pilot" and a.onet:
            tasks, titles = load_tasks(a.onet, FAMILY)
            prof = {n: profiles(tasks, {i: x["answer"] for i, x in runs[n].items()}) for n in names}
            md += ["Effort profiles (ordinal model) for the job-family occupations under each run's tags. "
                   "Each cell lists the runs in the order " + ", ".join(names) + "; spread is the largest minus the "
                   "smallest, in percentage points.", "",
                   "| occupation | " + " | ".join(PHASES) + " | largest spread |", "|---|" + "---|" * (len(PHASES) + 1)]
            for soc in FAMILY:
                cells, spreads = [], []
                for ph in PHASES:
                    vals = [prof[n][soc]["ordinal"][ph] * 100 for n in names]
                    spreads.append((max(vals) - min(vals), ph))
                    cells.append(" / ".join(f"{v:.0f}" for v in vals))
                s, ph = max(spreads)
                md.append(f"| {titles.get(soc, soc)} | " + " | ".join(cells) + f" | {s:.0f} pts ({ph}) |")
            md.append("")
    (out / "comparison.md").write_text("\n".join(md), encoding="utf-8")
    print(f"wrote {out / 'comparison.md'} and {len([g for g in groups.values() if len(g) > 1])} review files")


if __name__ == "__main__":
    main()
