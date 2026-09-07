# DP1 HL Computer Science — Lesson Calendar

Generator and data for the IB DP1 (Grade 11) HL Computer Science lesson calendar,
published as a Cowork Artifact.

## Files

- `build_site2.py` — generates `g11_calendar.html` from the JSON data files below. Run with `python3 build_site2.py`.
- `g11_lessons_v3.json` — the current 125-lesson schedule (content/assessment/IA/buffer), loaded by `build_site2.py`.
- `build_lessons_v3.py` — one-off script that produced `g11_lessons_v3.json` from `g11_all_items.json` + `classification.json` + the reused slot scaffolding in `debug_summary.json` / `all_slots.json`. Kept for reference; re-running it would regenerate the schedule from scratch (losing any manual tweaks made since).
- `classification.json` — manual half/full-lesson complexity judgement and bundled-pair list used by `build_lessons_v3.py`.
- `g11_all_items.json` — full IB syllabus item catalogue.
- `debug_summary.json`, `all_slots.json` — term dates, timetable slots, assessment Fridays, IA block — reused across builds.
- `g11_calendar.html` — the built output; this is what gets published to the Cowork Artifact.
- `progress_snapshots/` — dated snapshots of the live calendar's lesson-completion state (see below).

## How live progress relates to this repo

The published calendar is interactive: ticking a lesson complete, or adding a
Slides/Exit-ticket link, saves back into the *live Cowork Artifact*, not into
this repo. This repo is the generator + a history of the calendar's structure.

To capture completion progress here too, ask to "snapshot my progress" —
Claude will pull the live artifact's current lesson data and commit it under
`progress_snapshots/YYYY-MM-DD.json`, so you get a git history of what was
completed and when.

## Rebuilding

```
python3 build_site2.py
```
then publish the resulting `g11_calendar.html` as the Cowork Artifact.
