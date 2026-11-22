#!/usr/bin/env python3
"""Check one list's answers and summarise them.

    python3 -I replication/scripts/check_answers.py ITEMS.jsonl ANSWERS.jsonl REPORT.json

Checks every rule in INSTRUCTIONS.md, section 6: one answer per item, allowed values only, a reason for each.
Prints pass or fail and writes REPORT.json (counts by answer and by confidence, and every error). Exit code 1 on fail.
"""
import json
import sys
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(__file__).resolve().parent))  # python3 -I leaves the script's folder off the path
from common import check, list_of, load_jsonl, task_of


def main():
    items_path, answers_path, report_path = sys.argv[1:4]
    task = task_of(items_path)
    items, answers = load_jsonl(items_path), load_jsonl(answers_path)
    errs = check(task, items, answers)
    report = {"list": list_of(items_path), "task": task, "items": len(items), "answers": len(answers),
              "status": "fail" if errs else "pass", "errors": errs,
              "by_answer": dict(Counter(a.get("answer") for a in answers).most_common()),
              "by_confidence": dict(Counter(a.get("confidence") for a in answers).most_common()),
              "with_alt": sum(1 for a in answers if a.get("alt"))}
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=1, ensure_ascii=False)
    print(f"{report['list']}: {report['status']} ({len(answers)} answers for {len(items)} items, {len(errs)} errors)")
    for e in errs[:20]:
        print("  " + e)
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
