"""Pack data/onet-profiles.json + data/postings-summary.json into the page's two data files under page/data/."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASES = ["understand", "plan", "produce", "check", "sustain", "coordinate"]


def main():
    prof = json.load(open(ROOT / "data/onet-profiles.json"))
    dwa_rows = list(csv.DictReader(open(ROOT / "tags/dwa-phase-tags.tsv"), delimiter="\t"))
    dwa_ix = {r["dwa_id"]: i for i, r in enumerate(dwa_rows)}
    occ = []
    for soc, o in prof.items():
        tasks = []
        for t in o["tasks"]:
            tasks.append([t["x"], t["ty"], t["im"], t["rt"], t["md"], t["mc"], t["ft"],
                          [round(t["ph"].get(p, 0), 3) for p in PHASES], [dwa_ix[d[0]] for d in t["dw"]], t.get("pen")])
        occ.append({"soc": soc, "title": o["title"], "zone": o["zone"],
                    "p": {m: [o["profiles"][m][p] for p in PHASES] for m in o["profiles"]},
                    "c": {m: [o["covered"][m][p] for p in PHASES] for m in o["covered"]}, "am": o["aei_missing"],
                    "tasks": tasks})
    dwas = [[r["dwa_name"], PHASES.index(r["phase"]), r["basis"]] for r in dwa_rows]
    out = ROOT / "page/data"
    out.mkdir(parents=True, exist_ok=True)
    (out / "onet.json").write_text(json.dumps({"phases": PHASES, "occupations": occ, "dwas": dwas},
                                              ensure_ascii=False, separators=(",", ":")))
    post = json.load(open(ROOT / "data/postings-summary.json"))
    (out / "postings.json").write_text(json.dumps(post, ensure_ascii=False, separators=(",", ":")))
    by = ROOT / "data/postings-by-occupation.json"
    if by.exists():
        b = json.load(open(by))
        for v in b["occupations"].values():
            for items in list(v.get("stack", {}).values()) + [v.get("unmatched_top", [])]:
                for it in items:
                    it["phrase"] = "; ".join(it["phrase"].split("; ")[:3])
            for e in v.get("experience", {}).values():
                e.pop("hist", None)
        (out / "by-occupation.json").write_text(json.dumps(b, ensure_ascii=False, separators=(",", ":")))
    for f in out.iterdir():
        print(f, f.stat().st_size)


if __name__ == "__main__":
    main()
