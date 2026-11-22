#!/usr/bin/env python3
"""Turn the repository's own draft tags into hand-in folders, so they can be compared with the agents' runs.
Coordinator only: these are the answers agents must not see.

    python3 -I replication/coordinator/export_baseline.py OUT_DIR

The tags in tags/ were made on 2026-11-21 by rules (verb and object lists, a phrase rule list), before this kit
existed and not under its instructions. They are exported as the run "rules-draft-20261121" for every work-activity
and phrase list. There is no title baseline: the repository decided only six titles, none of them in these lists.
"""
import csv
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
from common import KIT, load_jsonl  # noqa: E402

REPO = KIT.parent
RUN = "rules-draft-20261121"


def main():
    out = Path(sys.argv[1])
    dwa = {r["dwa_id"]: r for r in csv.DictReader(open(REPO / "tags/dwa-phase-tags.tsv", encoding="utf-8"), delimiter="\t")}
    phr = {r["phrase"]: r for r in csv.DictReader(open(REPO / "tags/skill-phrase-phase-tags.tsv", encoding="utf-8"),
                                                 delimiter="\t")}
    for path in sorted((KIT / "items").glob("*.jsonl")):
        task = path.name.split("-")[0]
        if task == "titles":
            continue
        rows = []
        for it in load_jsonl(path):
            if task == "dwa":
                r = dwa[it["id"]]
                ans, why = r["phase"], f"{r['basis']}: {r.get('note') or ''}".strip(": ")
            else:
                r = phr.get(it["phrase"])
                ans, why = (r["phase"], r["basis"]) if r else ("neutral", "no rule fired")
            rows.append({"id": it["id"], "answer": ans, "alt": None, "confidence": None, "reason": why})
        d = out / f"shape-{path.stem}-{RUN}"
        d.mkdir(parents=True, exist_ok=True)
        with open(d / "answers.jsonl", "w", encoding="utf-8") as f:
            f.writelines(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
        print(d.name, len(rows))


if __name__ == "__main__":
    main()
