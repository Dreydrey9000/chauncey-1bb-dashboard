# Final quotes audit (this run): Kevin Sunday median, reel windows, 30d medians, band counts
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

def wd(r):
    return datetime.fromisoformat(r['ts']).weekday()

def hour_utc(r):
    return datetime.fromisoformat(r['ts']).hour

kev = [r for r in rows if r['account'] == 'kevin_ig' and feed(r)]
ksun = [num(r) for r in kev if wd(r) == 6 and num(r) is not None]
print(f'Kevin Sunday feed median={int(statistics.median(ksun)):,} n={len(ksun)}')

k_reels = [r for r in kev if r['is_reel'] == 'True' and num(r) is not None]
k30 = [num(r) for r in k_reels if r['date'] >= '2026-10-27']
print(f'Kevin 30d reel median={statistics.median(k30) if k30 else "n/a"} n={len(k30)}')
# reels by window: 4-6p ET = 20-23 UTC
k46 = [num(r) for r in k_reels if hour_utc(r) in (20, 21, 22, 23)]
kother = [num(r) for r in k_reels if hour_utc(r) not in (20, 21, 22, 23)]
print(f'Kevin reels 4-8p ET window median={int(statistics.median(k46)) if k46 else "n/a":,} n={len(k46)} vs other times {int(statistics.median(kother)) if kother else "n/a":,} n={len(kother)}')
# best 3 reels with their post hours (ET)
top3 = sorted(k_reels, key=lambda r: -num(r))[:3]
for r in top3:
    t = datetime.fromisoformat(r['ts'])
    print(f"  top reel: {r['date']} {t.hour - 5 if t.hour >= 5 else t.hour + 19}p-ish ET views={int(num(r)):,} theme={r['theme']}")

# Kevin identity + confession statics medians
kident_st = [num(r) for r in kev if r['is_reel'] == 'False' and r['theme'] == 'identity' and num(r) is not None]
kconf_st = [num(r) for r in kev if r['is_reel'] == 'False' and r['theme'] == 'confession' and num(r) is not None]
print(f'Kevin identity statics median={int(statistics.median(kident_st)):,} n={len(kident_st)} | confession statics median={int(statistics.median(kconf_st)):,} n={len(kconf_st)}')

# Drey: coach-story reel is noon lane best; count noon reels since 11-12 (template-only streak)
drey = [r for r in rows if r['account'] == 'drey_ig' and feed(r) and r['is_reel'] == 'True']
noon = sorted([r for r in drey if hour_utc(r) in (17, 18)], key=lambda r: r['ts'], reverse=True)
print('Drey noon reels since 11-12 (newest first):')
for r in noon[:10]:
    print(f"  {r['ts'][:10]} {int(float(r['views'])):,} {r['theme']}")
