#!/usr/bin/env python3
"""Build the item lists in replication/items/ that agents tag.

    python3 -I replication/scripts/make_items.py ONET_DIR OUT_DIR [--counts BY_OCCUPATION.json.gz --title-map TITLE_MAP.tsv]

ONET_DIR  the O*NET 31.0 text database (db_31_0_text): needs Occupation Data, Content Model Reference,
          GWAs to IWAs, GWAs to IWAs to DWAs, Tasks to DWAs and Task Statements.
--counts and --title-map are the every-title cluster run's outputs (docs/GATHERING-DATA.md, steps 3-5). Without them
only the work-activity lists and occupations.tsv are built, which is all an agent needs to rebuild (way A).

Writes:
  occupations.tsv                       every O*NET-SOC code and title (the answer space for job titles)
  dwa-pilot.jsonl, dwa-batch-NN.jsonl   detailed work activities: the pilot is every DWA linked to a task of the
                                        13 job-family occupations on the page; the batches split the rest by id
  titles-pilot.jsonl, titles-batch-NN   the most common job titles the run could not assign, by posting count
  phrases-pilot.jsonl, phrases-batch-NN the most common posting skill phrases, by mentions
Every list is deterministic: the same inputs give byte-identical files.
"""
import argparse
import csv
import gzip
import json
from collections import Counter, defaultdict
from pathlib import Path

FAMILY = ["15-1252.00", "15-1253.00", "15-1254.00", "15-1242.00", "15-1244.00", "15-1212.00", "15-1211.00",
          "15-2051.00", "15-2051.01", "13-1082.00", "29-1141.00", "13-2011.00", "47-2111.00"]
DWA_BATCHES, TITLES_PILOT, TITLE_BATCH, PHRASES_PILOT, PHRASE_BATCH, PHRASES_MAX = 8, 100, 200, 300, 300, 1500


def tsv(d, name):
    return list(csv.DictReader(open(Path(d) / name, encoding="utf-8", errors="replace"), delimiter="\t"))


def write(out, name, rows):
    with open(out / name, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{name}: {len(rows)}")


def chunks(rows, size):
    return [rows[i:i + size] for i in range(0, len(rows), size)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("onet"); ap.add_argument("out")
    ap.add_argument("--counts"); ap.add_argument("--title-map")
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)

    occ = {r["O*NET-SOC Code"]: r["Title"] for r in tsv(a.onet, "Occupation Data.txt")}
    with open(out / "occupations.tsv", "w", encoding="utf-8") as f:
        f.write("soc\ttitle\n" + "".join(f"{s}\t{t}\n" for s, t in sorted(occ.items())))
    print(f"occupations.tsv: {len(occ)}")

    # detailed work activities, with their place in O*NET's hierarchy and up to three task statements that use them
    hier = {r["DWA Element ID"]: r for r in tsv(a.onet, "GWAs to IWAs to DWAs.txt")}
    iwa = {r["IWA Element ID"]: r["IWA Element Name"] for r in tsv(a.onet, "GWAs to IWAs.txt")}
    gwa = {r["Element ID"]: r["Element Name"] for r in tsv(a.onet, "Content Model Reference.txt")}
    text = {(r["O*NET-SOC Code"], r["Task ID"]): r["Task"] for r in tsv(a.onet, "Task Statements.txt")}
    uses = defaultdict(list)
    for r in tsv(a.onet, "Tasks to DWAs.txt"):
        uses[r["DWA Element ID"]].append((r["O*NET-SOC Code"], r["Task ID"]))
    items = []
    for d in sorted(hier):
        u = sorted(set(uses.get(d, [])), key=lambda k: (k[1], k[0]))
        picks, seen = [], set()
        for i in sorted({0, len(u) // 2, len(u) - 1} if u else set()) + list(range(len(u))):
            soc, tid = u[i]
            if soc not in seen and len(picks) < 3 and (soc, tid) in text:
                seen.add(soc)
                picks.append({"task": text[(soc, tid)], "occupation": occ.get(soc, soc)})
        h = hier[d]
        items.append({"id": d, "dwa": h["DWA Element Name"], "iwa": iwa[h["IWA Element ID"]], "gwa": gwa[h["GWA Element ID"]],
                      "n_tasks": len(u), "examples": picks})
    pilot_ids = {d for d, us in uses.items() for soc, _ in us if soc in FAMILY}
    pilot = [i for i in items if i["id"] in pilot_ids]
    rest = [i for i in items if i["id"] not in pilot_ids]
    write(out, "dwa-pilot.jsonl", pilot)
    size = -(-len(rest) // DWA_BATCHES)
    for n, c in enumerate(chunks(rest, size), 1):
        write(out, f"dwa-batch-{n:02d}.jsonl", c)

    if not (a.counts and a.title_map):
        return
    src = json.load(gzip.open(a.counts, "rt"))
    tmap = {r["title_norm"]: r for r in csv.DictReader(open(a.title_map, encoding="utf-8"), delimiter="\t")}
    titles = []
    for t in src["top_unresolved_titles"]:
        if t["status"] not in ("ambiguous", "none"):
            continue
        cands = (tmap.get(t["title_norm"], {}).get("candidates") or "").split()
        titles.append({"id": f"t{len(titles) + 1:03d}", "title": t["title_norm"], "postings": t["postings"],
                       "status": t["status"], "candidates": [{"soc": s, "title": occ.get(s, s)} for s in cands]})
    write(out, "titles-pilot.jsonl", titles[:TITLES_PILOT])
    for n, c in enumerate(chunks(titles[TITLES_PILOT:], TITLE_BATCH), 1):
        write(out, f"titles-batch-{n:02d}.jsonl", c)

    tot, where = Counter(), defaultdict(Counter)
    for soc, o in src["occupations"].items():
        for ph, c in o["phrases"].items():
            tot[ph] += c[0]
            where[ph][soc] += c[0]
    top = sorted(tot.items(), key=lambda kv: (-kv[1], kv[0]))[:PHRASES_MAX]
    phrases = [{"id": f"p{i:04d}", "phrase": ph, "mentions": n,
                "occupations": [occ.get(s, s) for s, _ in sorted(where[ph].items(), key=lambda kv: (-kv[1], kv[0]))[:3]]}
               for i, (ph, n) in enumerate(top, 1)]
    write(out, "phrases-pilot.jsonl", phrases[:PHRASES_PILOT])
    for n, c in enumerate(chunks(phrases[PHRASES_PILOT:], PHRASE_BATCH), 1):
        write(out, f"phrases-batch-{n:02d}.jsonl", c)


if __name__ == "__main__":
    main()
