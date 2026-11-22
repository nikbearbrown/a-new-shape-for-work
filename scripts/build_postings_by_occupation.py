"""Every-title posting layer, local half: data/postings/by-occupation.json.gz -> data/postings-by-occupation.json

Applies the same draft phrase -> phase rules and lexicon classes as the pilot (scripts/build_postings.py) to the
per-occupation phrase counts the cluster job wrote. Occupations with fewer than MIN_POSTINGS postings are listed with
counts only. Spelling variants that resolve to one lexicon concept are summed, so a posting that lists both "React" and
"React.js" counts twice for React (rare in this source).
"""
import gzip
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from build_postings import CRED, KIND_PANEL, PHASES, phase_of  # noqa: E402

MIN_POSTINGS = 50
MIN_LEVEL = 30


def profile(counts):
    tot = sum(counts.get(p, 0) for p in PHASES)
    return {p: round(counts.get(p, 0) / tot, 4) if tot else 0 for p in PHASES}, tot


def main():
    src = json.load(gzip.open(ROOT / "data/postings/by-occupation.json.gz", "rt"))
    forms = json.load(open(ROOT / "data/lexicon-forms.json"))
    levels = src["levels"]
    out = {}
    for soc, a in src["occupations"].items():
        rec = {"n": a["n"], "text_dups": a["text_dups"], "with_skills": a["with_skills"], "levels": a["levels"],
               "dates": a["dates"], "phrase_mentions": a["phrase_mentions"]}
        if a["n"] < MIN_POSTINGS:
            out[soc] = rec
            continue
        tot, by_lvl, matched = defaultdict(int), {L: defaultdict(int) for L in levels}, 0
        concepts = {}
        for phrase, counts in a["phrases"].items():
            ph = phase_of(phrase)
            if ph != "neutral":
                tot[ph] += counts[0]
                for L, c in zip(levels, counts[1:]):
                    by_lvl[L][ph] += c
            m = forms.get(phrase)
            if m:
                matched += counts[0]
                k = ("id", m[0])
            else:
                k = ("phrase", phrase)
            c = concepts.setdefault(k, {"count": 0, "forms": [], "m": m, "phase": ph})
            c["count"] += counts[0]
            c["forms"].append(phrase)
        prof, diag = profile(tot)
        # shares are taken over the phrases the cluster kept (each occupation's 400 most common), the only ones tagged
        rec["all_phrase_mentions"] = rec["phrase_mentions"]
        rec["phrase_mentions"] = sum(c[0] for c in a["phrases"].values())
        ladder = {}
        for L in levels:
            pr, n = profile(by_lvl[L])
            ladder[L] = {"n_postings": a["levels"].get(L, 0), "n_mentions": n, "profile": pr}
        stack, unmatched = defaultdict(list), []
        n = max(a["with_skills"], 1)
        for k, c in sorted(concepts.items(), key=lambda kv: -kv[1]["count"]):
            item = {"label": c["m"][1] if c["m"] else c["forms"][0], "phrase": "; ".join(c["forms"][:4]),
                    "id": c["m"][0] if c["m"] else None, "share": round(min(c["count"] / n, 1), 4), "phase": c["phase"]}
            if c["m"]:
                stack[KIND_PANEL.get(c["m"][2], "skills")].append(item)
            elif CRED.search(c["forms"][0]):
                stack["credentials"].append(item)
            else:
                unmatched.append(item)
        exp = {}
        for L in levels + ["all"]:
            h = [sum(a["years"][x][i] for x in levels) for i in range(17)] if L == "all" else a["years"][L]
            tot_y = sum(h)
            if tot_y:
                flat = [i for i, c in enumerate(h) for _ in range(c)]
                exp[L] = {"n": tot_y, "median": statistics.median_low(flat),
                          "share_2plus": round(sum(h[2:]) / tot_y, 3), "hist": h}
        rec.update({"profile": prof, "diagnostic_mentions": diag, "lexicon_matched_mentions": matched,
                    "ladder": ladder, "stack": {k: v[:12] for k, v in stack.items()}, "unmatched_top": unmatched[:15],
                    "experience": exp,
                    "cue_share": {p: round(a["cue"][i] / a["cue_n"], 3) if a["cue_n"] else 0 for i, p in enumerate(PHASES)}})
        out[soc] = rec
    st = src["stats"]
    us = st.get("us_rows", 0)
    assigned = sum(st.get(f"title:{s}", 0) for s in ("unique", "rolled-up", "decided", "prefix", "suffix"))
    summary = {"us_rows": us, "assigned": assigned, "stats": st,
               "occupations_with_postings": len(out), "occupations_charted": sum(1 for v in out.values() if "profile" in v),
               "top_unresolved_titles": src["top_unresolved_titles"][:60], "min_postings": MIN_POSTINGS,
               "min_level": MIN_LEVEL}
    (ROOT / "data/postings-by-occupation.json").write_text(json.dumps({"summary": summary, "occupations": out}))
    print(json.dumps({k: v for k, v in summary.items() if k != "top_unresolved_titles"}, indent=1))


if __name__ == "__main__":
    main()
