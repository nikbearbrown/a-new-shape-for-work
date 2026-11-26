# Phase-tag review: Software Developers and Web Developers

**Status: in progress.** The worksheet is built. My judgments are not filled in yet.

## What I am checking

Whether the phase each work activity is tagged with fits how the work is actually done in two occupations:

- **Software Developers (15-1252.00):** 17 tasks, linked to 18 detailed work activities (22 task-activity links).
- **Web Developers (15-1254.00):** 29 tasks, linked to 26 detailed work activities (37 task-activity links).

The two occupations share only 2 activities.

## The worksheet

[phase-tag-review-software-web-developers.tsv](phase-tag-review-software-web-developers.tsv) has one row for each task and the work activity it links to.

| Column | Meaning |
|---|---|
| `occupation`, `task_id`, `task`, `task_type` | The O*NET task |
| `dwa_id`, `dwa_name` | The detailed work activity (DWA) the task links to |
| `iwa_phase` | The phase of the broader activity group the DWA belongs to |
| `current_phase`, `basis` | The phase in [tags/dwa-phase-tags.tsv](../../tags/dwa-phase-tags.tsv) and what it was based on (verb, object or activity group) |
| `my_phase`, `my_reason`, `when_it_applies` | My judgment: the phase I think fits, why, and in what setting. **Empty until I finish the review.** |

When the review is done, I will propose changes to `tags/dwa-phase-tags.tsv` in a separate pull request, using the `note`, `status` and `reviewed_by` fields as the contributor guide asks.

Source: O*NET 31.0 Database (Task Statements; Tasks to DWAs), U.S. Department of Labor, Employment and Training Administration, CC BY 4.0. Phases from this repository's `tags/`.
