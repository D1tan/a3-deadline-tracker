#!/usr/bin/env python3
"""Standalone deadline store for the deadline-tracker skill (standard library only)."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
import uuid
from datetime import date, datetime, timezone
from pathlib import Path


def store_path() -> Path:
    home = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))
    return home / "data" / "deadlines.json"


def load() -> list[dict]:
    try:
        return json.loads(store_path().read_text())
    except FileNotFoundError:
        return []


def save(items: list[dict]) -> None:
    path = store_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=".deadlines-")
    with os.fdopen(fd, "w") as handle:
        json.dump(items, handle, indent=1)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(tmp, path)


def describe(item: dict, today: date) -> str:
    days = (date.fromisoformat(item["due"]) - today).days
    when = ("due today" if days == 0 else "due tomorrow" if days == 1 else f"due in {days} days" if days > 0
            else f"{-days} day{'s' if days < -1 else ''} overdue")
    course = f" [{item['course']}]" if item.get("course") else ""
    return f"{item['id']}  {item['due']}  {item['title']}{course} — {when}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="deadlines")
    sub = parser.add_subparsers(dest="cmd", required=True)
    add = sub.add_parser("add")
    add.add_argument("title")
    add.add_argument("due", help="YYYY-MM-DD")
    add.add_argument("--course", default="")
    add.add_argument("--notes", default="")
    listing = sub.add_parser("list")
    listing.add_argument("--days", type=int, default=14)
    done = sub.add_parser("done")
    done.add_argument("id")
    args = parser.parse_args(argv)

    items = load()
    today = date.today()
    if args.cmd == "add":
        date.fromisoformat(args.due)
        item = {"id": uuid.uuid4().hex[:8], "title": args.title.strip(), "due": args.due, "course": args.course,
                "notes": args.notes, "done": False, "created": datetime.now(timezone.utc).isoformat()}
        items.append(item)
        save(items)
        print("Tracked:", describe(item, today))
    elif args.cmd == "list":
        due = sorted((i for i in items if not i.get("done")
                      and (date.fromisoformat(i["due"]) - today).days <= args.days), key=lambda i: i["due"])
        print("\n".join(describe(i, today) for i in due) or "Nothing due.")
    else:
        for item in items:
            if item["id"] == args.id:
                item["done"] = True
                save(items)
                print("Completed:", item["title"])
                return 0
        print(f"No deadline with id {args.id}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
