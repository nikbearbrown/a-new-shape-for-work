<!-- The design brief the prototype was built from, as pasted on 2026-11-21. Figures in it describe the Skills Lexicon as it stood then. -->

# Job Shape: Charting What a Job Asks For and Where the Effort Goes

*Suggested graphics and a feasibility assessment for per-title profiles built on Skills Lexicon, O*NET, and job postings.*

## The core problem

Yes, this can be built. But not as specified, because job postings can't tell you where effort goes. A posting tells you what an employer screens for. When a posting mentions Kubernetes, that's evidence someone thought Kubernetes worth writing down. It says nothing about whether the hire spends 2% or 40% of their week on it. Postings are also inflated with boilerplate, subject to experience creep, and lag the actual work by years.

So the honest version separates three things that the request runs together:

| Layer | What it measures | Source | Status in hand |
|---|---|---|---|
| **Emphasis** | What employers ask for | Job postings | Partial: extractor pilot, occurrence evidence, no representative corpus |
| **Requirement** | What the occupation needs, rated by analysts and job holders | O*NET skills, knowledge, abilities | Have it: 894 rated occupations |
| **Activity** | What the work consists of and how often | O*NET tasks with frequency and importance ratings, work activities | Not yet imported, but in the same O*NET archive |

An "effort profile" is a *model* built mainly from the activity layer, with emphasis shifts layered on top. Every chart that shows effort should say "estimated" on it. The most interesting chart may be the gap between layers, such as employers screening for Build skills while the occupation's tasks are mostly Verify.

There's a second problem. The five software phases don't generalize. A nurse, an accountant, or an electrician doesn't have a Build or Deploy phase in any meaningful sense. "For every job title" requires a universal phase frame, with the software modes as one specialization.

---

## Part 1: A phase frame that works for every job

O*NET's Generalized Work Activities (41 activities in four categories: Information Input, Mental Processes, Work Output, Interacting with Others) are the natural backbone. They're already rated for importance and level per occupation. A proposed mapping onto six universal phases:

| Universal phase | Software specialization | Example O*NET work activities |
|---|---|---|
| **Understand** | Specify | Getting Information; Identifying Objects, Actions, and Events |
| **Plan** | Design | Developing Objectives and Strategies; Organizing, Planning, and Prioritizing Work; Thinking Creatively; Drafting and Specifying Technical Devices |
| **Produce** | Build | Working with Computers; Handling and Moving Objects; Documenting/Recording Information |
| **Check** | Verify | Evaluating Information to Determine Compliance with Standards; Judging the Qualities of Things, Services, or People; Inspecting Equipment, Structures, or Material |
| **Sustain** | Operate | Monitoring Processes, Materials, or Surroundings; Controlling Machines and Processes; Repairing and Maintaining Equipment |
| **Coordinate** | (cross-cutting) | Communicating with Supervisors, Peers, or Subordinates; Coordinating the Work and Activities of Others |

Coordinate gets its own phase because for many jobs, it's the largest one, and hiding it inside the others makes every profile look more hands-on than it is.

This mapping is a proposal. It needs to be stored the same way Skills Lexicon stores claims: as a tagged assertion with evidence and review status, not as a hard-coded lookup. Tag at the Detailed Work Activity level (roughly 2,000 DWAs), and every occupation's task list inherits the tags.

---

## Part 2: Suggested graphics

Every chart below should carry a provenance strip: number of postings, date range, extraction coverage, share of mentions that were phase-diagnostic, and review status. Skills Lexicon currently has zero reviewed entries. That should be visible on the chart, not buried in a README.

### 1. The phase profile (the generalized five-mode chart)

**Question:** Where does this job's work sit across phases?

**Encoding:** One bar per phase, in fixed order, for one title. Show two series side by side: the O*NET activity-based estimate and the posting emphasis. A smoothed silhouette can sit behind the bars for the "curve" look, but the bars carry the data.

**Why two series:** The gap between them is the insight. If postings for QA analysts emphasize Produce skills while O*NET tasks are mostly Check, employers are screening for the wrong thing, or the occupation is changing faster than O*NET.

### 2. The phase shift (dumbbell chart)

**Question:** How has emphasis moved over time?

**Encoding:** One row per phase, with a dot for the earliest period and a dot for the latest, connected by a line. Use small multiples to compare titles.

This is the chart that would show code review in entry-level software postings doubling between 2020 and 2025, phase by phase.

### 3. The seniority ladder (100% stacked bars)

**Question:** How does the work change as people move up?

**Encoding:** One stacked bar per seniority level within a title family (entry, mid, senior, staff), with segments for phases.

This directly tests the pyramid hypothesis from the junior-developer discussion: a Produce-heavy entry level and Plan/Check-heavy senior levels, with the entry-level bar shifting over time. It requires postings, because O*NET occupations don't carry seniority. Seniority lives in titles.

### 4. Experience requirements (ridgeline plot)

**Question:** How much experience are "entry-level" roles actually demanding?

**Encoding:** One density ridge per year, showing the distribution of minimum required years for a title. Add one annotated number per ridge: the share of entry-level postings requiring two or more years.

This is the experience-creep chart. It's also one of the easiest to extract reliably, since "3+ years" is a regular pattern.

### 5. The requirement stack (grouped ranked bars)

**Question:** What does this job ask for, by type?

**Encoding:** Horizontal bars ranked by share of postings, in separate panels for skills, tools, knowledge, languages, and credentials. Color by phase where a concept is phase-diagnostic, and gray where it isn't. Split each bar into required and preferred. Add small arrows for rising and falling concepts.

