import csv, statistics, json
from collections import defaultdict

rows = list(csv.DictReader(open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv')))
print("total rows:", len(rows))

ts = sorted(r['ts'] for r in rows)
print("oldest ts:", ts[0], "| newest ts:", ts[-1])

today = '2026-11-12'
todays = [r for r in rows if r['date'] == today]
print("\n=== POSTS DATED", today, "===")
for r in todays:
    print(json.dumps({k: r[k] for k in ('account','ts','views','reach','likes','comments','shares','saves','er','is_reel','theme','url')}))
    print("  text:", r['content'][:120].replace('\n',' '))

meds = defaultdict(list)
for r in rows:
    v = r['views']
    if v not in ('', '0', None):
        try: meds[r['account']].append(int(v))
        except: pass
print("\n=== MEDIANS (views, all history) ===")
for acct in sorted(meds):
    print(f"{acct}: n={len(meds[acct])} median={statistics.median(meds[acct]):.0f} max={max(meds[acct])}")

print("\n=== POSTS LAST 7 DAYS (2026-11-06..11-12) ===")
recent = [r for r in rows if '2026-11-06' <= r['date'] <= today]
for r in sorted(recent, key=lambda x: x['ts']):
    print(f"{r['date']} {r['account']:<9} views={r['views']:>6} likes={r['likes']:>4} comm={r['comments']:>3} reel={r['is_reel']} theme={r['theme']}")

for acct in ('drey_ig','kevin_ig'):
    tm = defaultdict(list)
    for r in rows:
        if r['account']==acct and r['views']:
            try: tm[r['theme']].append(int(r['views']))
            except: pass
    print(f"\n=== {acct} THEME MEDIANS ===")
    for t, vals in sorted(tm.items(), key=lambda kv: -statistics.median(kv[1])):
        print(f"  {t}: n={len(vals)} median={statistics.median(vals):.0f}")
