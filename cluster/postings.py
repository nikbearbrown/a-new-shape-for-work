"""Job Shape posting pilot: pull a few titles out of two allow-listed Kaggle posting sets.

Runs on Explorer (stdlib only, python/3.13.5 module). Reads the zips in place, writes compact JSONL.

  A. asaniczka/1-3m-linkedin-jobs-and-skills-2024 v2 (ODC-By): LinkedIn, first_seen Jan 2024.
     job_skills is a list a model extracted from each posting (the dataset's own NER step), not employer tags.
  B. lukebarousse/data-analyst-job-postings-google-search v744 (Apache 2.0): Google Jobs, data analyst
     searches, scraped daily Nov 2022 to Apr 2025. description_tokens = the dataset's own tool keywords.

Per posting we keep: title group, seniority read from the title, date, company, title, minimum years of
experience (first stated "N years ... experience"), skills/tokens, and six phase cue-phrase flags.
No description text leaves the cluster.
"""
import ast
import csv
import gzip
import hashlib
import io
import json
import re
import sys
import zipfile
from collections import Counter
from pathlib import Path

csv.field_size_limit(sys.maxsize)
KAGGLE = Path("/projects/aiskunks/kaggle/jobs/kaggle-data")
OUT = Path(".")   # set from argv in __main__, so other scripts can import the rules below without side effects

GROUPS = {   # title group -> (include regex, extra exclude regex)
    "software-developer": (r"\bsoftware (engineer|developer|development engineer)\b|\bfull[- ]?stack (engineer|developer)\b|"
                           r"\bback[- ]?end (engineer|developer)\b", r"\b(test|qa|quality|manager)\b"),
    "qa-tester": (r"\b(qa|quality assurance) (engineer|analyst|tester|specialist)\b|\bsoftware (test|qa) engineer\b|"
                  r"\btest automation engineer\b|\bsoftware tester\b|\bsdet\b", r"\bmanager\b"),
    "data-scientist": (r"\bdata scientist\b", r"\bmanager\b"),
    "data-analyst": (r"\bdata analyst\b", r"\bmanager\b"),
    "registered-nurse": (r"\bregistered nurse\b|\brn\b", r"\b(practitioner|manager|lpn|lvn|educator|anesthetist|midwife|"
                                                          r"case manager|care manager)\b"),
    "accountant": (r"\baccountant\b", r"\bmanager\b"),
    "electrician": (r"\belectrician\b", r"\b(manager|helper)\b"),
    "project-manager": (r"\bproject manager\b", r"\b(assistant|program manager)\b"),
}
COMMON_EXCLUDE = r"\b(intern|internship|director|vp|vice president|head of|instructor|teacher|professor|recruiter|faculty)\b"
G = {k: (re.compile(a, re.I), re.compile(b, re.I)) for k, (a, b) in GROUPS.items()}
CX = re.compile(COMMON_EXCLUDE, re.I)


def group_of(title):
    for k, (inc, exc) in G.items():
        if inc.search(title) and not exc.search(title) and not CX.search(title):
            return k
    return None


LEAD = re.compile(r"\b(principal|lead|distinguished|chief|architect)\b", re.I)
TECH = {"software-developer", "qa-tester", "data-scientist", "data-analyst"}   # "Staff" means a level only in tech titles
SENIOR = re.compile(r"\b(senior|sr\.?|iii|iv|level 3|level 4)\b", re.I)
MID = re.compile(r"\b(ii|mid|mid-level|intermediate|level 2)\b", re.I)
ENTRY = re.compile(r"\b(junior|jr\.?|entry|entry-level|associate|graduate|new grad|apprentice|trainee|level 1)\b", re.I)
ROMAN_I = re.compile(r"\bI\b|\b1\b")   # case-sensitive: "Software Engineer I"


def seniority(title, group=None):
    if re.search(r"\bstaff accountant\b", title, re.I):
        return "entry"                     # accounting usage: Staff Accountant is the entry rung
    if re.search(r"\bjourneyman\b", title, re.I):
        return "mid"
    if re.search(r"\bmaster electrician\b", title, re.I):
        return "senior"
    if LEAD.search(title) or (group in TECH and re.search(r"\bstaff\b", title, re.I)):
        return "lead"
    if SENIOR.search(title):
        return "senior"
    if MID.search(title) or re.search(r"\b2\b", title):
        return "mid"
    if ENTRY.search(title) or ROMAN_I.search(title):
        return "entry"
    return "unmarked"


WORDNUM = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
           "twelve": 12, "fifteen": 15}
YEARS = re.compile(r"(?<![\d.$])(\d{1,2}|one|two|three|four|five|six|seven|eight|nine|ten|twelve|fifteen)"
                   r"(?:\s*(?:-|–|to)\s*\d{1,2})?\s*\+?\s*(?:\(\d{1,2}\)\s*)?\+?\s*(?:years?|yrs?)\b(?:\W+\w+){0,6}?\W+experience",
                   re.I)


def min_years(text):
    m = YEARS.search(text or "")
    if not m:
        return None
    v = m.group(1).lower()
    v = WORDNUM.get(v, None) if not v.isdigit() else int(v)
    return v if v is not None and 0 <= v <= 25 else None


