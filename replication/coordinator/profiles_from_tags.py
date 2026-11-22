#!/usr/bin/env python3
"""Effort profiles from one run's work-activity tags, computed the same way as the page (scripts/build_profiles.py).

    python3 -I replication/coordinator/profiles_from_tags.py ONET_DIR ANSWERS.jsonl [SOC ...]

For each task: weight = frequency term x importance x relevance (three models: ordinal, occurrence, flat), split
equally across the task's detailed work activities, each counted in the phase the run gave it. A task whose activities
the run did not tag is left out and reported as `untagged` (share of ordinal weight). Default occupations: the 13 in the
page's job-family chart, all of whose activities are in dwa-pilot.
"""
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

PHASES = ["understand", "plan", "produce", "check", "sustain", "coordinate"]
OCC_PER_YEAR = [1, 4, 24, 100, 250, 750, 2000]
FAMILY = ["15-1252.00", "15-1253.00", "15-1254.00", "15-1242.00", "15-1244.00", "15-1212.00", "15-1211.00",
          "15-2051.00", "15-2051.01", "13-1082.00", "29-1141.00", "13-2011.00", "47-2111.00"]


def tsv(d, name):
    return csv.DictReader(open(Path(d) / name, encoding="utf-8", errors="replace"), delimiter="\t")


def load_tasks(onet, socs):
    socs = set(socs)
    tasks = defaultdict(dict)
    for r in tsv(onet, "Task Ratings.txt"):
        if r["O*NET-SOC Code"] not in socs:
            continue
        t = tasks[r["O*NET-SOC Code"]].setdefault(r["Task ID"], {"ft": [0.0] * 7, "im": None, "rt": None, "dwas": []})
        v = float(r["Data Value"])
        if r["Scale ID"] == "FT":
            t["ft"][int(r["Category"]) - 1] = v
        elif r["Scale ID"] == "IM":
            t["im"] = v
        elif r["Scale ID"] == "RT":
            t["rt"] = v
    for r in tsv(onet, "Tasks to DWAs.txt"):
        t = tasks.get(r["O*NET-SOC Code"], {}).get(r["Task ID"])
        if t is not None:
            t["dwas"].append(r["DWA Element ID"])
    titles = {r["O*NET-SOC Code"]: r["Title"] for r in tsv(onet, "Occupation Data.txt")}
    return tasks, titles


def profiles(tasks, tags):
    """{soc: {"ordinal": {phase: share}, "occurrence": ..., "flat": ..., "untagged": share}}"""
    out = {}
    for soc, ts in tasks.items():
        prof = {m: Counter() for m in ("ordinal", "occurrence", "flat")}
        missing = total = 0.0
        for t in ts.values():
            if t["im"] is None or sum(t["ft"]) <= 0 or not t["dwas"]:
                continue
            p, tot = t["ft"], sum(t["ft"])
            rel = (t["rt"] if t["rt"] is not None else 100) / 100
            w = {"ordinal": sum((i + 1) * x for i, x in enumerate(p)) / tot * t["im"] * rel,
                 "occurrence": sum(OCC_PER_YEAR[i] * x for i, x in enumerate(p)) / tot * t["im"] * rel,
                 "flat": t["im"] * rel}
            total += w["ordinal"]
            split = Counter(tags[d] for d in t["dwas"] if d in tags)
            if len(split) == 0 or sum(split.values()) < len(t["dwas"]):
                missing += w["ordinal"]
                continue
            n = sum(split.values())
            for m in prof:
                for ph, c in split.items():
                    prof[m][ph] += w[m] * c / n
        out[soc] = {m: {ph: round(v[ph] / (sum(v.values()) or 1), 4) for ph in PHASES} for m, v in prof.items()}
        out[soc]["untagged"] = round(missing / total, 4) if total else 0
    return out


def main():
    onet, answers = sys.argv[1], sys.argv[2]
    socs = sys.argv[3:] or FAMILY
    tags = {}
    for line in open(answers, encoding="utf-8"):
        if line.strip():
            a = json.loads(line)
            tags[a["id"]] = a["answer"]
    tasks, titles = load_tasks(onet, socs)
    for soc, p in profiles(tasks, tags).items():
        row = "  ".join(f"{ph[:4]} {p['ordinal'][ph] * 100:4.0f}%" for ph in PHASES)
        print(f"{soc} {titles.get(soc, '')[:34]:34s} {row}  untagged {p['untagged'] * 100:.0f}%")


if __name__ == "__main__":
    main()
