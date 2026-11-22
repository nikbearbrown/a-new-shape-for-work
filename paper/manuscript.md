# A New Shape for Work

*What jobs involve, what employers advertise, and where AI use is visible*

**Rough first draft · 22 November 2026 · For author review**

## Abstract

An employer can advertise for software developers who write code and then hire them into work that requires substantial coordination. A task inventory and a job ad can both describe that job accurately while emphasizing different things. This paper presents a prototype for comparing three views of an occupation: the mix of activities described in O*NET, the emphasis of job advertisements, and the portion of modeled activity weighted by published evidence of Claude use. The prototype organizes work into six phases: understand, plan, produce, check, sustain, and coordinate. It builds activity profiles for 911 O*NET occupations. In a U.S. subset of a LinkedIn job-ad collection, the title matcher assigned 406,172 of 1,149,342 rows to occupations before duplicate removal; 409 rated occupations had enough mapped postings for a side-by-side profile. In the pilot, checking accounts for 32% of the task-weight index for software quality assurance analysts and testers, compared with 63% of their phase-diagnostic posting mentions. Differences like this help identify what to investigate. The denominators differ, and the prototype measures neither time on the job nor the effects of AI on employment.

## 1. Why describe the shape of a job?

A job title tells us little about how the work gets done. An electrician may install equipment, inspect an installation, troubleshoot faults, and coordinate with another trade. All four activities belong to the same job. Yet a job ad may say much more about troubleshooting than installation. It might do so because troubleshooting is difficult to hire for, because the opening is on a maintenance crew, or because the posting template emphasizes it. None of those explanations tells us how the worker spends a day.

AI makes this distinction especially important. A tool that helps draft code might shorten one step in a software project while increasing the need to check its output or coordinate changes across teams. That is a hypothesis about how work changes. An ad mentioning code review, or a dataset showing that people ask Claude to help with programming, does not by itself establish that such a shift has happened.

We use *job shape* to mean the distribution of a specified measure across phases of work. We compare three measures rather than collapse them into one index. For workers and educators, the comparison can help distinguish what gets someone hired from what they need to practice. For researchers, it identifies questions that require better evidence. Is a skill genuinely more central to an occupation, or merely more prominent in recruiting language? Is AI being used for a task because it saves work, because it helps someone do better work, or because the task is easy to try in a chat interface?

## 2. Related work

Task-based accounts of technological change shift attention from occupational titles to the activities that workers perform. Autor, Levy, and Murnane (2003) used that distinction to investigate how computerization could change the task composition of employment. We take the task as a unit of analysis but do not estimate a historical effect of technology. Our contribution is a way to display comparable profiles while keeping the evidence for each profile separate.

Deming and Kahn (2018) used job advertisements to study variation in employer skill requirements. Their work motivates treating recruiting text as informative in its own right. Our question is narrower: how does emphasis in an ad corpus line up with an independently constructed occupational task profile? Massenkoff and McCrory (2026) combine evidence about language-model capabilities with work-related Claude use to study AI exposure. We reuse their published task-level measure, but apply the prototype's own task weights. Our aggregates therefore should not be read as reproductions of their exposure estimates.

## 3. Measures and methods

### 3.1. Six phases

The phases describe the function an activity serves, not a fixed sequence. **Understand** means gathering information or assessing a situation. **Plan** means deciding what to do and how. **Produce** means carrying out the work or delivering the service. **Check** means inspecting, testing, or evaluating its quality. **Sustain** means maintaining something already in operation. **Coordinate** means aligning work across people. One task can contribute to more than one phase. The same activity can serve different purposes in different occupations. An analyst may analyze data to decide what to do next, or the analysis may be the product the client asked for.

### 3.2. Occupational activity

We used O*NET 31.0 task statements, ratings, and links to detailed work activities. The phase rules begin with 41 generalized work activities, refine the mapping at 332 intermediate activities, and assign draft labels to 2,087 detailed work activities. A task divides its weight equally across its linked detailed activities. All phase tags in this first pass are draft judgments.

For each task, the primary weight multiplies the mean of its seven reported frequency categories (coded 1 through 7), its importance rating, and its relevance fraction. A missing relevance rating defaults to one. We sum the resulting weights by phase and normalize within each occupation. Two sensitivity variants replace the mean category with either an assumed annual occurrence rate or a constant. A frequently performed task could take seconds or hours, so none of the three variants measures time. In the manuscript we call this an *activity index*; the prototype interface labels it estimated effort.

### 3.3. Recruiting emphasis

The posting pilot uses a U.S. subset of a LinkedIn collection whose retained records were first seen January 12–17, 2024. The matcher compares normalized listing titles with O*NET titles and aliases, including leading- and trailing-phrase matches. An unresolved or ambiguous title need not receive a code. A title assignment is a proposed link, not an audited classification. To reduce repeated ads, the pipeline first deduplicates by company, title, and location, then checks for identical summary text within an occupation. These rules can still miss duplicate vacancies and can collapse genuinely separate openings.

The phase analysis uses the dataset's extracted skill phrases, not a new human annotation of each original ad. Within each occupation, the prototype scores the 400 most common phrases. A phrase such as code review can signal Check; a tool name alone does not reliably identify a phase. The posting profile divides the count of diagnostic mentions in a phase by the total diagnostic mentions. It is not the percentage of ads or of hires. The separate Google Jobs data-analyst series illustrates a longitudinal interface and is not used for the three contrasts below or to infer a general trend.

### 3.4. AI-use evidence

