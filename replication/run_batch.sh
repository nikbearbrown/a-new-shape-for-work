#!/bin/bash
# Tag one item list end to end with Claude Code (headless, on your own plan), check it, and write the manifest.
# Usage: replication/run_batch.sh ITEMS.jsonl RUN_DIR
#   ITEMS.jsonl  a file from replication/items/ (dwa-pilot.jsonl, titles-batch-01.jsonl, ...)
#   RUN_DIR      your hand-in folder, shape-<list>-<model>-<YYYYMMDD> (INSTRUCTIONS.md, section 7)
# Optional: SHAPE_MODEL (default claude-opus-5-5), SHAPE_EFFORT (default high), WORKERS (parallel calls, default 2).
# Another model instead of Claude Code: scripts/render_prompts.py, then scripts/check_answers.py (README.md).
set -u
K=$(cd "$(dirname "$0")" && pwd)
ITEMS=$1
W=$2
mkdir -p "$W"
echo "== tagging $(date)"
python3 -I "$K/scripts/tag_with_claude.py" "$ITEMS" "$W/answers.jsonl" --workers "${WORKERS:-2}"
code=$?
python3 -I "$K/scripts/check_answers.py" "$ITEMS" "$W/answers.jsonl" "$W/report.json"
python3 -I "$K/scripts/write_manifest.py" "$ITEMS" "$W" > /dev/null
[ $code -eq 3 ] && { echo "== stopped at the usage limit $(date); rerun the same command to finish"; exit 3; }
echo "== done $(date)"
