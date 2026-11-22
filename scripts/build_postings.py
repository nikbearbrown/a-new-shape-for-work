"""Posting-side layers for the Job Shape prototype -> data/postings-summary.json

Inputs (from cluster/postings.py): data/postings/linkedin-2024.jsonl.gz, data/postings/gsearch-data-analyst.jsonl.gz
Lexicon forms: data/lexicon-forms.json (scripts/export_lexicon_forms.py). Phase tags for skill phrases: PHRASE_RULES
below, written to tags/skill-phrase-phase-tags.tsv for every phrase that reaches the charts.
"""
import csv
import gzip
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASES = ["understand", "plan", "produce", "check", "sustain", "coordinate"]
LEVELS = ["entry", "mid", "senior", "lead", "unmarked"]
GROUP_SOC = {"software-developer": "15-1252.00", "qa-tester": "15-1253.00", "data-scientist": "15-2051.00",
             "data-analyst": "15-2051.01", "registered-nurse": "29-1141.00", "accountant": "13-2011.00",
             "electrician": "47-2111.00", "project-manager": "13-1082.00"}

# A phrase is phase-diagnostic only if one of these fires; everything else (tools, languages, soft skills,
# credentials, domains) is neutral. First match wins. Draft, unreviewed.
PHRASE_RULES = [
    ("neutral", r"\b(communication|teamwork|collaborat\w*|interpersonal|problem[- ]?solving|analytical|attention to detail|"
                r"critical thinking|time management|organization(al)? skills|customer service|self[- ]motivated)\b"),
    ("neutral", r"401\(?k|\binsurance\b|\bpto\b|paid|benefits?\b|compensation|tuition|\bdrug (test|screen)|background check|"
                r"professional development|continuing education|\bagile\b|\bscrum\b(?! master)|kanban|"
                r"\bhealth (plan|care plan)\b|retirement|wellness"),
    ("check", r"\b(test(s|ing)?|qa|quality assurance|quality control|code reviews?|peer reviews?|audit(s|ing)?|inspection|"
              r"verification|validation|compliance|reconciliation|reconciliations|regression|accuracy|"
              r"internal controls?|sox|gaap compliance|quality improvement|chart review)\b"),
    ("sustain", r"\b(troubleshoot\w*|debugging|maintenance|monitoring|incident|on[- ]call|production support|"
                r"technical support|ci/cd|devops|site reliability|security|infection control|patient safety|repair\w*|"
                r"preventive|safety protocols|osha|month[- ]end close|year[- ]end close|close process)\b"),
    ("understand", r"\b(requirements|research|assessment|assessments|discovery|root cause|data analysis|"
                   r"statistical analysis|analysis|analytics|exploratory|diagnos\w+|blueprint reading|"
                   r"reading blueprints|schematics|diagrams|triage|patient evaluation)\b"),
    ("plan", r"\b(design|architecture|planning|plans?|strategy|strategic|roadmap|budget\w*|forecast\w*|estimat\w+|"
             r"scheduling|scope|data model(l)?ing|system design|care plan\w*)\b"),
    ("coordinate", r"\b(project management|program management|stakeholder\w*|leadership|leading|mentor\w*|supervis\w+|"
                   r"team management|people management|vendor management|delegation|coordination|coordinating|"
                   r"case management|change management|scrum master|client relations|relationship management)\b"),
    ("produce", r"\b(development|developing|programming|coding|software engineering|implementation|"
                r"data entry|bookkeeping|financial reporting|financial statements|journal entries|general ledger|"
                r"accounts (payable|receivable)|tax preparation|payroll|patient care|medication administration|"
                r"wound care|iv therapy|nursing care|direct care|bedside|electrical wiring|wiring|installation|"
                r"conduit|documentation|technical writing|data visuali[sz]ation|dashboards?|reporting|etl|"
                r"data pipelines?|machine learning model|model development|feature engineering|automation|"
                r"scripting|construction|charting|cost accounting)\b"),
]
RX = [(p, re.compile(r, re.I)) for p, r in PHRASE_RULES]
CRED = re.compile(r"\b(degree|bachelor'?s?|master'?s?|ph\.?d|diploma|licen[sc]e|licensed|certification|certified|"
                  r"certificate|cpa|bls|acls|pals|nihss|cna|bsn|msn|rn\b|journeyman)\b", re.I)
