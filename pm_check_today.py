#!/usr/bin/env python3
"""Evening inspire brief step 1: check posts_all.csv for today's founder posts."""
import csv, io, subprocess, sys

today = subprocess.run(["date", "+%Y-%m-%d"], capture_output=True, text=True).stdout.strip()
print("TODAY:", today)

with open("/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv", newline="") as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    fields = reader.fieldnames

print("FIELDS:", fields)
print("PARSED ROWS:", len(rows))

def date_of(row):
    for k in ("publishedAt", "date", "published_at", "timestamp", "postedAt"):
        v = row.get(k)
        if v:
            return v
    return ""

todays = [r for r in rows if date_of(r).startswith(today)]
print("POSTS TODAY:", len(todays))
for r in todays:
    slim = {k: v for k, v in r.items() if v}
    print(slim)

# also show the 5 most recent rows regardless of date, to sanity-check date format
print("\n--- 5 most recent rows (raw publishedAt) ---")
for r in rows[-5:]:
    print(date_of(r), "|", (r.get("account") or r.get("username") or r.get("platform") or "?"), "|", (r.get("content") or "")[:60])
