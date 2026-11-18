import csv, statistics as st
from collections import defaultdict
from datetime import datetime, timezone, timedelta

ET = timezone(timedelta(hours=-5))
rows = []
with open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv') as f:
    for r in csv.DictReader(f):
        rows.append(r)

def num(x):
    try: return float(x)
    except: return None

def parse_ts(ts):
    try: return datetime.fromisoformat(ts)
    except: return None

now = datetime(2026,11,18,12,1,tzinfo=timezone.utc)

print("=== FOUNDER POSTS SINCE Nov 16 12:00 UTC ===")
for r in rows:
    ts = parse_ts(r['ts'])
    if ts and ts >= datetime(2026,11,16,12,0,tzinfo=timezone.utc):
        age_h = round((now-ts).total_seconds()/3600,1)
        print(f"{r['account'][:8]:8} {r['date']} {ts.strftime('%H:%M')}Z (~{age_h}h ago) reel={r['is_reel']:5} views={r['views']:>6} likes={r['likes']:>4} comm={r['comments']:>3} skip%={r.get('skip','') or '-'} dur={r['dur_s'] or '-'} theme={r['theme']} url={r['url'][-20:]}")

print("\n=== DREY IG REELS: median views by theme (n) ===")
d = defaultdict(list)
all_drey_reels=[]
for r in rows:
    if r['account']=='drey_ig' and r['is_reel']=='True':
        v=num(r['views'])
        if v is not None:
            d[r['theme']].append(v); all_drey_reels.append(v)
for k,v in sorted(d.items(), key=lambda x:-st.median(x[1])):
    print(f"{k:12} median={st.median(v):>7.0f}  n={len(v)}")
print(f"ALL         median={st.median(all_drey_reels):>7.0f}  n={len(all_drey_reels)}")

print("\n=== KEVIN IG: statics vs reels ===")
ks, kr, kcomp = [], [], []
ktheme = defaultdict(list)
for r in rows:
    if r['account']=='kevin_ig':
        v=num(r['views'])
        if v is None: continue
        if r['is_reel']=='True':
            kr.append(v)
            c=num(r['skip'])
            if c is not None and c>0: kcomp.append(c)
        else:
            ks.append(v)
        ktheme[r['theme']].append(v)
print(f"statics median={st.median(ks):.0f} n={len(ks)} | reels median={st.median(kr):.0f} n={len(kr)} | reel completion median={st.median(kcomp):.1f}% n={len(kcomp)}")
print("top themes by median:", [(k, round(st.median(v)), len(v)) for k,v in sorted(ktheme.items(), key=lambda x:-st.median(x[1]))[:5]])

print("\n=== KEVIN REELS sorted by completion% (top 6, last 45 days) ===")
kk=[]
for r in rows:
    if r['account']=='kevin_ig' and r['is_reel']=='True':
        c=num(r['skip']); v=num(r['views'])
        ts=parse_ts(r['ts'])
        if c and c>0 and v is not None and ts and ts>=datetime(2026,10,4,tzinfo=timezone.utc):
            kk.append((c,v,r['date'],r['theme']))
for c,v,dt,th in sorted(kk,reverse=True)[:6]:
    print(f"compl={c:>5.1f}% views={v:>6.0f} {dt} {th}")

print("\n=== DREY IG REELS: median views by ET posting hour (n>=2) ===")
h = defaultdict(list)
for r in rows:
    if r['account']=='drey_ig' and r['is_reel']=='True':
        ts=parse_ts(r['ts']); v=num(r['views'])
        if ts and v is not None:
            h[ts.astimezone(ET).hour].append(v)
for k,v in sorted(h.items()):
    if len(v)>=2:
        print(f"{k:>2}:00 ET median={st.median(v):>6.0f} n={len(v)}")

liam_1pm = [(10338,354),(9987,288),(4663,80),(4301,52),(5417,99),(4621,92)]
liam_5pm = [(5495,76),(8714,69),(3658,29),(11732,294),(4250,63),(3481,30)]
v1=sum(x[0] for x in liam_1pm); c1=sum(x[1] for x in liam_1pm)
v5=sum(x[0] for x in liam_5pm); c5=sum(x[1] for x in liam_5pm)
print(f"\n=== LIAM 1pm vs 5pm UTC (6 days, today's pull) ===")
print(f"1pm: {c1} comments / {v1} views = {100*c1/v1:.2f}%  |  5pm incl outlier: {100*c5/v5:.2f}% | 5pm excl 294-outlier reel: {100*(c5-294)/(v5-11732):.2f}%")

# Bedros cadence math (12 reels pulled)
print("\n=== BEDROS cadence: 12 reels span ===")
print("Nov 16 18:13Z back to Oct 26 16:15Z = 21.1 days, 12 reels = ~1 reel / 1.76 days")
print("views range: 76137 - 363810; median of 12:", st.median([220123,339733,182879,209807,76137,167355,156901,363810,206459,243483,137928,219018]))
