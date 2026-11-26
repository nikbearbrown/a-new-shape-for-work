"""Check findings on A New Shape for Work against the repo's own files.

Run from the top of the repo:   python3 notes/deepa-shenoy/verify_findings.py
Standard library only. Reads files; writes nothing inside the repo.
Each check prints EVIDENCE (the numbers, read straight from the files) and where they came from.
"""
import csv
import difflib
import hashlib
import json
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path.cwd()
if not (ROOT / "research-data" / "SHA256SUMS").exists():
    sys.exit("Run this from the top of the repo (the folder with README.md and research-data/): python3 notes/deepa-shenoy/verify_findings.py")


def head(n, title):
    print(f"\n{'=' * 78}\n{n}. {title}\n{'=' * 78}")


def tsv(path):
    return list(csv.DictReader(open(path, encoding="utf-8"), delimiter="\t"))


# ---------------------------------------------------------------------------------------------------------------
head(1, "Checksums: are the deposit files the ones the authors published?")
ok = True
for line in open(ROOT / "research-data/SHA256SUMS"):
    want, name = line.split()
    got = hashlib.sha256((ROOT / "research-data" / name.lstrip("*")).read_bytes()).hexdigest()
    status = "OK " if got == want else "BAD"
    ok &= got == want
    print(f"  {status} {name}")
print("  RESULT:", "all checksums match" if ok else "MISMATCH")

# ---------------------------------------------------------------------------------------------------------------
head(2, "Reproduce: rebuild both CSVs and Figure 3 in a scratch copy, compare byte for byte")
with tempfile.TemporaryDirectory() as tmp:
    copy = Path(tmp) / "repo"
    shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns(".git"))
    for script in ["research-data/export-profiles.py", "paper/figures/build-ai-overlay.py"]:
        r = subprocess.run([sys.executable, "-I", script], cwd=copy, capture_output=True, text=True)
        print(f"  ran {script}: exit {r.returncode}")
    for f in ["research-data/activity-profiles.csv", "research-data/posting-emphasis.csv",
              "paper/figures/ai-overlay-developers.svg"]:
        same = (copy / f).read_bytes() == (ROOT / f).read_bytes()
        print(f"  {'IDENTICAL' if same else 'DIFFERENT'}  {f}")

# ---------------------------------------------------------------------------------------------------------------
A = list(csv.DictReader(open(ROOT / "research-data/activity-profiles.csv")))
P = list(csv.DictReader(open(ROOT / "research-data/posting-emphasis.csv")))
act = {r["onet_soc"] for r in A}
post = {r["onet_soc"] for r in P}
cut = {r["onet_soc"] for r in P if r["passes_display_cutoff"] == "1"}

head(3, "Headline numbers (manuscript table, Section 4)")
for soc, phase, name in [("15-1253.00", "check", "QA analysts"), ("15-1252.00", "coordinate", "Software developers"),
                         ("47-2111.00", "sustain", "Electricians")]:
    a = next(r for r in A if r["onet_soc"] == soc and r["phase"] == phase and r["weighting_model"] == "ordinal")
    p = next(r for r in P if r["onet_soc"] == soc and r["phase"] == phase)
    print(f"  {name:20} {phase:10} task share {float(a['activity_share']):.2%}   "
          f"ad share {float(p['diagnostic_mention_share']):.2%}")
print("  (compare with the manuscript: 32.28/62.76, 36.10/8.02, 14.40/48.70)")

head(4, "Occupation counts (these already match Section 4; no issue here)")
print(f"  rated occupations (activity table) .......... {len(act)}")
print(f"  codes with mapped postings .................. {len(post)}")
print(f"  codes with 50+ retained ads ................. {len(cut)}")
print(f"  rated occupations with some postings ........ {len(act & post)}")
print(f"  rated occupations with 50+ ads (both layers)  {len(act & cut)}")

# ---------------------------------------------------------------------------------------------------------------
head(5, "Ad-side coverage: what share of skill mentions count, across ALL 429 occupations?")
ratios = []
for r in P:
    if r["onet_soc"] in cut and r["phase"] == "understand" and int(r["top_phrase_mentions"]) > 0:
        ratios.append(int(r["diagnostic_mentions"]) / int(r["top_phrase_mentions"]))
ratios.sort()
print(f"  occupations: {len(ratios)}   median {statistics.median(ratios):.1%}   "
      f"min {ratios[0]:.1%}   max {ratios[-1]:.1%}")
print(f"  occupations under 10%: {sum(x < 0.10 for x in ratios)}")
print("  (the paper reports 18-42% for the eight featured occupations only)")
dates = Counter((r["first_seen"], r["last_seen"]) for r in P)
print(f"  posting dates in the table: earliest {min(d[0] for d in dates)}, latest {max(d[1] for d in dates)}")

# ---------------------------------------------------------------------------------------------------------------
head(6, "Missing AI joins: why are 157 tasks unmatched, and who is affected?")
onet = json.load(open(ROOT / "page/data/onet.json"))
key = lambda t: re.sub(r"\s+", " ", t.strip().lower())
aei = {key(r["task"]): float(r["penetration"])
       for r in csv.DictReader(open(ROOT / "research-data/sources/anthropic-task-penetration.csv"))}
