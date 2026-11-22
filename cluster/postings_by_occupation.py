"""Every-title posting layer: assign each US LinkedIn posting to an O*NET occupation by its title, then aggregate.

    python3 -I postings_by_occupation.py TITLE_MAP OUT_DIR [--limit N]

TITLE_MAP is data/title-map.tsv from scripts/make_title_map.py (copied to the cluster). Postings whose normalised title
is `unique`, `rolled-up` or `decided` count for that occupation (or, failing an exact match, the longest leading or
trailing run of 2+ words that is: statuses `prefix` and `suffix`); `ambiguous` and unmatched titles are counted and the
most common ones are listed in the output, so a person can add decisions to tags/title-decisions.tsv and rerun.

Writes OUT_DIR/by-occupation.json.gz: per occupation, posting counts after two dedup steps, level counts, skill-phrase
counts overall and by level (top 400 phrases), first-stated minimum years by level, phase cue counts, date range.
No description text and no per-posting rows leave the cluster. Stdlib only (python/3.13.5 module on Explorer).
"""
import csv
import gzip
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from postings import KAGGLE, cues, member, min_years, seniority  # noqa: E402
from title_norm import norm_title  # noqa: E402

LEVELS = ["entry", "mid", "senior", "lead", "unmarked"]
TOP_PHRASES = 400


def lookup(tmap, k):
    """Exact normalised title first; else the longest leading, then trailing, run of 2+ words that resolves
    ("registered nurse icu" -> "registered nurse", "backend software engineer" -> "software engineer")."""
    status, soc = tmap.get(k, ("none", ""))
    if soc or status in ("ambiguous", "excluded"):
        return status, soc
    w = k.split()
    for n in range(len(w) - 1, 1, -1):
        st, sc = tmap.get(" ".join(w[:n]), ("none", ""))
        if sc:
            return "prefix", sc
    for n in range(len(w) - 1, 1, -1):
        st, sc = tmap.get(" ".join(w[-n:]), ("none", ""))
        if sc:
            return "suffix", sc
    return status, soc


def main(argv):
    title_map, out = Path(argv[1]), Path(argv[2])
    limit = int(argv[argv.index("--limit") + 1]) if "--limit" in argv else None
    out.mkdir(parents=True, exist_ok=True)
    tmap = {r["title_norm"]: (r["status"], r["soc"]) for r in csv.DictReader(open(title_map), delimiter="\t")}
    zp = KAGGLE / "asaniczka/1-3m-linkedin-jobs-and-skills-2024/v2/dataset.zip"
    sel, seen, stats, unresolved = {}, set(), Counter(), Counter()
    for i, r in enumerate(member(zp, "linkedin_job_postings.csv")):
        if limit and i >= limit:
            break
        stats["rows"] += 1
        if r["search_country"] != "United States":
            continue
        stats["us_rows"] += 1
        k = norm_title(r["job_title"])
        status, soc = lookup(tmap, k)
        stats[f"title:{status}"] += 1
        if not soc:
            unresolved[(status, k)] += 1
            continue
        key = (soc, r["company"].strip().lower(), r["job_title"].strip().lower(), r["job_location"].strip().lower())
        if key in seen:
            stats["dup:company-title-location"] += 1
            continue
        seen.add(key)
        lvl = seniority(r["job_title"], "software-developer" if soc.startswith("15-") else None)
        sel[r["job_link"]] = [soc, lvl, r["first_seen"], None, None, None, None]   # + skills, years, cues, text hash
    print("postings pass", dict(stats), flush=True)
    for r in member(zp, "job_skills.csv"):
        p = sel.get(r["job_link"])
        if p is not None:
            p[3] = [sys.intern(re.sub(r"\s+", " ", s.strip().strip(".;:-").lower())) for s in (r["job_skills"] or "").split(",") if s.strip()]
    print("skills pass done", flush=True)
    for r in member(zp, "job_summary.csv"):
        p = sel.get(r["job_link"])
        if p is not None:
            t = r["job_summary"] or ""
            p[4], p[5] = min_years(t), cues(t)
            p[6] = hashlib.md5(re.sub(r"\W+", " ", t.lower()).strip().encode()).hexdigest()[:12]
    print("summary pass done", flush=True)

    agg = defaultdict(lambda: {"n": 0, "levels": Counter(), "phr": Counter(), "phr_lvl": defaultdict(Counter),
                               "years": defaultdict(Counter), "cue": Counter(), "cue_n": 0, "dates": [None, None],
                               "with_skills": 0, "text_dups": 0})
    seen_h = set()
    for soc, lvl, d, sk, y, cu, h in sel.values():
        a = agg[soc]
        if h and (soc, h) in seen_h:
            a["text_dups"] += 1
            continue
        seen_h.add((soc, h))
        a["n"] += 1
        a["levels"][lvl] += 1
        a["dates"] = [min(filter(None, [a["dates"][0], d])), max(filter(None, [a["dates"][1], d]))]
        if sk:
            a["with_skills"] += 1
            for s in set(sk):
                a["phr"][s] += 1
                a["phr_lvl"][lvl][s] += 1
        if y is not None:
            a["years"][lvl][min(y, 16)] += 1
        if cu:
            a["cue_n"] += 1
            for j, b in enumerate(cu):
                a["cue"][j] += b
    res = {}
    for soc, a in agg.items():
        top = [s for s, _ in a["phr"].most_common(TOP_PHRASES)]
        res[soc] = {"n": a["n"], "text_dups": a["text_dups"], "with_skills": a["with_skills"], "levels": dict(a["levels"]),
                    "dates": a["dates"], "phrase_mentions": sum(a["phr"].values()),
                    "phrases": {s: [a["phr"][s]] + [a["phr_lvl"][L][s] for L in LEVELS] for s in top},
                    "level_mentions": {L: sum(a["phr_lvl"][L].values()) for L in LEVELS},
                    "years": {L: [a["years"][L][i] for i in range(17)] for L in LEVELS},
                    "cue": [a["cue"][j] for j in range(6)], "cue_n": a["cue_n"]}
    top_unresolved = [{"status": st, "title_norm": k, "postings": c} for (st, k), c in unresolved.most_common(500)]
    with gzip.open(out / "by-occupation.json.gz", "wt") as f:
        json.dump({"source": str(zp), "stats": stats, "levels": LEVELS, "occupations": res,
                   "top_unresolved_titles": top_unresolved}, f)
    print("done", len(res), "occupations", flush=True)


if __name__ == "__main__":
    main(sys.argv)
