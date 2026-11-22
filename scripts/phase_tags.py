"""Draft phase tags for O*NET work activities -> tags/iwa-phase-tags.tsv.

Six universal phases: understand, plan, produce, check, sustain, coordinate.
Software names for the first five: specify, design, build, verify, operate.

Tags are drafts: one person-in-the-loop judgment per line, status "draft", reviewed_by empty.
basis = paste-mapping   the GWA -> phase mapping in the Job Shape brief, applied to every IWA under it
        gwa-default     a GWA the brief did not map; phase chosen here
        iwa-override    this IWA departs from its GWA's phase; the note says why
Every task inherits phases through Tasks to DWAs -> DWA -> IWA.
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "source/onet-31.0"

PASTE = {  # from the brief, Part 1
    "4.A.1.a.1": "understand",   # Getting Information
    "4.A.1.b.1": "understand",   # Identifying Objects, Actions, and Events
    "4.A.2.b.4": "plan",         # Developing Objectives and Strategies
    "4.A.2.b.6": "plan",         # Organizing, Planning, and Prioritizing Work
    "4.A.2.b.2": "plan",         # Thinking Creatively
    "4.A.3.b.2": "plan",         # Drafting, Laying Out, and Specifying Technical Devices
    "4.A.3.b.1": "produce",      # Working with Computers
    "4.A.3.a.2": "produce",      # Handling and Moving Objects
    "4.A.3.b.6": "produce",      # Documenting/Recording Information
    "4.A.2.a.3": "check",        # Evaluating Information to Determine Compliance with Standards
    "4.A.2.a.1": "check",        # Judging the Qualities of Objects, Services, or People
    "4.A.1.b.2": "check",        # Inspecting Equipment, Structures, or Materials
    "4.A.1.a.2": "sustain",      # Monitoring Processes, Materials, or Surroundings
    "4.A.3.a.3": "sustain",      # Controlling Machines and Processes (overridden below: operating IS producing)
    "4.A.3.b.4": "sustain",      # Repairing and Maintaining Mechanical Equipment
    "4.A.3.b.5": "sustain",      # Repairing and Maintaining Electronic Equipment
    "4.A.4.a.2": "coordinate",   # Communicating with Supervisors, Peers, or Subordinates
    "4.A.4.b.1": "coordinate",   # Coordinating the Work and Activities of Others
}
GWA_DEFAULT = {  # GWAs the brief left out
    "4.A.1.b.3": ("check", "estimating quantities is mostly measuring"),
    "4.A.2.a.2": ("produce", "processing information is clerical output"),
    "4.A.2.a.4": ("understand", "analysis informs a decision; CONTESTED: for analyst jobs the analysis is the product"),
    "4.A.2.b.1": ("plan", "deciding how and with what is planning"),
    "4.A.2.b.3": ("understand", "keeping knowledge current"),
    "4.A.2.b.5": ("plan", "scheduling"),
    "4.A.3.a.1": ("produce", "general physical work"),
    "4.A.3.a.4": ("produce", "driving is the work"),
    "4.A.4.a.1": ("produce", "explaining to clients is service output"),
    "4.A.4.a.3": ("produce", "serving the public is service output"),
    "4.A.4.a.4": ("coordinate", "relationships"),
    "4.A.4.a.5": ("produce", "care is the work output"),
    "4.A.4.a.6": ("produce", "selling is the work output"),
    "4.A.4.a.7": ("coordinate", "negotiation and conflict"),
    "4.A.4.a.8": ("produce", "direct public service"),
    "4.A.4.b.2": ("coordinate", "team building"),
    "4.A.4.b.3": ("produce", "teaching is the work output for teachers; work-procedure training overridden to coordinate"),
    "4.A.4.b.4": ("coordinate", "directing others' work"),
    "4.A.4.b.5": ("coordinate", "coaching"),
    "4.A.4.b.6": ("produce", "advice is the service output"),
    "4.A.4.c.1": ("produce", "administrative output"),
    "4.A.4.c.2": ("coordinate", "staffing"),
    "4.A.4.c.3": ("sustain", "keeping resources stocked"),
}
OVERRIDE = {  # IWA suffix under its GWA -> (phase, why)
    "4.A.1.a.2.c": ("check", "monitoring financial data is auditing"),
    "4.A.1.a.2.f": ("check", "monitoring behaviour or performance is judging it"),
    "4.A.1.a.2.h": ("understand", "watching outside trends is information gathering"),
    "4.A.1.a.2.k": ("check", "compliance monitoring"),
    "4.A.1.b.1.a": ("produce", "marking objects is handling work"),
    "4.A.1.b.2.a": ("understand", "diagnostic tests on patients gather information for a diagnosis"),
    "4.A.1.b.2.i": ("understand", "examining patients is assessment"),
    "4.A.1.b.3.b": ("plan", "cost estimates are planning"),
    "4.A.1.b.3.c": ("produce", "calculating financial data is accounting output"),
    "4.A.1.b.3.e": ("understand", "patient measurements are assessment"),
    "4.A.2.a.1.a": ("understand", "needs assessment"),
    "4.A.2.a.1.f": ("understand", "evaluating a patient's condition is assessment"),
    "4.A.2.a.1.j": ("plan", "feasibility is a planning judgment"),
    "4.A.2.a.2.a": ("check", "data quality"),
    "4.A.2.a.2.d": ("check", "reconciliation"),
    "4.A.2.a.2.e": ("check", "verification"),
    "4.A.2.a.4.e": ("check", "reviewing designs and specifications"),
    "4.A.2.a.4.l": ("sustain", "system performance analysis is operations"),
    "4.A.2.b.1.b": ("sustain", "diagnosing equipment problems"),
    "4.A.2.b.1.c": ("check", "authorising is approval"),
    "4.A.2.b.1.e": ("produce", "legal decisions are a judge's output"),
    "4.A.2.b.1.f": ("understand", "diagnosis"),
    "4.A.2.b.1.g": ("check", "editing reviews text"),
    "4.A.2.b.1.i": ("produce", "carrying out procedures"),
    "4.A.2.b.1.k": ("produce", "editing media is production"),
    "4.A.2.b.2.j": ("produce", "marketing materials are made, not planned"),
    "4.A.2.b.2.o": ("produce", "visual designs are a designer's output"),
    "4.A.2.b.2.r": ("produce", "content creation"),
    "4.A.2.b.2.t": ("produce", "artistic work"),
    "4.A.2.b.2.u": ("produce", "theories and models are research output"),
    "4.A.2.b.5.c": ("coordinate", "booking appointments for others"),
    "4.A.3.a.1.b": ("sustain", "protecting people or property"),
    "4.A.3.a.1.c": ("sustain", "cleaning tools and work areas is upkeep"),
    "4.A.3.a.1.e": ("sustain", "waste disposal is upkeep"),
    "4.A.3.a.1.i": ("sustain", "cleaning medical equipment is upkeep"),
    "4.A.3.a.1.k": ("sustain", "safety and security"),
    "4.A.3.a.2.b": ("check", "sampling products is quality control"),
    "4.A.3.a.2.i": ("sustain", "adjusting equipment keeps it running"),
    "4.A.3.a.2.x": ("sustain", "adjusting medical equipment keeps it running"),
    "4.A.3.a.2.al": ("understand", "field samples feed research"),
    "4.A.3.a.2.au": ("check", "specimens for testing"),
    "4.A.3.a.3.a": ("produce", "operating equipment is the work output, not upkeep"),
    "4.A.3.a.3.b": ("produce", "operating equipment is the work output, not upkeep"),
    "4.A.3.a.3.c": ("produce", "operating equipment is the work output, not upkeep"),
    "4.A.3.a.3.d": ("produce", "operating equipment is the work output, not upkeep"),
    "4.A.3.a.3.e": ("produce", "operating equipment is the work output, not upkeep"),
    "4.A.3.a.3.f": ("produce", "operating equipment is the work output, not upkeep"),
    "4.A.3.a.3.g": ("produce", "operating equipment is the work output, not upkeep"),
    "4.A.3.a.3.h": ("produce", "operating equipment is the work output, not upkeep"),
    "4.A.3.a.3.i": ("produce", "operating equipment is the work output, not upkeep"),
    "4.A.3.a.3.j": ("produce", "operating equipment is the work output, not upkeep"),
    "4.A.3.a.3.k": ("produce", "operating equipment is the work output, not upkeep"),
    "4.A.3.a.3.l": ("produce", "operating equipment is the work output, not upkeep"),
    "4.A.3.b.1.b": ("sustain", "security measures are operations"),
    "4.A.3.b.1.d": ("sustain", "resolving computer problems is operations"),
    "4.A.4.a.2.j": ("understand", "conferring with clients on needs is requirements gathering (software: specify)"),
    "4.A.4.b.3.c": ("coordinate", "teaching safety procedures to co-workers"),
    "4.A.4.b.3.d": ("coordinate", "training others on work procedures"),
    "4.A.4.c.1.a": ("sustain", "clerical overhead keeps operations running"),
    "4.A.4.c.3.b": ("understand", "ordering tests gathers information"),
    "4.A.4.c.3.d": ("produce", "collecting payments is the work output"),
    "4.A.4.c.3.f": ("produce", "prescribing is treatment"),
}
CONTESTED_GWA = {"4.A.2.a.4", "4.A.3.b.6", "4.A.4.b.6", "4.A.4.a.1"}


def main():
    cm = {r["Element ID"]: r["Element Name"] for r in csv.DictReader(open(SRC / "Content Model Reference.txt"), delimiter="\t")}
    out = ROOT / "tags/iwa-phase-tags.tsv"
    out.parent.mkdir(exist_ok=True)
    rows = list(csv.DictReader(open(SRC / "GWAs to IWAs.txt"), delimiter="\t"))
    with open(out, "w", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["iwa_id", "iwa_name", "gwa_id", "gwa_name", "phase", "basis", "note", "contested", "status", "reviewed_by"])
        for r in rows:
            g, i = r["GWA Element ID"], r["IWA Element ID"]
            if i in OVERRIDE:
                ph, basis, note = *OVERRIDE[i], None
                note = OVERRIDE[i][1]
                basis = "iwa-override"
            elif g in PASTE:
                ph, basis, note = PASTE[g], "paste-mapping", ""
            else:
                ph, note = GWA_DEFAULT[g]
                basis = "gwa-default"
            w.writerow([i, r["IWA Element Name"], g, cm[g], ph, basis, note, "yes" if g in CONTESTED_GWA else "",
                        "draft", ""])
    print("wrote", out, len(rows))


if __name__ == "__main__":
    main()