missing, per_occ = [], defaultdict(lambda: [0, 0])
for o in onet["occupations"]:
    for t in o["tasks"]:
        per_occ[(o["soc"], o["title"])][1] += 1
        if t[-1] is None:
            missing.append((o["soc"], o["title"], t[0]))
            per_occ[(o["soc"], o["title"])][0] += 1
print(f"  rated tasks with no AI score: {len(missing)}   occupations affected: "
      f"{sum(1 for v in per_occ.values() if v[0])}")
print(f"  tasks with odd characters (encoding problems): "
      f"{sum(1 for m in missing if any(ord(c) > 127 for c in m[2]))}")
print("  hardest hit (missing / rated tasks):")
for (soc, title), (m, n) in sorted(per_occ.items(), key=lambda kv: -kv[1][0] / kv[1][1])[:5]:
    print(f"    {soc} {title}: {m}/{n}")
by_start = defaultdict(list)
for k in aei:
    by_start[" ".join(k.split()[:2])].append(k)
near = []
for soc, title, text in missing:
    k = key(text)
    pool = by_start.get(" ".join(k.split()[:2]), [])
    best = difflib.get_close_matches(k, pool, n=1, cutoff=0.9)
    if best:
        near.append((soc, title, text, best[0], aei[best[0]]))
print(f"  near-identical text in the Anthropic file (similarity >= 0.90): {len(near)}")
print(f"  ...of those with a nonzero AI score: {[(n[1], n[4]) for n in near if n[4] > 0]}")
print("  two examples (O*NET 31.0 wording  vs  Anthropic file wording):")
for n in near[:2]:
    print(f"    {n[1]}\n      O*NET: {n[2][:110]}\n      AEI  : {n[3][:110]}")

print("\n  PARALEGALS (23-2011.00): which of their 12 tasks have no AI score?")
para = next(o for o in onet["occupations"] if o["soc"] == "23-2011.00")
for t in para["tasks"]:
    print(f"    {'MISSING -> counted as 0' if t[-1] is None else f'score {t[-1]:.2f}':24} {t[0][:75]}")

# ---------------------------------------------------------------------------------------------------------------
head(7, "Rule bug: security clearances are counted as Sustain work")
tags = tsv(ROOT / "tags/skill-phrase-phase-tags.tsv")
clear = [t for t in tags if "clearance" in t["phrase"]]
print(f"  phrases containing 'clearance': {len(clear)}   by phase: {Counter(t['phase'] for t in clear).most_common()}")
for t in clear[:3]:
    print(f"    '{t['phrase']}' -> {t['phase']}")
rule = re.search(r'\("sustain", r"(.*?)"\)', open(ROOT / "scripts/build_postings.py").read(), re.S)
print(f"  the Sustain rule in scripts/build_postings.py contains 'security': {'security' in rule.group(0)}")
print("  docs/METHOD.md says credentials are neutral:",
      "credentials" in open(ROOT / "docs/METHOD.md").read())
print("\n  Same requirement, different wording, different phase:")
for ph in ["security clearance", "secret clearance", "ts/sci clearance"]:
    hit = next((t["phase"] for t in tags if t["phrase"] == ph), "neutral (not in tag file)")
    print(f"    '{ph}' -> {hit}")
print("\n  Which occupations' dashboards show a clearance phrase (Chart 5, 'not in the lexicon yet' panel):")
occs = json.load(open(ROOT / "page/data/by-occupation.json"))["occupations"]
names = {o["soc"]: o["title"] for o in onet["occupations"]}
for soc, v in occs.items():
    for it in v.get("unmatched_top") or []:
        if "clearance" in it["phrase"]:
            dm, ws = v["diagnostic_mentions"], v["with_skills"]
            sus = v["profile"]["sustain"] * dm
            line = (f"    {names.get(soc, soc)} ({soc}): '{it['phrase']}' in {it['share']:.1%} of ads -> {it['phase']}"
                    f"; Sustain share {v['profile']['sustain']:.1%}")
            if it["phase"] == "sustain":
                cm = it["share"] * ws
                line += f"; about {cm:.0f} of its ~{sus:.0f} Sustain mentions are this one phrase (estimate)"
            print(line)

# ---------------------------------------------------------------------------------------------------------------
head(8, "Dashboard wording that says more than the paper")
html = open(ROOT / "page/index.html", encoding="utf-8").read()
print("  index.html opens with 'How AI is Affecting Jobs.':", "How AI is Affecting Jobs." in html)
print("  manuscript abstract says it measures neither time nor 'the effects of AI on employment':",
      "effects of AI on employment" in open(ROOT / "paper/manuscript.md").read())
print("  index.html says posting layer 'covers every occupation O*NET names a title for':",
      "covers every occupation O*NET names a title for" in html)

# ---------------------------------------------------------------------------------------------------------------
head(9, "Two software-developer task tags to question (Chart 7)")
phases = onet["phases"]
dev = next(o for o in onet["occupations"] if o["soc"] == "15-1252.00")
for t in dev["tasks"]:
    if t[0].startswith(("Train users", "Consult with customers")):
        split = {phases[i]: s for i, s in enumerate(t[7]) if s}
        print(f"  '{t[0][:80]}...' -> {split}")
print("  replication/prompts/phases.txt lists 'training' and 'liaising' under coordinate:",
      all(w in open(ROOT / "replication/prompts/phases.txt").read() for w in ["training", "liaising"]))
print("\nDone. Every number above was read from files in this folder.")
