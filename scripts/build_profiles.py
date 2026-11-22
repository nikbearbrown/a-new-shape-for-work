"""O*NET-only effort profiles for every occupation with task ratings -> data/onet-profiles.json.

For each task: frequency distribution over O*NET's seven categories (FT), importance (IM, 1-5), relevance (RT, % of
incumbents who say the task is part of the job). The task's phases come from its DWAs (equal split across its DWAs).

Three effort models, all labelled ESTIMATED; none is time data:
  ordinal     w = mean frequency category (1-7) x IM x RT/100.  Main series. Categories are roughly log-spaced,
              so this treats a daily task as worth ~2x a monthly one, not 20x.
  occurrence  w = expected occurrences per year x IM x RT/100, categories mapped to 1, 4, 24, 100, 250, 750, 2000.
              Treats every occurrence as equally long, so hourly micro-tasks dominate.
  flat        w = IM x RT/100.  Ignores frequency.
Also a cross-check from the Work Activities ratings: sum over GWAs of (IM - 1), each GWA split by its DWAs' phases.
"""
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "source/onet-31.0"
PHASES = ["understand", "plan", "produce", "check", "sustain", "coordinate"]
OCC_PER_YEAR = [1, 4, 24, 100, 250, 750, 2000]
FEATURED = ["15-1252.00", "15-1253.00", "15-2051.00", "15-2051.01", "29-1141.00", "13-2011.00", "47-2111.00",
            "13-1082.00", "15-1254.00", "15-1244.00", "15-1212.00", "15-1211.00", "15-1242.00", "15-1299.08"]


def tsv(name):
    return csv.DictReader(open(SRC / name, encoding="utf-8", errors="replace"), delimiter="\t")


def norm(v):
    s = sum(v.values()) or 1
    return {p: round(v.get(p, 0) / s, 4) for p in PHASES}


AEI = ROOT / "source/anthropic-economic-index/labor-market-impacts/task_penetration.csv"


def load_aei():
    """Anthropic Economic Index task coverage, keyed by lower-cased task text. Empty if not downloaded."""
    if not AEI.exists():
        return {}
    key = lambda t: re.sub(r"\s+", " ", t.strip().lower())
    return {key(r["task"]): float(r["penetration"]) for r in csv.DictReader(open(AEI, encoding="utf-8"))}