We link the Anthropic Economic Index's published task-penetration file to O*NET task text after normalizing case and whitespace. The published score reflects eligibility and observed work-related Claude use under the source's criteria, with automated use weighted more heavily than augmentative use. For each phase, we multiply each task's contribution to the activity index by its penetration score, then sum. The result is a penetration-weighted share of the index. The implementation contributes zero to its numerator for an unmatched task; future versions should distinguish unknown from a matched zero in the display. The overlay does not represent all AI tools, the fraction of workers using AI, or the probability that a job will be automated.

## 4. What the prototype shows

Of 1,149,342 U.S. rows in the LinkedIn snapshot, 406,172 (35.34%) were assigned before deduplication, 216,975 (18.88%) were ambiguous, 521,332 (45.36%) did not match, and 4,863 (0.42%) were explicitly excluded. About a third of assignments (134,405) used leading- or trailing-phrase matches. The two duplicate filters left 277,976 records. The posting layer returned mapped records for 915 occupation codes; 429 met the minimum of 50 retained postings. Of the 911 occupations with O*NET activity profiles, 849 had some posting coverage and 409 met that threshold. Fifty is a display cutoff, not a test of precision or representativeness.

| Occupation | Phase | Share of task-weight index | Share of diagnostic ad mentions | Retained ads | Diagnostic mentions |
|---|---|---:|---:|---:|---:|
| Software quality assurance analysts and testers | Check | 32.28% | 62.76% | 543 | 2,672 |
| Software developers | Coordinate | 36.10% | 8.02% | 6,336 | 17,915 |
| Electricians | Sustain | 14.40% | 48.70% | 686 | 2,193 |

These are useful contrasts precisely because the columns answer different questions. An ad may foreground testing because testing differentiates an opening. Coordination may be common in software development but less often captured by the extracted skill list or rules. A hiring corpus may also contain more maintenance openings than the electrician task inventory would lead one to expect. The pilot does not distinguish these explanations. A gap should direct attention to the ads, tagging rules, and workers' accounts before it guides a curriculum or a staffing decision.

The direction of each gap survives the two alternate weighting choices: QA Check ranges from 26.90% to 34.14%; developer Coordinate, 30.75% to 36.40%; and electrician Sustain, 12.39% to 18.53%. That is a check on frequency weights only. No alternative phase annotations were used. Even among the 400 most common phrases, only 41.84%, 23.44%, and 27.70%, respectively, were diagnostic in these three cases.

The penetration-weighted activity index is 34.79% for software developers and 6.09% for registered nurses; it is zero in the prototype for electricians. A zero says the matched source and model contributed nothing under this definition. It does not establish that electricians make no use of AI. Separately, weighting sensitivity is visible even for a familiar role: software developers' Produce share is 16.35% under the ordinal model, 21.87% under the occurrence model, and 15.54% under the flat model. This comparison measures sensitivity to the weighting assumptions, not agreement with an independent observation of working hours.

## 5. Limits and the next test

The sources describe different periods. The O*NET release date is not the date every occupation was observed. For example, the developer task ratings are from incumbents in August 2025, while the QA ratings are from occupational experts in August 2022. The prototype also retains rating cells flagged for recommended suppression. A sensitivity check should use the [O*NET quality flags and sample metadata](https://www.onetcenter.org/dictionary/31.0/csv/task_ratings.html) and report how results change when flagged cells are excluded.

The immediate priority is to validate the links before broadening the corpus. A stratified review should include direct, ambiguous, and unmatched titles, as well as multiple industries and seniority levels. A reviewer should see the duties alongside the title. For phase classification, two reviewers can tag the same activities independently, record alternative labels when the phase depends on context, and adjudicate disagreements. The repository includes a replication kit for independently tagging work activities, titles, and skill phrases; agreement between models can identify review targets but does not establish accuracy.

The strongest test would compare job ads, worker accounts, and task diaries from the same kinds of jobs. That design could distinguish recruiting emphasis from task frequency and measured time. It could also test whether work shifts from production toward checking or coordination after AI enters a workflow. Such a study would need a comparison over time and a credible way to account for changes in employers, job composition, and selection into AI use.

A practical next step is to choose three occupations with large gaps and ask, for each one, whether the gap survives review of the title match, the phase tag, and actual worker descriptions. If the gap disappears, the prototype has identified a measurement error. If it persists, it has identified a question worth investigating about how employers describe work and how workers do it.

## References and data

- Autor, D. H., Levy, F., and Murnane, R. J. (2003). [The Skill Content of Recent Technological Change: An Empirical Exploration](https://doi.org/10.1162/003355303322552801). *Quarterly Journal of Economics*, 118(4), 1279–1333.
- Deming, D., and Kahn, L. B. (2018). [Skill Requirements across Firms and Labor Markets: Evidence from Job Postings for Professionals](https://www.nber.org/papers/w23328). *Journal of Labor Economics*, 36(S1), S337–S369. Link leads to the authors' working-paper version.
- Massenkoff, M., and McCrory, P. (2026). [Labor market impacts of AI: A new measure and early evidence](https://www.anthropic.com/research/labor-market-impacts). Anthropic. [Published data release](https://huggingface.co/datasets/Anthropic/EconomicIndex/tree/4e5f69fab13a9c3f7d0dcc31a6f893a9818738f6/labor_market_impacts).
- U.S. Department of Labor, Employment and Training Administration. [O*NET 31.0 Database](https://www.onetcenter.org/dl_files/database/db_31_0_text.zip). Used under [CC BY 4.0](https://www.onetcenter.org/license_db.html). O*NET is a trademark of USDOL/ETA.
- Asaniczka. [1.3M LinkedIn Jobs & Skills (2024)](https://www.kaggle.com/datasets/asaniczka/1-3m-linkedin-jobs-and-skills-2024). Corpus source; see repository documentation for transformation and rights notes.
