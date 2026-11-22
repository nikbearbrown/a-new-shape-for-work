# Research data: A New Shape for Work

This folder is the public research-data deposit for the November 21, 2026 prototype. It holds machine-readable tables and source information, rather than a second copy of the recruiting corpus.

| File | Unit and use |
|---|---|
| [activity-profiles.csv](activity-profiles.csv) | One row per rated occupation, weighting model, and phase. Shares are fractions of the modeled activity index, not working hours. The AI column weights task contributions by Anthropic's published task penetration. Unmatched tasks contribute zero to that numerator; unknown does not mean absence of AI use. |
| [posting-emphasis.csv](posting-emphasis.csv) | One row per mapped occupation and phase, with retained ad counts, phrase denominators, and first/last observed dates. Share is relative to diagnostic mentions among the most frequent skill phrases. Blank shares mean no phase profile is available; blank is not zero. Phase rows repeat occupation-level counts and must not be summed to obtain ad totals. |
| [sources/anthropic-task-penetration.csv](sources/anthropic-task-penetration.csv) | Unmodified public upstream input, 17,998 task-score rows. See attribution and hash below. |
| [SOURCE-MANIFEST.json](SOURCE-MANIFEST.json) | Pinned source revisions, snapshot commit, checksums, provenance, and row counts. |
| [export-profiles.py](export-profiles.py) | Recreates both tables from the repository's public JSON: run `python3 research-data/export-profiles.py` from the checkout. It stops before writing if any pinned input or dashboard JSON has a missing or invalid checksum. |

The complete current analysis artifacts continue to live in [page/data/](../page/data/): occupation task and phase profiles (`onet.json`), all-title recruiting aggregates (`by-occupation.json`), and the eight-title and dated data-analyst pilot (`postings.json`). See [method](../docs/METHOD.md), [data gathering](../docs/GATHERING-DATA.md), and [unreviewed phase tags](../tags/). The recruiting data are a corpus snapshot, not labor-market estimates. The records for which both layers can be shown number 409, not all 429 occupation codes meeting the posting cutoff.

## Source versions and rights

- **O*NET® 31.0 Database**, U.S. Department of Labor, Employment and Training Administration (USDOL/ETA). [Original text archive](https://www.onetcenter.org/dl_files/database/db_31_0_text.zip), SHA-256 `6883548adf5fde64cf6f801b35d15519c9225f2732c3cab0e281c652d16b23a9`. Used under [CC BY 4.0](https://www.onetcenter.org/license_db.html). O*NET® is a trademark of USDOL/ETA. Humanitarians AI Incorporated derived phase labels, weights, and profiles from the original tables. USDOL/ETA has not approved, endorsed, or tested these modifications.
- **Anthropic Economic Index**, [task penetration release at commit 4e5f69f](https://huggingface.co/datasets/Anthropic/EconomicIndex/tree/4e5f69fab13a9c3f7d0dcc31a6f893a9818738f6/labor_market_impacts), data released under CC BY per the [pinned dataset card](https://huggingface.co/datasets/Anthropic/EconomicIndex/blob/4e5f69fab13a9c3f7d0dcc31a6f893a9818738f6/README.md). The unchanged file's SHA-256 is `85bee872db1d55d3e9a7f4e89da5ae4a5d59aa8ec875d728fbf4b7d820984616`. [Method report](https://www.anthropic.com/research/labor-market-impacts).
- **Asaniczka, [1.3M LinkedIn Jobs & Skills (2024)](https://www.kaggle.com/datasets/asaniczka/1-3m-linkedin-jobs-and-skills-2024)**, version 2, Open Data Commons Attribution per the source notes. The public tables contain occupation-level counts, not original postings, employers, URLs, or job-description text. The raw archive remains in the project's Explorer source collection.
- **Luke Barousse, [Data Analyst Job Postings (Google Search)](https://www.kaggle.com/datasets/lukebarousse/data-analyst-job-postings-google-search)**, version 744, Apache 2.0 per the source notes. Only the existing pilot aggregates are shared here; the raw archive stays on Explorer.
- **Skills Lexicon**, [repository](https://github.com/nikbearbrown/skills-lexicon), source revision `0ba8e0c2` for class assignments in the dashboard. No copy of the lexicon input is needed to read the tables in this folder.

## Where future research output goes

Run LLM drafting and literature gathering outside Explorer. Deposit gathered source manifests, analysis tables and run evidence in the paper project's Explorer folder. Publish the redistributable research data and source notes in this GitHub folder; link to restricted or externally licensed material instead of mirroring it without permission. Keep raw recruiting archives and per-posting extracts off public GitHub. No Paper Orchestra literature run is included in this deposit. The deposit exporter verifies the published snapshot; it is not the upstream build. Before rebuilding the public dashboard from raw inputs, verify the pinned Anthropic file. A missing input must be represented as unavailable, not as zero AI coverage.
