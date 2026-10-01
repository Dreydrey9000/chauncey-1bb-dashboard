import csv
from datetime import datetime
rows = list(csv.DictReader(open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv')))
def d(x):
    try: return datetime.strptime(x[:10], '%Y-%m-%d')
    except Exception: return None
def v(x):
    try: return int(float(x))
    except Exception: return 0
drey = sorted([r for r in rows if r['account']=='drey_ig'], key=lambda r: r['date'])
print("DREY IG last 5:")
for r in drey[-5:]:
    print(f"  {r['date'][:10]} reel={r['is_reel']} v={r['views']} c={r['comments']} theme={r['theme']}")
dreels = [r for r in drey if r['is_reel']=='True']
last_reel = dreels[-1]['date'][:10]
print("Drey last reel:", last_reel, "| days silent:", (datetime(2026,10,1)-d(last_reel)).days)
print()
kreels = sorted([r for r in rows if r['account']=='kevin_ig' and r['is_reel']=='True' and r['date']>='2026-09-20'], key=lambda r: r['date'])
print("KEVIN IG reels since 9/20:")
for r in kreels:
    print(f"  {r['date'][:10]} v={r['views']} dur={r['dur_s']}s skip={r['skip']} theme={r['theme']}")
print()
k14 = [r for r in rows if r['account']=='kevin_ig' and r['date']>='2026-09-17']
ks = sorted([v(r['views']) for r in k14 if r['is_reel']=='True'])
kt = sorted([v(r['views']) for r in k14 if r['is_reel']!='True'])
def med(l): return l[len(l)//2] if l else None
print(f"KEVIN IG since 9/17: reels median={med(ks)} n={len(ks)} | statics median={med(kt)} n={len(kt)}")
top = sorted(k14, key=lambda r: v(r['views']), reverse=True)[:4]
for r in top:
    print(f"  TOP {r['date'][:10]} v={r['views']} reel={r['is_reel']} theme={r['theme']} cap={r['content'][:60]}")