KIND_PANEL = {"tool": "tools", "platform": "tools", "library": "tools", "framework": "tools", "standard": "tools",
              "programming-language": "languages", "markup-language": "languages", "modeling-language": "languages",
              "style-language": "languages", "human-language": "languages", "credential": "credentials",
              "knowledge": "knowledge", "skill": "skills", "method": "skills", "ability": "skills"}


def norm(s):
    return re.sub(r"\s+", " ", s.strip().strip(".;:-").lower())


def phase_of(phrase):
    if CRED.search(phrase):
        return "neutral"
    for p, rx in RX:
        if rx.search(phrase):
            return p
    return "neutral"


def profile(counter):
    tot = sum(counter[p] for p in PHASES)
    return {p: round(counter[p] / tot, 4) if tot else 0 for p in PHASES}, tot


def linkedin(forms):
    rows = [json.loads(l) for l in gzip.open(ROOT / "data/postings/linkedin-2024.jsonl.gz", "rt")]
    out, tagrows = {}, {}
    seen_h = set()
    for g in GROUP_SOC:
        R = [r for r in rows if r["g"] == g]
        raw = len(R)
        R = [r for r in R if not r["dup"]]
        keyed = len(R)
        keep = []
        for r in R:
            if r["h"] and (g, r["h"]) in seen_h:
                continue
            seen_h.add((g, r["h"]))
            keep.append(r)
        R = keep
        withsk = [r for r in R if r["sk"]]
        share, cls = Counter(), {}
        lvl_ph = defaultdict(Counter)
        tot_ph, all_mentions = Counter(), 0
        lvl_n = Counter(r["s"] for r in withsk)
        for r in withsk:
            ph = set()
            for s in {norm(x) for x in r["sk"] if norm(x)}:
                share[s] += 1
                all_mentions += 1
                p = phase_of(s)
                tagrows.setdefault(s, p)
                if p != "neutral":
                    tot_ph[p] += 1
                    lvl_ph[r["s"]][p] += 1
        prof, diag = profile(tot_ph)
        ladder = {}
        for L in LEVELS:
            pr, n = profile(lvl_ph[L])
            ladder[L] = {"n_postings": lvl_n[L], "n_mentions": n, "profile": pr}
        # requirement stack: top phrases by share, panelled by lexicon class
        # one count per posting per concept: spelling variants (React, React.js, ReactJS) merge on the lexicon id
        concept_n, concept_forms = Counter(), defaultdict(Counter)
        for r in withsk:
            keys = set()
            for s in {norm(x) for x in r["sk"] if norm(x)}:
                m = forms.get(s)
                k = ("id", m[0]) if m else ("phrase", s)
                keys.add(k)
                concept_forms[k][s] += 1
            for k in keys:
                concept_n[k] += 1
        stack = defaultdict(list)
        unmatched = []
        n = len(withsk)
        for k, c in concept_n.most_common(500):
            top_phrase = concept_forms[k].most_common(1)[0][0]
            phrases = [p for p, _ in concept_forms[k].most_common(4)]
            if k[0] == "id":
                m = forms[top_phrase]
                panel = KIND_PANEL.get(m[2], "skills")
                stack[panel].append({"label": m[1], "phrase": "; ".join(phrases), "id": m[0], "share": round(c / n, 4),
                                     "phase": phase_of(top_phrase)})
            else:
                panel = "credentials" if CRED.search(top_phrase) else None
                item = {"label": top_phrase, "phrase": top_phrase, "id": None, "share": round(c / n, 4),
                        "phase": phase_of(top_phrase)}
                (stack[panel].append(item) if panel else unmatched.append(item))
        matched_mentions = sum(c for s, c in share.items() if s in forms)
        # experience
        yrs = defaultdict(list)
        for r in R:
            if r["y"] is not None:
                yrs[r["s"]].append(r["y"])
                yrs["all"].append(r["y"])
        exp = {}
        for k, v in yrs.items():
            v.sort()
            exp[k] = {"n": len(v), "median": v[len(v) // 2], "share_2plus": round(sum(x >= 2 for x in v) / len(v), 3),
                      "hist": [sum(1 for x in v if x == i) for i in range(16)] + [sum(1 for x in v if x > 15)]}
        cue = Counter()
        cue_n = 0
        for r in R:
            if r["cue"]:
                cue_n += 1
                for i, b in enumerate(r["cue"]):
                    cue[PHASES[i]] += b
        out[g] = {"soc": GROUP_SOC[g], "raw": raw, "after_key_dedup": keyed, "after_text_dedup": len(R),
                  "with_skills": n, "levels": dict(lvl_n), "phrase_mentions": all_mentions, "diagnostic_mentions": diag,
                  "lexicon_matched_mentions": matched_mentions, "profile": prof, "ladder": ladder,
                  "stack": {k: v[:12] for k, v in stack.items()}, "unmatched_top": unmatched[:15],
                  "experience": exp,
                  "cue_share": {p: round(cue[p] / cue_n, 3) if cue_n else 0 for p in PHASES}, "cue_n": cue_n,
                  "dates": [min(r["d"] for r in R), max(r["d"] for r in R)]}
    with open(ROOT / "tags/skill-phrase-phase-tags.tsv", "w", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["phrase", "phase", "basis", "status"])
        for s, p in sorted(tagrows.items()):
            if p != "neutral":
                w.writerow([s, p, "rule", "draft"])
    return out


def gsearch():
    R = [json.loads(l) for l in gzip.open(ROOT / "data/postings/gsearch-data-analyst.jsonl.gz", "rt")]
    half = lambda d: f"{d[:4]}-H{1 if int(d[5:7]) <= 6 else 2}"
    by_half = defaultdict(list)
    for r in R:
        by_half[half(r["d"])].append(r)
    tok_rank = {}
    for h, rs in sorted(by_half.items()):
        c = Counter(t for r in rs for t in set(r["tok"]))
        tok_rank[h] = {"n": len(rs), "share": {t: round(v / len(rs), 4) for t, v in c.most_common(25)}}
    years = {}
    for y in ("2022", "2023", "2024", "2025"):
        rs = [r for r in R if r["d"][:4] == y]
        v = sorted(r["y"] for r in rs if r["y"] is not None)
        ent = [r["y"] for r in rs if r["s"] == "entry" and r["y"] is not None]
        months = sorted({r["d"][:7] for r in rs})
        years[y] = {"n_postings": len(rs), "n_with_years": len(v), "median": v[len(v) // 2] if v else None,
                    "share_2plus": round(sum(x >= 2 for x in v) / len(v), 3) if v else None,
                    "entry_n": len(ent), "entry_share_2plus": round(sum(x >= 2 for x in ent) / len(ent), 3) if ent else None,
                    "hist": [sum(1 for x in v if x == i) for i in range(16)] + [sum(1 for x in v if x > 15)],
                    "months": [months[0], months[-1]] if months else None}
    cues = {}
    for y in ("2023", "2025"):
        rs = [r for r in R if r["d"][:4] == y]
        L = sorted(r["len"] for r in rs if r.get("len") is not None)
        cues[y] = {"n": len(rs), "share": {p: round(sum(r["cue"][i] for r in rs) / len(rs), 3) for i, p in enumerate(PHASES)},
                   "len_median": L[len(L) // 2] if L else None}
    return {"n": len(R), "dates": [min(r["d"] for r in R), max(r["d"] for r in R)], "tokens": tok_rank,
            "years": years, "cues": cues, "levels": dict(Counter(r["s"] for r in R))}


if __name__ == "__main__":
    forms = json.load(open(ROOT / "data/lexicon-forms.json"))
    res = {"gsearch": gsearch()}
    if (ROOT / "data/postings/linkedin-2024.jsonl.gz").exists():
        res["linkedin"] = linkedin(forms)
    (ROOT / "data/postings-summary.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res["gsearch"]["years"], indent=0)[:1500])
    print(res["gsearch"]["cues"])
