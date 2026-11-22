#!/usr/bin/env python3
"""Tag one item list with headless Claude Code (`claude -p`) on the plan this machine is signed in to. No API key.

    python3 -I replication/scripts/tag_with_claude.py ITEMS.jsonl ANSWERS.jsonl [--workers N]

Each message is one call with no tools, no project files, no memory and no session history: it runs from an empty
folder with the setting sources switched off, and its reply must match the answer schema. A message whose answers fail
the checks gets one retry, sent with the list of errors; whatever still fails is recorded, not retried again.
Answers already in ANSWERS.jsonl are skipped, so an interrupted run can be rerun. Stops cleanly at the plan's usage limit.

Environment (optional): SHAPE_MODEL (default claude-opus-5-5), SHAPE_EFFORT (default high),
CLAUDE_BIN (default: newest Claude desktop bundle, else `claude` on PATH), CLEAN_DIR (default: next to ANSWERS.jsonl).
"""
import argparse
import glob
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
import threading
import time
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, str(Path(__file__).resolve().parent))  # python3 -I leaves the script's folder off the path
from common import TASKS, check, clean_answer, list_of, load_jsonl, schema, system_prompt, task_of, user_message

MODEL = os.environ.get("SHAPE_MODEL", "claude-opus-5-5")
EFFORT = os.environ.get("SHAPE_EFFORT", "high")
# Variables the Claude desktop app sets for its own session; a tagging call must not inherit them.
DROP_ENV = ("CLAUDE_CODE_USER_EMAIL", "CLAUDE_CODE_SESSION_ID", "CLAUDE_CODE_HOST_SESSION_ID",
            "CLAUDE_CODE_CHILD_SESSION", "CLAUDE_CODE_CHILD_NOTES_DIR", "CLAUDE_CODE_MESSAGING_SOCKET",
            "CLAUDE_CODE_MESSAGING_TOKEN", "CLAUDE_CODE_SESSION_ATTENDED", "CLAUDE_CODE_TERMINAL_MCP_TOOLS",
            "CLAUDE_CODE_REPORT_FINDINGS", "CLAUDE_CODE_ENABLE_ASK_USER_QUESTION_TOOL", "CLAUDE_PID", "CLAUDECODE")
LIMIT_WORDS = re.compile(r"usage limit|limit reached|rate.?limit|weekly limit|out of (usage|credits)|429|"
                         r"hit your .{0,20}limit|5-hour limit|exceeded", re.I)


class LimitReached(Exception):
    pass


def claude_bin():
    if os.environ.get("CLAUDE_BIN"):
        return os.environ["CLAUDE_BIN"]
    found = glob.glob(os.path.expanduser(
        "~/Library/Application Support/Claude/claude-code/*/*/claude.app/Contents/MacOS/claude"))
    key = lambda p: [int(x) for x in re.findall(r"claude-code/([\d.]+)/", p)[0].split(".")]
    return sorted(found, key=key)[-1] if found else shutil.which("claude")


def ask(system, prompt, task, clean_dir):
    """One headless call. Returns (list of answers or None, raw text, seconds)."""
    cmd = [claude_bin(), "-p", "--model", MODEL, "--effort", EFFORT,
           "--setting-sources", "", "--strict-mcp-config", "--disable-slash-commands",
           "--system-prompt", system, "--tools", "", "--no-session-persistence",
           "--output-format", "json", "--json-schema", json.dumps(schema(task))]
    env = {k: v for k, v in os.environ.items() if k not in DROP_ENV}
    msg = ""
    for tries in range(3):
        started = time.time()
        p = subprocess.run(cmd, input=prompt, capture_output=True, text=True, cwd=clean_dir, env=env, timeout=1800)
        try:
            out = json.loads(p.stdout)
        except json.JSONDecodeError:
            out = {"is_error": True, "result": (p.stdout or p.stderr or "no output")[-2000:]}
        secs = round(time.time() - started, 1)
        if not out.get("is_error"):
            reply, text = out.get("structured_output"), out.get("result") or ""
            if reply is None and LIMIT_WORDS.search(text):
                raise LimitReached(text[:500])
            if reply is None:
                try:
                    reply = json.loads(re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip()))
                except json.JSONDecodeError:
                    reply = None
            return (reply or {}).get("answers") if isinstance(reply, dict) else None, text, secs
        msg = str(out.get("result", ""))
        if LIMIT_WORDS.search(msg):
            raise LimitReached(msg[:500])
        time.sleep(30 * (tries + 1))
    return None, msg, 0


