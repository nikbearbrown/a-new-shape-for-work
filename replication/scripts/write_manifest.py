#!/usr/bin/env python3
"""Record what a run used: python3 -I replication/scripts/write_manifest.py ITEMS.jsonl RUN_DIR

Writes RUN_DIR/manifest.json: the list, file hashes of the items and the exact instructions, the model settings
found in the answers, the check result, and the kit's git commit if there is one.
"""
import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # python3 -I leaves the script's folder off the path
from common import KIT, list_of, load_jsonl, system_prompt, task_of


def main():
    items_path, run = sys.argv[1], Path(sys.argv[2])
    task = task_of(items_path)
    answers = load_jsonl(run / "answers.jsonl") if (run / "answers.jsonl").exists() else []
    report = json.loads((run / "report.json").read_text()) if (run / "report.json").exists() else {}
    sha = lambda b: hashlib.sha256(b).hexdigest()
    commit = subprocess.run(["git", "-C", str(KIT), "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
    settings = Counter(json.dumps({k: v for k, v in (a.get("_meta") or {}).items() if k in ("model", "effort", "claude_code")},
                                  sort_keys=True) for a in answers)
    manifest = {"list": list_of(items_path), "task": task,
                "items_sha256": sha(Path(items_path).read_bytes()),
                "instructions_sha256": sha(system_prompt(task).encode("utf-8")),
                "kit_commit": commit.stdout.strip() or None,
                "settings": [json.loads(s) | {"answers": n} for s, n in settings.items()],
                "answers": len(answers), "check": report.get("status"), "errors": len(report.get("errors", []))}
    (run / "manifest.json").write_text(json.dumps(manifest, indent=1), encoding="utf-8")
    print(json.dumps(manifest))


if __name__ == "__main__":
    main()