This is where Skills Lexicon's class structure pays off. Keeping credentials and knowledge out of the skills ranking prevents degrees from crowding out actual capabilities.

### 6. Rank changes (bump chart)

**Question:** Which requirements are climbing or falling for this title?

**Encoding:** Top 15 to 20 concepts, ranked by posting share per period, with lines tracing each concept's rank.

This gives a quick read on churn: whether a title's requirements are stable or turning over.

### 7. The day-to-day (task frequency strip)

**Question:** What does the job actually involve, and how often?

**Encoding:** One row per O*NET task statement for the occupation. Rows are sorted into frequency bands (hourly, daily, weekly, monthly, yearly), sized by importance, and colored by phase.

This is the honest day-in-the-life chart. It shows rated frequency and importance without inventing hours. If you want a "week in the life" waffle chart in hours, it has to be labeled as a model. Converting ordinal frequency categories to hours is an assumption, not data.

### 8. The human/agent overlay (split bars)

**Question:** Within each phase, how much of the work is AI-exposed?

**Encoding:** Phase profile bars split into AI-exposed and not-exposed segments, aggregated from task-level exposure. Sources include the Anthropic Economic Index's O*NET task mappings and whatever exposure measures the Exposure Explorer already holds.

This is the two-layer chart from the effort-distribution doc, made per occupation.

### 9. The job family (small multiples)

**Question:** How do related titles divide up the work?

**Encoding:** Phase profiles for a family of titles side by side, on identical axes. For example: software developer, QA analyst, DevOps engineer, product manager, and data analyst.

This shows where effort concentrates across a family and which titles are absorbing the phases agents are vacating.

### The reverse view: concept pages

Every chart above is title-first, but the lexicon is concept-first. A concept page shows, for one concept such as code review:

- which titles ask for it
- at what seniority levels
- in which phase
- how that has changed over time

This turns the lexicon into a demand map.

### Charts to avoid

**Radar charts.** Area depends on axis order and exaggerates differences, and readers misjudge them.

**Smooth density curves drawn over categorical phases.** The troughs between bumps imply zero effort at handoffs, the same problem as the whiteboard.

**Word clouds.** Size encodes nothing reliably.

**Stacked areas with more than six categories.** They become unreadable.

---

## Part 3: Can it be built?

Yes. Here's what's in hand and what's missing, based on the repository's current state.

| Component | Status | Gap |
|---|---|---|
| Concept vocabulary | 3,754 concepts with variants and classes | 0 reviewed; classification flags open |
| O*NET skills, knowledge, abilities ratings | Imported for 894 occupations | None for this purpose |
| O*NET tasks, frequency ratings, work activities | Not imported | Same archive as the existing imports; straightforward to add |
| Phase tags | Don't exist | New claim type with evidence, tagged at the DWA level first |
| Extraction from postings | Pilot on 126 postings | Precision and recall unmeasured |
| Title → occupation mapping | Pilot script only | No committed dataset; seniority not preserved |
| Experience extraction | Doesn't exist | New, but pattern-friendly |
| Postings corpus | Occurrence evidence across 30 datasets; structural survey of archives | Not independent jobs; not deduplicated; not representative; dataset frequency isn't demand |
| AI exposure | Exposure Explorer data | Needs linking at the task level |

### Recommended build order

1. **O*NET-only profiles for every rated occupation.** Import task ratings and work activities, tag DWAs to phases, and generate charts 1, 7, and 8 for all 894 occupations. This needs no postings and covers "every job" at the occupation level. It fits naturally as a new page type in the AI Exposure Explorer.
2. **A posting pilot on five to ten titles.** Include at least one non-software occupation to stress-test the universal frame. Extract concepts, experience, and seniority. Hand-label a sample and measure precision and recall before showing any emphasis chart.
3. **Time series.** Add dated postings for charts 2, 4, and 6. O*NET's archived releases add a slower requirement-side time series, with the caveat that O*NET resurveys occupations on a rolling basis, so changes partly reflect resurvey timing.
4. **The seniority ladder.** Build chart 3 once the title mapping preserves seniority instead of collapsing it into the occupation.

### A built-in calibration case

Software developers are the one occupation with outside time-use data: Microsoft, Atlassian, and the Brooks lineage all put hands-on coding at roughly 15–30% of time. If the O*NET-based estimate for software developers puts Produce at 60%, the frequency-to-effort model is miscalibrated. Better to learn that on the one occupation where you can check before publishing 894 profiles.

---

## Part 4: Where the inference breaks

**Mention isn't time.** This is the central limit. Postings measure emphasis. Only the task layer approximates activity, and only ordinally.

**Phase-neutral concepts dominate.** Python, Excel, and communication skills appear constantly and say nothing about phase. Counting them toward Produce inflates every profile. Use only phase-diagnostic concepts for phase charts, and report what share of mentions qualified.

**Lag runs in both directions.** Postings lag the work, and O*NET lags postings. Agent adoption moved in 18 months; entry-level code-review mentions took five years to double. A chart can be accurate and still describe last cycle's job.

**Representativeness.** The repository already states that dataset frequency doesn't establish labor-market demand. The same limit applies to every emphasis chart here. Until the corpus is deduplicated and its coverage characterized, emphasis charts describe the corpus, not the labor market.

**Ghost postings and boilerplate.** Some postings are never filled, and many copy requirement lists from templates. Deduplicating near-identical text helps, but some inflation can't be removed.

**The phase mapping itself.** Tagging work activities to phases is judgment. Treat it like every other lexicon claim: drafted, evidenced, sampled for human review, and versioned.
