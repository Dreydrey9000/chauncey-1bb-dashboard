# Slot/window medians from THIS run's posts_all.csv (feed only) — 2026-11-26 AM
import csv, statistics
from datetime import datetime

rows = list(csv.DictReader(open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv')))

def feed(r):
    return r['content'].strip() != '' and '/stories/' not in r['url']

def num(r):
    try:
        return float(r['views'])
    except (ValueError, TypeError):
        return None

def hour_utc(r):
    try:
        return datetime.fromisoformat(r['ts']).hour
    except Exception:
        return None

drey = [r for r in rows if r['account'] == 'drey_ig' and feed(r)]
kevin = [r for r in rows if r['account'] == 'kevin_ig' and feed(r)]

# Drey slots: noon = 17-18 UTC (12p ET), evening = 0-1 UTC (7-9p ET prev day)
drey_noon = [num(r) for r in drey if hour_utc(r) in (17, 18) and num(r) is not None]
drey_eve = [num(r) for r in drey if hour_utc(r) in (0, 1) and num(r) is not None]
print(f'DREY noon-slot(12p ET) median={int(statistics.median(drey_noon)):,} n={len(drey_noon)}')
print(f'DREY evening-slot(7p ET) median={int(statistics.median(drey_eve)):,} n={len(drey_eve)}')
drey_statics = [num(r) for r in drey if r['is_reel'] == 'False' and num(r) is not None]
print(f'DREY statics median={int(statistics.median(drey_statics)):,} n={len(drey_statics)}')
drey_reels30 = [num(r) for r in drey if r['is_reel'] == 'True' and num(r) is not None and r['date'] >= '2026-10-27']
print(f'DREY reels 30d median={statistics.median(drey_reels30) if drey_reels30 else "n/a"} n={len(drey_reels30)}')

# Kevin statics by window: 2p = 18-20 UTC, 5-8p ET = 21-01 UTC
kstatic = [r for r in kevin if r['is_reel'] == 'False' and num(r) is not None]
k2p = [num(r) for r in kstatic if hour_utc(r) in (18, 19, 20)]
k58 = [num(r) for r in kstatic if hour_utc(r) in (21, 22, 23, 0, 1)]
kident = [num(r) for r in kstatic if r['theme'] == 'identity']
print(f'KEVIN statics 2p-window median={int(statistics.median(k2p)):,} n={len(k2p)}')
print(f'KEVIN statics 5-8p-window median={int(statistics.median(k58)):,} n={len(k58)}')
print(f'KEVIN identity statics median={int(statistics.median(kident)):,} n={len(kident)}')

# Kevin reel completion (his reels) and theme medians already computed; recalc room theme
kroom = [num(r) for r in kevin if r['theme'] == 'room' and num(r) is not None]
print(f'KEVIN room theme median={int(statistics.median(kroom)):,} n={len(kroom)}')

# Drey recent ai_systems reels top value (last 14d) for the 728 comparison
dai = sorted([num(r) for r in drey if r['is_reel'] == 'True' and r['theme'] == 'ai_systems'
              and num(r) is not None and r['date'] >= '2026-11-12'], reverse=True)
print(f'DREY ai_systems reels since 11-12: top5={dai[:5]}')
