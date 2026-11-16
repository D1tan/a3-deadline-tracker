# Hermes skill tap: deadline-tracker

A [Hermes Agent](https://hermes-agent.nousresearch.com/docs) skill tap with one
skill, **deadline-tracker**: track assignments, project milestones and bills,
and surface what is due soon in briefings and on request. Written for the
CSCI 599 Assignment 3 personal assistant; uses only the Python standard library.

```
skills/
└── deadline-tracker/
    ├── SKILL.md            # when to use, procedure, pitfalls, verification
    └── scripts/deadlines.py  # add / list / done, JSON store under $HERMES_HOME/data
```

## Install

```sh
hermes skills tap add OWNER/REPO
hermes skills install OWNER/REPO/skills/deadline-tracker --yes
hermes skills list | grep deadline-tracker
```

Replace `OWNER/REPO` with this repository. Hermes records the installed tree
revision in `~/.hermes/skills/.hub/lock.json`; release `v1.0.0` is the version
submitted for the assignment.

## Use

Ask the agent things like "the 570 problem set is due Friday" or "what's due
this week?". Without the A3 deployment's native tools the skill runs its script:

```sh
python3 scripts/deadlines.py add "CSCI 570 problem set 6" 2026-11-21 --course "CSCI 570"
python3 scripts/deadlines.py list --days 14
python3 scripts/deadlines.py done <id>
```

All example data is fictional.
