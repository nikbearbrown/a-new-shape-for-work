#!/usr/bin/env python3
"""Render the exact messages for one item list, for any model.

    python3 -I replication/scripts/render_prompts.py ITEMS.jsonl PROMPTS.jsonl
    python3 -I replication/scripts/render_prompts.py --assembled      # rewrite prompts/assembled/*.txt

Each line of PROMPTS.jsonl is one message: {"list", "chunk", "ids", "system", "user"}. Send each in a fresh conversation
with `system` as the system prompt (or, if your model has none, as the start of the message) and `user` as the message.
Save the replies as described in INSTRUCTIONS.md, section 5.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # python3 -I leaves the script's folder off the path
from common import KIT, TASKS, list_of, load_jsonl, system_prompt, task_of, user_message


def main():
    if sys.argv[1:] == ["--assembled"]:
        out = KIT / "prompts/assembled"
        out.mkdir(exist_ok=True)
        for t in TASKS:
            (out / f"{t}.txt").write_text(system_prompt(t), encoding="utf-8")
            print(f"prompts/assembled/{t}.txt")
        return
    items_path, out_path = sys.argv[1:3]
    task = task_of(items_path)
    items, size = load_jsonl(items_path), TASKS[task][1]
    system = system_prompt(task)
    with open(out_path, "w", encoding="utf-8") as f:
        for n in range(0, len(items), size):
            c = items[n:n + size]
            f.write(json.dumps({"list": list_of(items_path), "chunk": n // size + 1, "ids": [i["id"] for i in c],
                                "system": system, "user": user_message(c)}, ensure_ascii=False) + "\n")
    print(f"{-(-len(items) // size)} messages for {len(items)} items -> {out_path}")


if __name__ == "__main__":
    main()
