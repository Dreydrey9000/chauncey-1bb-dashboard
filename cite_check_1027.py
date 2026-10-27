#!/opt/homebrew/bin/python3
"""Verify brief citations: drey confession opens, 10-26 opener, comment drought, kevin statics."""
import csv

PATH = "/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv"
rows = [r for r in csv.DictReader(open(PATH, newline="", encoding="utf-8"))]

def n(r, k):
    try: return int(r[k] or 0)
    except ValueError: return 0

print("== DREY IG October reels (date, views, comments, theme, opener) ==")
for r in rows:
    if r["account"] == "drey_ig" and r["date"] >= "2026-10-01":
        opener = (r["content"] or "")[:60].replace("\n", " ")
        print(f"  {r['date']} v={n(r,'views'):5d} c={n(r,'comments'):3d} {r['theme']:11s} | {opener}")

print("\n== DREY IG confession posts, all time ==")
for r in rows:
    if r["account"] == "drey_ig" and r["theme"] == "confession" and n(r, "views") > 0:
        print(f"  {r['date']} v={n(r,'views'):5d} c={n(r,'comments'):3d} | {(r['content'] or '')[:50]}")

print("\n== KEVIN IG statics (reel=False), October ==")
for r in rows:
    if r["account"] == "kevin_ig" and r["is_reel"] == "False" and r["date"] >= "2026-10-01":
        print(f"  {r['date']} v={n(r,'views'):5d} c={n(r,'comments'):3d} {r['theme']:11s} | {(r['content'] or '')[:50].replace(chr(10),' ')}")

print("\n== Comment drought check: Drey IG last 7 posts with views>0 ==")
d = sorted([r for r in rows if r["account"] == "drey_ig" and r["date"] >= "2026-10-01"], key=lambda r: r["date"])[-7:]
zeros = sum(1 for r in d if n(r, "comments") == 0)
print(f"  {zeros} of last 7 with 0 comments")

print("\n== KEVIN IG top 5 all time ==")
top = sorted([r for r in rows if r["account"] == "kevin_ig" and n(r,"views")>0], key=lambda r: -n(r,"views"))[:5]
for r in top:
    print(f"  {r['date']} v={n(r,'views'):6d} {r['theme']:11s} | {(r['content'] or '')[:50].replace(chr(10),' ')}")
