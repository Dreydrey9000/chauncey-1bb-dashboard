# CSV anchor stats for inspire brief (cron-safe: script file, not heredoc)
import csv, statistics
from collections import defaultdict

path = "/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv"
rows = []
with open(path, newline='', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        rows.append(r)

print("total rows:", len(rows))

by_acct = defaultdict(list)
for r in rows:
    by_acct[r['account']].append(r)

for acct, rs in by_acct.items():
    rs_sorted = sorted(rs, key=lambda r: r['ts'], reverse=True)
    print(f"\n=== {acct}: {len(rs)} posts; latest 3 ===")
    for r in rs_sorted[:3]:
        print(f"{r['date']} theme={r['theme']} reel={r['is_reel']} views={r['views']} likes={r['likes']} comments={r['comments']} saves={r['saves']} er={r['er']} | {r['content'][:70]!r}")

for acct in ['drey_ig', 'kevin_ig']:
    rs = by_acct[acct]
    themes = defaultdict(list)
    for r in rs:
        try:
            v = int(r['views'])
        except (ValueError, TypeError):
            continue
        themes[r['theme']].append(v)
    print(f"\n--- {acct} theme medians (n, median views) ---")
    for t, vs in sorted(themes.items(), key=lambda kv: -statistics.median(kv[1])):
        print(f"{t}: n={len(vs)} median={int(statistics.median(vs))}")
    allv = [int(r['views']) for r in rs if r['views'].isdigit()]
    print(f"OVERALL median views: {int(statistics.median(allv))} (n={len(allv)})")

rs = by_acct['kevin_ig']
reels = [int(r['views']) for r in rs if r['is_reel'] == 'True' and r['views'].isdigit()]
statics = [int(r['views']) for r in rs if r['is_reel'] != 'True' and r['views'].isdigit()]
print(f"\nkevin_ig reels median views: {int(statistics.median(reels))} (n={len(reels)})")
print(f"kevin_ig static median views: {int(statistics.median(statics))} (n={len(statics)})")

# Drey confession/room vs ai split for the anchor claim
rs = by_acct['drey_ig']
dr_theme = defaultdict(list)
for r in rs:
    try:
        dr_theme[r['theme']].append(int(r['views']))
    except (ValueError, TypeError):
        pass
print("\n--- drey_ig key themes ---")
for t in ['confession', 'room', 'ai_systems', 'ai_tools', 'other']:
    if t in dr_theme:
        vs = dr_theme[t]
        print(f"{t}: n={len(vs)} median={int(statistics.median(vs))} max={max(vs)}")
