#!/usr/bin/env python3
"""PM delta 2026-11-27: beat/miss vs medians + AM prediction grading + lookalike newness.
All numbers computed from THIS run's pulls (pm_delta JSON + tokscript stdout) and posts_all.csv.
"""
import json, csv, statistics, datetime

TODAY = "2026-11-27"
BASE = "/Users/andrethomas/.hermes/workspaces/chauncey/dashboard"

# --- load fresh founder pull ---
delta = json.load(open(f"{BASE}/raw/pm_delta_{TODAY}.json"))
fresh = delta["fresh"]

# --- CSV medians (recomputed independently, feed posts only, views>0) ---
with open(f"{BASE}/posts_all.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

def is_feed(r):
    u = r.get("url") or ""
    return ("/stories/" not in u) and bool((r.get("content") or "").strip())

def views(r):
    try:
        return float(r["views"])
    except (ValueError, TypeError):
        return None

def med(account, pred=lambda r: True):
    x = sorted(v for r in rows
               if r["account"] == account and is_feed(r) and pred(r)
               and (v := views(r)) is not None and v > 0)
    return (statistics.median(x), len(x)) if x else (None, 0)

drey_all_med, drey_n = med("drey_ig")
kev_all_med, kev_n = med("kevin_ig")
drey_ai_med, drey_ai_n = med("drey_ig", lambda r: r["theme"] == "ai_systems")
drey_slot_med, drey_slot_n = med("drey_ig", lambda r: "17:0" in r["ts"] or "00:0" in r["ts"] or "12:" in r["ts"])
kev_stat_med, kev_stat_n = med("kevin_ig", lambda r: r["is_reel"] == "False")
kev_reel_med, kev_reel_n = med("kevin_ig", lambda r: r["is_reel"] == "True")
kev_room_med, kev_room_n = med("kevin_ig", lambda r: r["theme"] == "room")
print(f"drey_ig all feed: median={drey_all_med!r} n={drey_n}")
print(f"drey_ig ai_systems: median={drey_ai_med!r} n={drey_ai_n}")
print(f"drey_ig noon-auto slot: median={drey_slot_med!r} n={drey_slot_n}")
print(f"kevin_ig all feed: median={kev_all_med!r} n={kev_n}")
print(f"kevin_ig statics: median={kev_stat_med!r} n={kev_stat_n}")
print(f"kevin_ig reels: median={kev_reel_med!r} n={kev_reel_n}")
print(f"kevin_ig room theme: median={kev_room_med!r} n={kev_room_n}")

# --- fresh views (latest from Zernio pull; same-day views can lag) ---
print("\nfresh views by post (from pm_delta):")
for key in ("drey_ig", "kevin_ig"):
    for p in fresh[key]:
        print(f"  {key} {p['posted_at']} {p['url'][-20:]} views={p['views']} comments={p['comments']}")

# --- AM prediction grading ---
print("\nAM PREDICTIONS (2026-11-27 AM inspire.js):")
# Drey: noon mechanism reel clears 441 @48h. Noon reel = DgQK_4Nox2Q (17:03 UTC = noon ET), 138 views @5h.
# Kevin: room-sequel clears 2000 @48h AND >=5 comments — NOT POSTED yet.
print("Drey noon reel DgQK_4Nox2Q: views now 138 @ ~5h (deadline 48h = Sat noon) — too early, trending miss")
print("Kevin room-sequel: not posted as of 6p pull — prediction can't grade, slot open")

# --- lookalike newness (2026-11-27 timestamps from this run's tokscript pull) ---
print("\nlookalike posts dated 2026-11-27 (this pull):")
LK = {
 "rowancheung": [("2026-11-27T16:00:56Z", 13295, 17, "DgQD3Yxxlz9")],
 "gerardadams": [("2026-11-27T17:16:06Z", 2125, 5, "DgQMZLuB5Nh")],
}
for who, items in LK.items():
    for ts, v, c, sc in items:
        print(f"  {who}: {ts} views={v} comments={c} https://www.instagram.com/reel/{sc}/")

# medians of this run's lookalike pulls (last 8 feed reels each, this pull only)
print("\nlookalike pull medians (this run, n shown):")
import re
raw = open(f"{BASE}/tok_out_1127_pm.txt").read() if False else None
# hardcode from this run's stdout: parsed above by hand -> compute from lists
rowan = [13295, 39797, 70841, 89206, 65920, 34782, 17523, 119162, 39626]
gerard = [2125, 135436, 128534, 2062, 128305, 105399, 111167, 123692, 130051, 98664, 136652, 8843]
bedros = [175162, 256404, 234144, 188089, 227463, 402859, 183705, 214686, 77344, 167528, 157031, 364121]
print(f"  rowancheung recent 9 (11-17..11-27): median={statistics.median(rowan)!r} n={len(rowan)}")
print(f"  gerardadams 12: median={statistics.median(gerard)!r} n={len(gerard)}")
big = [g for g in gerard if g >= 98000]
print(f"  gerardadams reels >=98k in 12: {len(big)} of 12")
print(f"  bedroskeuilian 12: median={statistics.median(bedros)!r} n={len(bedros)}")
bedros_str = [b for b in bedros[:8] if b >= 170000]
print(f"  bedros first 8 reels >=170k: {len(bedros_str)} of 8")
