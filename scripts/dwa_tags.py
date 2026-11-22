"""Draft phase tags at the DWA level (2,087 Detailed Work Activities) -> tags/dwa-phase-tags.tsv.

Order of precedence (first that fires wins), each row records which one:
  manual     a hand decision for one DWA (MANUAL below), with the reason
  patient    assessing a patient or client's condition or needs is Understand (diagnosis), whatever the verb
  verb       the DWA's leading verb names the phase unambiguously (STRONG below)
  object     an ambiguous verb (Develop, Conduct, Perform, Analyze, ...) resolved by what it acts on
  iwa        otherwise the DWA inherits its IWA's tag from tags/iwa-phase-tags.tsv
All rows are drafts (status "draft", reviewed_by empty).
"""
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "source/onet-31.0"

STRONG = {
    "check": "Inspect Test Verify Review Check Audit Weigh Appraise Proofread Measure Grade Calibrate",
    "sustain": "Monitor Maintain Repair Clean Adjust Service Troubleshoot Patrol Enforce Stock Dispose Replace Protect Lubricate "
               "Replenish Sterilize Guard",
    "plan": "Plan Schedule Design Estimate Select Forecast Budget",
    "understand": "Research Investigate Interview Gather Study Diagnose Survey Observe Search",
    "produce": "Operate Install Assemble Create Write Build Construct Fabricate Cut Administer Treat Teach Sell Program Enter "
               "Drive Load Package Mix Shape Trim Smooth Drill Lay Serve Cultivate Record Document Modify Paint Cook Weld "
               "Sew Code Compose Perform",
    "coordinate": "Coordinate Supervise Collaborate Confer Communicate Discuss Negotiate Assign Encourage Signal Notify Direct "
                  "Manage Delegate Recruit Hire Mentor Liaise",
}
VERB = {v: ph for ph, vs in STRONG.items() for v in vs.split()}
OBJECT = [  # (regex on the full DWA name, phase) for verbs that are not in VERB; first match wins
    (r"\btest(s|ing)?\b|\bquality\b|\baudits?\b|\binspection|\bcompliance\b|\baccuracy\b", "check"),
    (r"technical support|\bmaintenance\b|\brepairs?\b|troubleshoot|\bsecurity\b", "sustain"),
    (r"\b(requirements|needs)\b", "understand"),
    (r"\b(research|surveys?|studies|interviews?|investigations?)\b", "understand"),
    (r"\b(plans?|polic(y|ies)|strateg(y|ies)|procedures|standards|specifications|budgets?|schedules?|goals|objectives|"
     r"guidelines|curricul\w*|metrics)\b", "plan"),
    (r"\b(software|computer programs?|code|applications|content|materials|presentations|artwork|products?|prototypes?|"
     r"reports?|documents?|documentation)\b", "produce"),
]
PATIENT = re.compile(r"^(Assess|Evaluate|Examine|Analyze|Collect|Gather|Interview|Measure|Test)\b.*\b(patients?|clients?|"
                     r"individuals?|residents?|students?)\b.*\b(condition|health|needs|status|symptoms|functioning|history|"
                     r"capabilities|abilities)", re.I)
MANUAL = {  # DWA id -> (phase, why). Filled from the featured-occupation review in review-dwa.txt
}


def main():
    iwa = {r["iwa_id"]: r for r in csv.DictReader(open(ROOT / "tags/iwa-phase-tags.tsv"), delimiter="\t")}
    rows = list(csv.DictReader(open(SRC / "GWAs to IWAs to DWAs.txt"), delimiter="\t"))
    out = ROOT / "tags/dwa-phase-tags.tsv"
    changed = 0
    with open(out, "w", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["dwa_id", "dwa_name", "iwa_id", "iwa_phase", "phase", "basis", "note", "status", "reviewed_by"])
        for r in rows:
            d, name, i = r["DWA Element ID"], r["DWA Element Name"], r["IWA Element ID"]
            iph = iwa[i]["phase"]
            verb = name.split()[0]
            if d in MANUAL:
                ph, basis, note = MANUAL[d][0], "manual", MANUAL[d][1]
            elif PATIENT.search(name):
                ph, basis, note = "understand", "patient", "assessing a person's condition or needs"
            elif verb in VERB:
                ph, basis, note = VERB[verb], "verb", verb
            else:
                hit = next(((p, rx) for rx, p in OBJECT if re.search(rx, name, re.I)), None)
                if hit:
                    ph, basis, note = hit[0], "object", hit[1][:40]
                else:
                    ph, basis, note = iph, "iwa", iwa[i]["basis"]
            changed += ph != iph
            w.writerow([d, name, i, iph, ph, basis, note, "draft", ""])
    print("wrote", out, len(rows), "rows;", changed, "differ from their IWA tag")


if __name__ == "__main__":
    main()