def tag_chunk(task, system, items, clean_dir):
    """Tag one message's items; retry once with the errors. Returns (answers, attempts, errors, seconds)."""
    first = user_message(items)
    prompt, secs = first, 0.0
    for attempt in (1, 2):
        answers, text, s = ask(system, prompt, task, clean_dir)
        secs += s
        answers = [clean_answer(a) for a in answers or [] if isinstance(a, dict)]
        errs = check(task, items, answers) if answers else [f"no answers returned: {text[:300]}"]
        if not errs or attempt == 2:
            return answers, attempt, errs, secs
        prompt = (first + "\n\nYour previous reply was:\n" + json.dumps({"answers": answers}, ensure_ascii=False)
                  + "\n\nIt failed these checks:\n- " + "\n- ".join(errs)
                  + "\nFix only these problems and return the complete corrected JSON object.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("items"); ap.add_argument("answers")
    ap.add_argument("--workers", type=int, default=2)
    a = ap.parse_args()
    task = task_of(a.items)
    system, size = system_prompt(task), TASKS[task][1]
    items = load_jsonl(a.items)
    done = {x["id"] for x in load_jsonl(a.answers)} if os.path.exists(a.answers) else set()
    todo = [i for i in items if i["id"] not in done]
    chunks = [todo[n:n + size] for n in range(0, len(todo), size)]
    clean_dir = os.environ.get("CLEAN_DIR", os.path.join(os.path.dirname(os.path.abspath(a.answers)), ".clean"))
    os.makedirs(clean_dir, exist_ok=True)
    version = subprocess.run([claude_bin(), "--version"], capture_output=True, text=True).stdout.strip()
    print(f"{list_of(a.items)}: {len(todo)} to tag in {len(chunks)} messages, {len(done)} already done; "
          f"{MODEL} effort {EFFORT}; {a.workers} at a time; claude {version}", flush=True)
    lock, stop, failed = threading.Lock(), threading.Event(), []

    def work(n, chunk):
        if stop.is_set():
            return
        try:
            answers, attempts, errs, secs = tag_chunk(task, system, chunk, clean_dir)
        except LimitReached as e:
            stop.set()
            print(f"STOPPED at the usage limit: {e}", flush=True)
            return
        valid = {x["id"] for x in answers} - {e.split(":")[0] for e in errs}
        meta = {"model": MODEL, "effort": EFFORT, "claude_code": version, "attempts": attempts, "seconds": secs}
        with lock, open(a.answers, "a", encoding="utf-8") as f:
            for x in answers:
                if x["id"] in valid:
                    f.write(json.dumps({**x, "_meta": meta}, ensure_ascii=False) + "\n")
            if errs:
                failed.extend(errs)
            print(f"  message {n}: {len(valid)}/{len(chunk)} answered, attempts {attempts}, {secs:.0f}s"
                  + (f", {len(errs)} errors left" if errs else ""), flush=True)

    with ThreadPoolExecutor(a.workers) as ex:
        list(ex.map(lambda nc: work(*nc), enumerate(chunks, 1)))
    if failed:
        print(f"{len(failed)} errors not fixed by the retry; rerun to try the missing items again:", *failed[:10], sep="\n  ")
    sys.exit(3 if stop.is_set() else 0)


if __name__ == "__main__":
    main()
