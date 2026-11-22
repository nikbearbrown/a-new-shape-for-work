#!/usr/bin/env python3
"""Write the chat-only messages (way C) for the pilot lists.

    python3 -I replication/scripts/make_handout.py OUT_DIR [ITEMS.jsonl ...]   # default: the three pilot lists

Each message is complete on its own: the instructions, word for word, then a slice of the items.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # python3 -I leaves the script's folder off the path
from common import KIT, list_of, load_jsonl, system_prompt, task_of, user_message

PER_MESSAGE = {"dwa": 60, "titles": 50, "phrases": 150}


def main():
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    lists = sys.argv[2:] or [KIT / f"items/{t}-pilot.jsonl" for t in ("dwa", "titles", "phrases")]
    for path in lists:
        task, name = task_of(path), list_of(path)
        items, size = load_jsonl(path), PER_MESSAGE[task_of(path)]
        parts = [items[n:n + size] for n in range(0, len(items), size)]
        for k, part in enumerate(parts, 1):
            text = (f"# A New Shape for Work, independent replication: {name}, message {k} of {len(parts)}\n\n"
                    "Several models are doing this same task separately so their answers can be compared. Work only "
                    "from this message. Do not look for, ask for or use anyone else's answers, and do not ask another "
                    "AI to do any of it.\n\n## Instructions\n\n" + system_prompt(task) + "\n## Items\n\n"
                    + user_message(part) + "\n\n## What to send back\n\nThe JSON object described above, and nothing "
                    f"else. It is saved as `reply-{name}-{k}.json`.\n")
            (out / f"{name}-{k}.md").write_text(text, encoding="utf-8")
            print(f"{name}-{k}.md: {len(part)} items")


if __name__ == "__main__":
    main()
