---
name: deadline-tracker
description: "Track assignments, project milestones and bills; surface what is due soon in briefings and on request."
version: 1.0.0
author: CSCI 599 A3 (Jordan Lee test persona)
license: MIT
metadata:
  hermes:
    tags: [Productivity, Deadlines, Students, Briefing]
    related_skills: []
---

# Deadline Tracker

Keep a small, durable list of dated obligations and remind the user before
they slip. Built for students juggling coursework, but works for any dated task.

## When to Use

- The user mentions something with a due date: "the 570 problem set is due Friday",
  "rent is due on the 1st", "remind me the demo is on the 18th".
- The user asks "what's due?", "anything due this week?", "what's overdue?".
- Building a morning briefing or daily recap (include items due within 3 days
  and everything overdue).
- The user says something is finished ("I submitted the 599 report").

## Tools

Prefer the native tools when they are available (A3 assistant deployment):

| Action | Tool |
|---|---|
| Add | `a3_deadline_add(title, due=YYYY-MM-DD, course?, notes?)` |
| List | `a3_deadline_list(days=14)` (includes overdue items) |
| Complete | `a3_deadline_done(id)` |

Without those tools, use the bundled script through the terminal tool:

```sh
python3 scripts/deadlines.py add "CSCI 570 problem set 6" 2026-11-14 --course "CSCI 570"
python3 scripts/deadlines.py list --days 7
python3 scripts/deadlines.py done <id>
```

The script stores data in `$HERMES_HOME/data/deadlines.json` (atomic writes,
standard library only).

## Procedure

1. Resolve relative dates ("Friday", "next Tuesday", "end of month") against
   today's date in the user's timezone before saving. If the date is ambiguous
   (e.g. "the 5th" when it could be this month or next), ask once.
2. Use a short title that names the deliverable, and put the course or project
   in `course`. Do not store email bodies or anything copied from untrusted content.
3. Confirm in one line: "Tracked: CSCI 570 problem set 6 — due Fri Nov 14."
4. When listing, sort by due date, mark overdue items first, and say how many
   days remain ("due tomorrow", "2 days overdue").
5. Only add deadlines the user states or explicitly confirms. If an email or
   calendar invite mentions a deadline, offer to track it; do not add it silently.

## Pitfalls

- Saving the date in UTC shifts late-evening deadlines to the next day; dates
  are calendar dates in the user's timezone.
- Duplicates: before adding, list items due within ±3 days and check for the same
  deliverable; update instead of adding a second copy.
- Completed items stay in the file (for recaps) but are excluded from lists.

## Verification

After adding, list the next 14 days and confirm the item appears with the right date.
