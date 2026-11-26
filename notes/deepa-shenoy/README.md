# notes/deepa-shenoy

Notes from Deepa Shenoy ([@ds2204](https://github.com/ds2204)) on *A New Shape for Work*, moved here from email as Nik asked.

| File | What it is |
| --- | --- |
| `findings.md` | What I checked, what I found, and what I propose to change, with file and line references |
| `verify_findings.py` | Read-only script that prints the evidence for each finding from the repo's own files |
| `missing-ai-joins-review.csv` | All 157 rated tasks with no AI-overlay score, next to the closest Anthropic task wording, its similarity and its score |

## Run the checks

From the top of the repo:

```
python3 notes/deepa-shenoy/verify_findings.py
```

Standard library only. It reads files and writes nothing inside the repo. The reproduction check runs the authors' export scripts in a temporary copy.

## Status

| Item | Status |
| --- | --- |
| Deposit reproduction | Done: both CSVs and Figure 3 rebuild byte-identical |
| Security clearance tagged Sustain | Finding documented; fix and before/after shares pending per-occupation phrase counts |
| Reworded tasks among the 157 missing joins | Candidate list built. Proposed matches for paralegals, hydrologists and epidemiologists, not confirmed; next: O*NET Task ID check and a second reviewer |
| Dashboard summary wording on posting coverage | Suggested rewording documented |

No files outside `notes/deepa-shenoy/` are changed. `tags/` is untouched.

## AI use

I used Claude to help write `verify_findings.py`, build the candidate list in the CSV, and draft these notes. I checked every number against the source files myself. I did not use AI to choose any tags; the proposed match/no-match judgments are mine.
