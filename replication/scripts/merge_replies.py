#!/usr/bin/env python3
"""Turn saved chat replies (way C) into one answers file.

    python3 -I replication/scripts/merge_replies.py ANSWERS.jsonl reply-dwa-pilot-1.json reply-dwa-pilot-2.json ...

Each reply is the JSON object a message asked for ({"answers": [...]}); code fences around it are ignored.
"""
import json
import re
import sys


def main():
    out, n = sys.argv[1], 0
    with open(out, "w", encoding="utf-8") as f:
        for path in sys.argv[2:]:
            text = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", open(path, encoding="utf-8").read())
            for a in json.loads(text)["answers"]:
                f.write(json.dumps({**a, "_meta": {"reply": path}}, ensure_ascii=False) + "\n")
                n += 1
    print(f"{n} answers -> {out}")


if __name__ == "__main__":
    main()