CUES = {   # draft cue phrases per phase; presence only. Noisy by design: shown as a cross-check, not the main series.
    "understand": r"requirements? gathering|gather(?:ing)? (?:business )?requirements|business requirements|"
                  r"understand(?:ing)? (?:the )?(?:business|customer|user|client) needs|user research|root[- ]cause|"
                  r"investigat\w+|exploratory|ad[- ]hoc analys\w+|patient assessments?|assess(?:ing)? patients?",
    "plan": r"\bdesign(?:s|ed|ing)?\b|architect\w*|roadmap|\bstrateg\w+|data model(?:l)?ing|care plans?|"
            r"\bplan(?:s|ning)?\b|estimat\w+|scop(?:e|ing) (?:projects?|work)",
    "produce": r"\bbuild(?:s|ing)?\b|\bdevelop(?:s|ing)? (?:dashboards?|reports?|models?|code|software|applications?|features?|"
               r"queries|pipelines?)|creat(?:e|ing) (?:dashboards?|reports?|visuali[sz]ations?)|"
               r"writ(?:e|ing) (?:sql|queries|code|scripts|software)|\bcod(?:e|ing)\b|automat(?:e|ing)\b|"
               r"administer(?:ing)? medications?|install(?:s|ing|ation)?\b|journal entries|prepar(?:e|ing) financial statements",
    "check": r"validat\w+|data quality|data integrity|\baccuracy\b|quality assurance|\bqa\b|\baudit\w*|\btest(?:s|ing)?\b|"
             r"reconcil\w+|\bverif\w+|code reviews?|peer reviews?|inspect\w*|compliance",
    "sustain": r"maintain\w*|maintenance|monitor\w*|troubleshoot\w*|\bsupport(?:s|ing)? (?:existing|ongoing|production)|"
               r"on[- ]call|production support|\bincidents?\b|\brepair\w*|month[- ]end close",
    "coordinate": r"stakeholders?|cross[- ]functional|collaborat\w+ with|partner(?:s|ing)? with|"
                  r"present(?:ing)? (?:findings|results|insights)|\bmentor\w*|lead (?:a )?teams?|coordinat\w+|"
                  r"supervis\w+|interdisciplinary team",
}
CUE_RX = [(k, re.compile(v, re.I)) for k, v in CUES.items()]


def cues(text):
    return [1 if rx.search(text or "") else 0 for _, rx in CUE_RX]


def member(zpath, name):
    z = zipfile.ZipFile(zpath)
    return csv.DictReader(io.TextIOWrapper(z.open(name), encoding="utf-8", errors="replace", newline=""))


def run_linkedin():
    zp = KAGGLE / "asaniczka/1-3m-linkedin-jobs-and-skills-2024/v2/dataset.zip"
    sel, seen, stats = {}, set(), Counter()
    for r in member(zp, "linkedin_job_postings.csv"):
        stats["rows"] += 1
        if r["search_country"] != "United States":
            continue
        stats["us_rows"] += 1
        g = group_of(r["job_title"])
        if not g:
            continue
        key = (r["company"].strip().lower(), r["job_title"].strip().lower(), r["job_location"].strip().lower())
        dup = key in seen
        seen.add(key)
        stats[f"sel:{g}"] += 1
        stats[f"dup:{g}"] += dup
        sel[r["job_link"]] = {"g": g, "s": seniority(r["job_title"], g), "lvl": r["job_level"], "d": r["first_seen"],
                              "co": r["company"], "t": r["job_title"], "dup": dup, "sk": None, "y": None, "cue": None,
                              "h": None}
    print("postings pass", dict(stats), flush=True)
    for r in member(zp, "job_skills.csv"):
        p = sel.get(r["job_link"])
        if p is not None:
            p["sk"] = [s.strip() for s in (r["job_skills"] or "").split(",") if s.strip()]
    print("skills pass done", flush=True)
    for r in member(zp, "job_summary.csv"):
        p = sel.get(r["job_link"])
        if p is not None:
            t = r["job_summary"] or ""
            p["y"], p["cue"] = min_years(t), cues(t)
            p["h"] = hashlib.md5(re.sub(r"\W+", " ", t.lower()).strip().encode()).hexdigest()[:12]
    print("summary pass done", flush=True)
    with gzip.open(OUT / "linkedin-2024.jsonl.gz", "wt") as f:
        for p in sel.values():
            f.write(json.dumps(p, ensure_ascii=False) + "\n")
    return stats


def run_gsearch():
    zp = KAGGLE / "lukebarousse/data-analyst-job-postings-google-search/v744/dataset.zip"
    seen, stats = set(), Counter()
    with gzip.open(OUT / "gsearch-data-analyst.jsonl.gz", "wt") as f:
        for r in member(zp, "gsearch_jobs.csv"):
            stats["rows"] += 1
            title = r.get("title") or ""
            if not re.search(r"\bdata analyst\b", title, re.I) or CX.search(title) or re.search(r"\bmanager\b", title, re.I):
                continue
            key = r.get("job_id") or (r.get("company_name", "").lower(), title.lower(), (r.get("location") or "").lower())
            if key in seen:
                stats["dup"] += 1
                continue
            seen.add(key)
            try:
                toks = ast.literal_eval(r.get("description_tokens") or "[]")
            except Exception:
                toks = []
            d = r.get("description") or ""
            f.write(json.dumps({"d": (r.get("date_time") or "")[:10], "s": seniority(title, "data-analyst"), "co": r.get("company_name"),
                                "t": title, "y": min_years(d), "tok": toks, "cue": cues(d), "len": len(d)}, ensure_ascii=False) + "\n")
            stats["kept"] += 1
    return stats


if __name__ == "__main__":
    OUT = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    OUT.mkdir(parents=True, exist_ok=True)
    s1 = run_gsearch()
    print("gsearch", dict(s1), flush=True)
    if len(sys.argv) > 2 and sys.argv[2] == "gsearch-only":
        sys.exit(0)
    s2 = run_linkedin()
    (OUT / "stats.json").write_text(json.dumps({"linkedin": s2, "gsearch": s1, "cues": CUES,
                                                 "groups": GROUPS, "common_exclude": COMMON_EXCLUDE}, indent=1))
    print("done", flush=True)
