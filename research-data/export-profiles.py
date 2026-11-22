"""Export two analysis tables from the public prototype JSON. Python 3 stdlib."""
import csv
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA = ROOT / "page" / "data"

def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))

def save(name, fields, rows):
    with (HERE / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(fields)
        writer.writerows(rows)

def verify_snapshot():
    manifest = json.loads((HERE / "SOURCE-MANIFEST.json").read_text(encoding="utf-8"))
    snapshots = [(ROOT / a["path"], a["sha256"]) for a in manifest["prototype_artifacts"]]
    snapshots += [(HERE / a["path"], a["sha256"]) for a in manifest["inputs"] if "path" in a]
    for path, digest in snapshots:
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
            raise SystemExit(f"Missing or changed pinned data: {path}; export stopped.")


def main():
    verify_snapshot()
    onet = load("onet.json")
    postings = load("by-occupation.json")
    phases = tuple(onet["phases"])
    assert len(phases) == 6
    models = ("ordinal", "occurrence", "flat")
    save("activity-profiles.csv",
         ("onet_soc", "occupation", "weighting_model", "phase", "activity_share",
          "ai_penetration_weighted_share", "task_count", "unmatched_task_penetration_count"),
         ((o["soc"], o["title"], m, ph, o["p"][m][i], o["c"][m][i],
           len(o["tasks"]), o["am"])
          for o in sorted(onet["occupations"], key=lambda o: o["soc"]) for m in models for i, ph in enumerate(phases)))
    save("posting-emphasis.csv",
         ("onet_soc", "phase", "diagnostic_mention_share", "retained_ads", "ads_with_skills",
          "all_phrase_mentions", "top_phrase_mentions", "diagnostic_mentions", "first_seen", "last_seen",
          "passes_display_cutoff"),
         ((soc, ph, (o.get("profile") or {}).get(ph), o["n"], o.get("with_skills"),
           o.get("all_phrase_mentions"), o.get("phrase_mentions"), o.get("diagnostic_mentions"),
           *o["dates"], int(o["n"] >= postings["summary"]["min_postings"]))
          for soc, o in sorted(postings["occupations"].items()) for ph in phases))

if __name__ == "__main__":
    main()
