"""Job title -> O*NET occupation lookup -> data/title-map.tsv

Every title O*NET lists for an occupation (Occupation Data titles, Job Titles.txt alternate titles, Sample of Reported
Titles.txt), normalised the same way cluster/title_norm.py normalises posting titles. A title that lands on one
occupation is `unique`; on a base occupation and its own sub-occupations (29-1141.00, 29-1141.03) it is `rolled-up`
to the base; a hand decision in tags/title-decisions.tsv makes it `decided` (or `excluded`, soc "-", when posting usage of
the title does not match any O*NET occupation that lists it); anything else is `ambiguous` (all
candidates kept, none chosen, and postings with that title are counted but not assigned). Exact match only: no model, no fuzzy
matching. Run:  python3 -I scripts/make_title_map.py
"""
import csv
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "cluster"))
from title_norm import norm_title  # noqa: E402

SRC = ROOT / "source/onet-31.0"


def sing(title):
    """Singular of a title's last word: Nurses -> Nurse, Secretaries -> Secretary, Analysts -> Analyst."""
    w = title.strip().split()
    if not w:
        return title
    last = w[-1]
    if re.search(r"ies$", last, re.I):
        last = last[:-3] + "y"
    elif re.search(r"[^s]s$", last, re.I):
        last = last[:-1]
    return " ".join(w[:-1] + [last])


def tsv(name):
    return csv.DictReader(open(SRC / name, encoding="utf-8", errors="replace"), delimiter="\t")


def main():
    socs, sources = defaultdict(set), defaultdict(set)
    rated = {r["O*NET-SOC Code"] for r in tsv("Task Ratings.txt")}
    for r in tsv("Occupation Data.txt"):
        k = norm_title(r["Title"])
        if k:
            socs[k].add(r["O*NET-SOC Code"]); sources[k].add("occupation")
    # O*NET names occupations in the plural ("Data Scientists"); postings use the singular. Add singular forms of each
    # occupation title and of its first conjunct ("Radiologic Technologists and Technicians" -> "radiologic technologist"),
    # only where no other O*NET title already claims that form.
    singular = {}
    for r in tsv("Occupation Data.txt"):
        title = r["Title"]
        for form in {title, re.split(r",| and ", title)[0]}:
            k = norm_title(sing(form))
            if k and k not in socs:
                singular.setdefault(k, set()).add(r["O*NET-SOC Code"])
    for r in tsv("Job Titles.txt"):
        for col in ("Job Title", "Short Title"):
            k = norm_title(r.get(col) or "")
            if k and r.get(col) != "n/a":
                socs[k].add(r["O*NET-SOC Code"]); sources[k].add("job-titles")
    for r in tsv("Sample of Reported Titles.txt"):
        k = norm_title(r["Reported Job Title"])
        if k:
            socs[k].add(r["O*NET-SOC Code"]); sources[k].add("reported")
    for k, v in singular.items():
        if k not in socs:
            socs[k] |= v; sources[k].add("occupation-singular")
    decisions = {r["title_norm"]: r for r in csv.DictReader(open(ROOT / "tags/title-decisions.tsv"), delimiter="\t")}
    out = ROOT / "data/title-map.tsv"
    out.parent.mkdir(exist_ok=True)
    n_unique = n_amb = 0
    with open(out, "w", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["title_norm", "status", "soc", "candidates", "sources"])
        for k in sorted(set(socs) | set(decisions)):
            s = sorted(socs.get(k, ()))
            bases = {x[:7] for x in s}
            if k in decisions and decisions[k]["soc"] == "-":
                status, soc = "excluded", ""
            elif k in decisions:
                status, soc = "decided", decisions[k]["soc"]
            elif len(s) == 1:
                status, soc = "unique", s[0]
            elif len(bases) == 1 and bases.pop() + ".00" in s:
                status, soc = "rolled-up", s[0][:7] + ".00"     # 29-1141.00 + 29-1141.03 -> the base occupation
            else:
                status, soc = "ambiguous", ""
            n_unique += status not in ("ambiguous", "excluded")
            n_amb += status == "ambiguous"
            w.writerow([k, status, soc, " ".join(s), " ".join(sorted(sources.get(k, {"decision"})))])
    covered = {s for k, v in socs.items() if len(v) == 1 for s in v}
    print(f"{len(socs)} normalised titles: {n_unique} resolve to one occupation (unique, rolled-up or decided), {n_amb} ambiguous; "
          f"{len(covered)} occupations reachable by a unique title ({len(covered & rated)} of {len(rated)} rated)")


if __name__ == "__main__":
    main()
