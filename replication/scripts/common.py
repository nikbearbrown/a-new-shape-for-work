"""Shared pieces of the replication kit: the three tasks, their prompts, and the answer checks. Standard library only."""
import json
from pathlib import Path

KIT = Path(__file__).resolve().parents[1]
PHASES = ["understand", "plan", "produce", "check", "sustain", "coordinate"]
CONFIDENCE = ["high", "medium", "low"]
TASKS = {
    # task: (prompt template, items per message)
    "dwa": ("system-dwa.txt", 30),
    "titles": ("system-titles.txt", 25),
    "phrases": ("system-phrases.txt", 50),
}


def task_of(path):
    """dwa, titles or phrases, from an item file's name (dwa-pilot.jsonl, titles-batch-01.jsonl, ...)."""
    name = Path(path).name
    for t in TASKS:
        if name.startswith(t + "-"):
            return t
    raise SystemExit(f"can't tell the task from the file name {name}: it must start with dwa-, titles- or phrases-")


def list_of(path):
    """The list name, for example dwa-pilot or phrases-batch-02."""
    return Path(path).name.removesuffix(".jsonl")


def load_jsonl(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def occupations():
    rows = (KIT / "items/occupations.tsv").read_text(encoding="utf-8").splitlines()[1:]
    return dict(r.split("\t", 1) for r in rows)


def system_prompt(task):
    """The full instructions for a task: its template with the phases, the answer format and (for titles) the
    occupation list filled in. These are the words every model gets."""
    p = KIT / "prompts"
    text = (p / TASKS[task][0]).read_text(encoding="utf-8")
    text = text.replace("PHASES\n", (p / "phases.txt").read_text(encoding="utf-8"))
    text = text.replace("FORMAT\n", (p / "answer-format.txt").read_text(encoding="utf-8"))
    if "OCCUPATIONS\n" in text:
        occ = occupations()
        text = text.replace("OCCUPATIONS\n", "Occupation list (O*NET-SOC code, title):\n"
                            + "".join(f"{s}\t{t}\n" for s, t in occ.items()))
    return text


def user_message(items):
    lines = "\n".join(json.dumps(i, ensure_ascii=False) for i in items)
    return (f"Here are {len(items)} items. Each line is one item, as JSON.\n\n{lines}\n\n"
            f"Return the JSON object described in your instructions, with one answer for each of the {len(items)} items.")


def answer_values(task):
    if task == "dwa":
        return PHASES, PHASES
    if task == "phrases":
        return PHASES + ["neutral"], PHASES
    codes = list(occupations()) + ["-"]
    return codes, codes


def schema(task):
    """JSON schema for one message's reply (used with `claude -p --json-schema`)."""
    ans, alt = answer_values(task)
    item = {"type": "object", "additionalProperties": False, "required": ["id", "answer", "alt", "confidence", "reason"],
            "properties": {"id": {"type": "string"}, "answer": {"type": "string", "enum": ans},
                           "alt": {"type": ["string", "null"], "enum": alt + [None]},
                           "confidence": {"type": "string", "enum": CONFIDENCE}, "reason": {"type": "string"}}}
    return {"type": "object", "additionalProperties": False, "required": ["answers"],
            "properties": {"answers": {"type": "array", "items": item}}}


def check(task, items, answers):
    """Errors (list of strings) for a set of answers against the items they answer. Empty list = pass."""
    ans_ok, alt_ok = answer_values(task)
    ans_ok, alt_ok = set(ans_ok), set(alt_ok)
    want = {i["id"] for i in items}
    errs, seen = [], {}
    for a in answers:
        i = a.get("id")
        if i not in want:
            errs.append(f"{i}: not one of the items sent")
            continue
        if i in seen:
            errs.append(f"{i}: answered more than once")
            continue
        seen[i] = a
        if a.get("answer") not in ans_ok:
            errs.append(f"{i}: answer {a.get('answer')!r} is not allowed")
        if a.get("alt") is not None and (a["alt"] not in alt_ok or a["alt"] == a.get("answer")):
            errs.append(f"{i}: alt {a.get('alt')!r} is not allowed (it must differ from answer, or be null)")
        if a.get("confidence") not in CONFIDENCE:
            errs.append(f"{i}: confidence must be high, medium or low")
        if not isinstance(a.get("reason"), str) or not a["reason"].strip():
            errs.append(f"{i}: reason is missing")
    for i in sorted(want - set(seen)):
        errs.append(f"{i}: no answer")
    return errs


def clean_answer(a):
    """The answer fields only, without anything a runner added."""
    return {k: a.get(k) for k in ("id", "answer", "alt", "confidence", "reason")}

