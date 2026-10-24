# statics medians for the morning brief (from refreshed posts_all.csv)
import csv, statistics

rows = list(csv.DictReader(open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv')))

def is_reel(r):
    return r.get('is_reel') in ('True', 'true', '1')

def v(x):
    try:
        return float(x) if x not in ('', None) else None
    except Exception:
        return None

for acc in ('drey_ig', 'kevin_ig'):
    st = [v(r['views']) for r in rows if r['account'] == acc and not is_reel(r)]
    st = [x for x in st if x is not None]
    rl = [v(r['views']) for r in rows if r['account'] == acc and is_reel(r)]
    rl = [x for x in rl if x is not None]
    print(f"{acc}: statics n={len(st)} median={statistics.median(st):.0f} | reels n={len(rl)} median={statistics.median(rl):.0f}")

# 30d statics median for kevin (as prior briefs used)
import datetime
cutoff = '2026-09-24'
kst = [v(r['views']) for r in rows if r['account'] == 'kevin_ig' and not is_reel(r) and r['date'] >= cutoff]
kst = [x for x in kst if x is not None]
print(f"kevin_ig statics 30d: n={len(kst)} median={statistics.median(kst):.0f}")

# drey confession + room medians (n counts) and last-9-reel miss streak context
d = [r for r in rows if r['account'] == 'drey_ig' and is_reel(r)]
d.sort(key=lambda r: r['ts'])
print("drey_ig last 9 reels (date, views, theme):")
for r in d[-9:]:
    print(" ", r['date'], r['views'], r['theme'])
