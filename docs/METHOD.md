# Method

How the prototype turns O*NET ratings, job postings and AI-use data into a job's shape, and where each step is weak. The design brief behind it is [job-shape-brief.md](job-shape-brief.md).

## Three layers, kept apart

| Layer | Question | Source | Unit |
|---|---|---|---|
| Activity | What does the work consist of, and how often? | O*NET 31.0 task statements and ratings | estimated share of effort |
| Emphasis | What do employers ask for? | job postings (LinkedIn Jan 2024; Google Jobs 2022–2025 for data analysts) | share of phase-diagnostic skill mentions |
| AI overlay | Which of the work do people already bring to AI? | Anthropic Economic Index task coverage | share of estimated effort in covered tasks |

The charts never add these together. The interesting result is usually the gap between them.

## Six phases

| Phase | Software name | Examples of O*NET work activities |
|---|---|---|
| Understand | specify | Getting Information; diagnosis; conferring with clients on needs |
| Plan | design | Thinking Creatively; Organizing, Planning, and Prioritizing; Drafting and Specifying |
| Produce | build | Working with Computers; Handling and Moving Objects; Documenting; operating equipment; care and service delivery |
| Check | verify | Evaluating Compliance; Judging Qualities; Inspecting; testing |
| Sustain | operate | Monitoring; Repairing and Maintaining; security; upkeep |
| Coordinate | cross-cutting | Communicating with Supervisors and Peers; Coordinating; supervising; staffing |

Tags are set at three levels, each recorded with its basis:

1. **GWA** (41 generalized work activities): the brief's mapping where it gave one (`paste-mapping`), a default chosen here otherwise (`gwa-default`). One departure from the brief: Controlling Machines and Processes is Produce, because operating equipment is the work output for operators.
2. **IWA** (332 intermediate work activities): overrides where an IWA clearly sits in another phase, each with a reason (`tags/iwa-phase-tags.tsv`).
3. **DWA** (2,087 detailed work activities): the leading verb when it names a phase unambiguously (Inspect, Monitor, Plan, Research, Install, Supervise…), the object for ambiguous verbs (Develop testing routines → Check; Provide technical support → Sustain), patient and client assessment → Understand, otherwise the IWA tag (`tags/dwa-phase-tags.tsv`).

A task inherits phases from its DWAs, split equally.

**Contested:** "Analyzing Data or Information" is Understand. For data scientists and analysts the analysis is the product, so this one choice sends half their profile to Understand. Documenting and Advising are contested in the same way.

## Effort models

For each task, O*NET gives a frequency distribution over seven categories (yearly or less … hourly or more), importance (1–5) and relevance (share of incumbents who say the task is part of the job). Weight = frequency term × importance × relevance:

- **Ordinal** (main): the mean category number, 1–7. Categories are roughly log-spaced, so a daily task counts about twice a monthly one.
- **Occurrence**: times per year (1, 4, 24, 100, 250, 750, 2000). Treats every occurrence as equally long, so hourly micro-tasks dominate.
- **Flat**: ignores frequency.

None of these is time. Converting ordinal categories to hours is an assumption, which is why every effort chart carries "Estimated".

**Calibration.** Software developers are the one occupation with outside time-use data (hands-on coding at about 15–30% of time, per the brief). Produce comes out at 16% (ordinal), 22% (occurrence) and 16% (flat). That is in range, but 7 of the 17 tasks are conferring, supervising or reporting, so the pass is weak evidence.

**A cross-check that failed.** O*NET's work-activity importance ratings, mapped the same way, give nearly the same profile for every occupation (about 13/17/29/11/9/20). Only the task layer separates jobs, so the activity ratings are not charted.

## Posting emphasis

A posting's skill list (the dataset's own model-extracted `job_skills`) is split into phrases. A phrase is phase-diagnostic only if one of the draft rules in `scripts/build_postings.py` fires (testing, code review → Check; troubleshooting, maintenance → Sustain; requirements, research → Understand; design, planning → Plan; leadership, supervision → Coordinate; development, patient care, wiring → Produce). Tools, languages, soft skills, credentials and benefits boilerplate are neutral. Emphasis is each phase's share of diagnostic mentions. In the every-title run, 18–42% of mentions qualify for the eight featured occupations (over each occupation's 400 most common phrases), and each chart prints the share.

Postings are deduplicated twice: same company, title and location; then the same summary text within an occupation (agency reposts: 21% of postings that survived the first step, 26% for software developers).

**Level** comes from title words: Junior, Associate, Apprentice, I → entry; II, Journeyman → mid; Senior, III → senior; Lead, Principal, (tech) Staff → lead. "Staff Accountant" is entry. Most nurse postings name no level.

**Experience** is the first "N years … experience" phrase in the posting text.

## AI overlay

The Economic Index file gives one value per O*NET task statement. It is 0 for most tasks. It is positive when a task is judged LLM-feasible (Eloundou et al.) and shows enough work-related Claude use in the August and November 2025 samples, with automated use weighted fully and augmentative use at half. It joins to 18,680 of 18,838 O*NET 31.0 task statements on lower-cased text.

Covered effort for a phase = Σ task weight × phase share × coverage. The paper behind the file weights tasks by time share to get "observed exposure"; this page uses its own effort model, so its totals are not the paper's numbers.

## Where it breaks

- **Mention isn't time.** Postings measure what is written down, not where the hours go.
- **Coarse task lists.** Information security analysts have 11 rated tasks; one tag decides a fifth of the profile.
- **Model-extracted skills.** The LinkedIn skill lists reflect the extraction model's vocabulary as much as the employer's.
- **One snapshot.** Change over time exists only for data analysts.
- **Lexicon gaps.** 15–50% of skill mentions matched a lexicon entry for the eight featured occupations. Git, Kubernetes, Jenkins, nursing and patient care have none; "Linux" resolves to "Linux systems administration".
- **Title ambiguity.** "Data Analyst" is a listed title for eight occupations. Matching assigned 35% of US postings to an occupation; leading- and trailing-word matches are the least certain.
- **Observed use, not capability.** The AI overlay says where Claude use shows up, not what AI could do or what jobs will change.
