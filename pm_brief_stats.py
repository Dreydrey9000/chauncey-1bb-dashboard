#!/opt/homebrew/bin/python3
"""Summarize posts_all.csv: per-account/theme medians + recent posts for the inspire brief."""
import csv, statistics, collections, datetime

PATH = "/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv"

rows = []
with open(PATH, newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        try:
            r["views_n"] = int(r["views"] or 0)
            r["likes_n"] = int(r["likes"] or 0)
            r["comments_n"] = int(r["comments"] or 0)
        except ValueError:
            continue
        rows.append(r)

# per account x theme medians (views>0 only)
med = collections.defaultdict(list)
for r in rows:
    if r["views_n"] > 0:
        med[(r["account"], r["theme"])].append(r["views_n"])

print("== MEDIANS by account x theme (views, n) ==")
for (acct, theme), v in sorted(med.items()):
    if len(v) >= 3:
        print(f"{acct:12s} {theme:14s} median={int(statistics.median(v)):6d} n={len(v)}")

# top posts per founder account overall
print("\n== TOP 6 POSTS per founder account (by views) ==")
for acct in ["drey_ig", "drey_tt", "kevin_ig", "kevin_tt"]:
    sub = sorted([r for r in rows if r["account"] == acct and r["views_n"] > 0],
                 key=lambda r: -r["views_n"])[:6]
    print(f"\n-- {acct} --")
    for r in sub:
        print(f"  {r['date']} v={r['views_n']:7d} c={r['comments_n']:4d} reel={r['is_reel']} theme={r['theme']}")
        print(f"     {r['content'][:90].replace(chr(10),' ')}")

# last 7 days of posts per founder account
print("\n== RECENT (max date in file minus 7d) ==")
dates = [r["date"] for r in rows if r["date"]]
latest = max(dates)
cutoff = (datetime.date.fromisoformat(latest) - datetime.timedelta(days=7)).isoformat()
print(f"latest date in CSV: {latest}; cutoff: {cutoff}")
for acct in ["drey_ig", "drey_tt", "kevin_ig", "kevin_tt"]:
    sub = [r for r in rows if r["account"] == acct and r["date"] and r["date"] >= cutoff]
    sub.sort(key=lambda r: r["date"])
    print(f"\n-- {acct} ({len(sub)} posts in window) --")
    for r in sub:
        print(f"  {r['date']} v={r['views_n']:7d} c={r['comments_n']:4d} reel={r['is_reel']} theme={r['theme']}")

# confession/room vs AI-tool anchors
print("\n== DREY IG anchors ==")
for label, themes in [("confession/room", {"confession", "room"}), ("ai_systems/tools", {"ai_systems", "tools", "ai_tools"})]:
    v = [r["views_n"] for r in rows if r["account"] == "drey_ig" and r["theme"] in themes and r["views_n"] > 0]
    print(f"{label}: n={len(v)} median={int(statistics.median(v)) if v else 'n/a'}")
allmed = [r["views_n"] for r in rows if r["views_n"] > 0]
print(f"all-accounts median views: {int(statistics.median(allmed))} (n={len(allmed)})")
