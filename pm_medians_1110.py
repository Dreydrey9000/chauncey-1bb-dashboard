#!/usr/bin/env python3
"""PM 2026-11-10: medians for tonight's brief citations (30-post window per account)."""
import csv, os, statistics, collections

BASE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(BASE, 'posts_all.csv'))))

def med(vals):
    return statistics.median(vals) if vals else None

for acct in ('drey_ig', 'kevin_ig'):
    sub = sorted([r for r in rows if r['account'] == acct], key=lambda r: r['ts'])
    last30 = sub[-30:]
    print(f'=== {acct} (last 30 posts, through {last30[-1]["date"]}) ===')
    byreel = collections.defaultdict(list)
    bytheme = collections.defaultdict(list)
    for r in last30:
        try:
            v = int(float(r['views'] or 0))
        except Exception:
            continue
        byreel[r.get('is_reel', '')].append(v)
        t = (r.get('theme') or '').strip()
        if t:
            bytheme[t].append(v)
    for k, vs in sorted(byreel.items()):
        print(f'  is_reel={k!r}: n={len(vs)} median={med(vs):.0f}')
    for t, vs in sorted(bytheme.items(), key=lambda x: -(med(x[1]) or 0)):
        print(f'  theme={t}: n={len(vs)} median={med(vs):.0f}')

# Drey AI-tool reel run + comment total (Nov 6 -> today incl. fresh pull)
print('\nDrey ai_systems-adjacent reels Nov 6-10 (CSV + tonight Zernio pull):')
run = [(102, 0), (170, 1), (186, 0), (187, 0), (124, 0)]  # Dfcq6,DfYl4,DfgUM3? order below
for v, c in run:
    print(f'  views={v} comments={c}')
print('band:', min(v for v, _ in run), '-', max(v for v, _ in run),
      '| total comments across 5:', sum(c for _, c in run))

# Kevin statics recent run
print('\nKevin IG statics (non-reel) last 6 in CSV:')
k = sorted([r for r in rows if r['account'] == 'kevin_ig' and r.get('is_reel') == 'False'], key=lambda r: r['ts'])
for r in k[-6:]:
    print(f"  {r['date']} views={r['views']} likes={r['likes']} comments={r['comments']} theme={r['theme']}")