def main():
    aei = load_aei()
    aei_key = lambda t: re.sub(r"\s+", " ", t.strip().lower())
    occ = {r["O*NET-SOC Code"]: r for r in tsv("Occupation Data.txt")}
    zones = {r["O*NET-SOC Code"]: int(r["Job Zone"]) for r in tsv("Job Zones.txt")}
    dwa = {r["dwa_id"]: r for r in csv.DictReader(open(ROOT / "tags/dwa-phase-tags.tsv"), delimiter="\t")}
    dwa_gwa = {r["DWA Element ID"]: r["GWA Element ID"] for r in tsv("GWAs to IWAs to DWAs.txt")}
    tasks = defaultdict(dict)
    for r in tsv("Task Statements.txt"):
        tasks[r["O*NET-SOC Code"]][r["Task ID"]] = {"text": r["Task"], "type": r["Task Type"], "ft": [0.0] * 7,
                                                     "im": None, "rt": None, "dwas": []}
    for r in tsv("Task Ratings.txt"):
        t = tasks[r["O*NET-SOC Code"]].get(r["Task ID"])
        if t is None:
            continue
        v = float(r["Data Value"])
        if r["Scale ID"] == "FT":
            t["ft"][int(r["Category"]) - 1] = v
        elif r["Scale ID"] == "IM":
            t["im"] = v
        elif r["Scale ID"] == "RT":
            t["rt"] = v
    for r in tsv("Tasks to DWAs.txt"):
        t = tasks[r["O*NET-SOC Code"]].get(r["Task ID"])
        if t is not None:
            t["dwas"].append(r["DWA Element ID"])
    # GWA importance per occupation, and each GWA's phase split (over all its DWAs, unweighted)
    gwa_split = defaultdict(Counter)
    for d, g in dwa_gwa.items():
        gwa_split[g][dwa[d]["phase"]] += 1
    gwa_im = defaultdict(dict)
    for r in tsv("Work Activities.txt"):
        if r["Scale ID"] == "IM":
            gwa_im[r["O*NET-SOC Code"]][r["Element ID"]] = float(r["Data Value"])

    out, review = {}, []
    for soc, ts in sorted(tasks.items()):
        rated = {k: t for k, t in ts.items() if t["im"] is not None and sum(t["ft"]) > 0}
        if not rated:
            continue
        prof = {m: Counter() for m in ("ordinal", "occurrence", "flat")}
        cov = {m: Counter() for m in prof}          # weight that is both in a phase and covered by observed AI use
        aei_missing = 0
        unlinked, rows = 0, []
        for tid, t in rated.items():
            p = t["ft"]
            tot = sum(p)
            mean_cat = sum((i + 1) * x for i, x in enumerate(p)) / tot
            occ_yr = sum(OCC_PER_YEAR[i] * x for i, x in enumerate(p)) / tot
            rel = (t["rt"] if t["rt"] is not None else 100) / 100
            w = {"ordinal": mean_cat * t["im"] * rel, "occurrence": occ_yr * t["im"] * rel, "flat": t["im"] * rel}
            split = Counter(dwa[d]["phase"] for d in t["dwas"] if d in dwa)
            if not split:
                unlinked += 1
                continue
            n = sum(split.values())
            pen = aei.get(aei_key(t["text"])) if aei else None
            if aei and pen is None:
                aei_missing += 1
            for m in prof:
                for ph, c in split.items():
                    prof[m][ph] += w[m] * c / n
                    cov[m][ph] += w[m] * c / n * (pen or 0)
            modal = max(range(7), key=lambda i: p[i])
            rows.append({"id": tid, "x": t["text"], "ty": t["type"][:1], "im": t["im"], "rt": round(rel * 100),
                         "mc": round(mean_cat, 2), "md": modal + 1, "ft": [round(v) for v in p],
                         "ph": {k: round(v / n, 3) for k, v in split.items()}, "pen": pen,
                         "dw": [[d, dwa[d]["dwa_name"], dwa[d]["phase"], dwa[d]["basis"]] for d in t["dwas"] if d in dwa]})
        gw = Counter()
        for g, im in gwa_im.get(soc, {}).items():
            tot = sum(gwa_split[g].values()) or 1
            for ph, c in gwa_split[g].items():
                gw[ph] += max(im - 1, 0) * c / tot
        out[soc] = {"title": occ[soc]["Title"], "zone": zones.get(soc), "n_tasks": len(rated), "unlinked": unlinked,
                    "profiles": {m: norm(v) for m, v in prof.items()}, "gwa": norm(gw), "tasks": rows,
                    "covered": {m: {p: round(cov[m][p] / (sum(prof[m].values()) or 1), 4) for p in PHASES} for m in prof},
                    "aei_missing": aei_missing}
        if soc in FEATURED:
            review.append(f"\n## {soc} {occ[soc]['Title']}  ordinal={out[soc]['profiles']['ordinal']}")
            for t in sorted(rows, key=lambda t: -t["im"] * t["rt"]):
                review.append(f"  [{t['ty']}] IM {t['im']} RT {t['rt']} md {t['md']}  {t['x'][:110]}")
                for d in t["dw"]:
                    review.append(f"      {d[2]:10s} {d[3]:6s} {d[0]}  {d[1]}")
    (ROOT / "data").mkdir(exist_ok=True)
    (ROOT / "data/onet-profiles.json").write_text(json.dumps(out, ensure_ascii=False))
    (ROOT / "data/review-dwa.txt").write_text("\n".join(review))
    print(len(out), "occupations;", sum(o["unlinked"] for o in out.values()), "rated tasks without DWAs")


if __name__ == "__main__":
    main()
