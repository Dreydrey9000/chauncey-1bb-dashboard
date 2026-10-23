"""Evening medians: per-founder, per-format, last-30-day view medians from posts_all.csv."""
import csv, datetime, statistics, os

BASE = os.path.dirname(os.path.abspath(__file__))
today = datetime.date(2026, 10, 23)
cutoff = today - datetime.timedelta(days=30)

rows = []
with open(os.path.join(BASE, 'posts_all.csv')) as f:
    for r in csv.DictReader(f):
        rows.append(r)

print('CSV max date:', max(r['date'] for r in rows if r.get('date')))

def fmt(d):
    try:
        return datetime.date.fromisoformat(str(d)[:10])
    except Exception:
        return None

for acct in ('drey_ig', 'kevin_ig'):
    for is_reel in (True, False):
        vals, dates = [], []
        for r in rows:
            if r['account'] != acct:
                continue
            try:
                reel = str(r.get('is_reel', '')).strip().lower() in ('1', 'true', 'yes')
            except Exception:
                continue
            if reel != is_reel:
                continue
            d = fmt(r.get('date'))
            if not d or d < cutoff:
                continue
            try:
                v = int(float(r['views'] or 0))
            except Exception:
                continue
            vals.append(v)
            dates.append(d)
        label = 'reels' if is_reel else 'statics'
        if vals:
            print(f'{acct} {label}: n={len(vals)} median={statistics.median(vals)} maxdate={max(dates)}')

# themes for last 30d, drey reels only, quick sanity on lane medians
from collections import defaultdict
for acct in ('drey_ig', 'kevin_ig'):
    bytheme = defaultdict(list)
    for r in rows:
        if r['account'] != acct:
            continue
        d = fmt(r.get('date'))
        if not d or d < cutoff:
            continue
        try:
            v = int(float(r['views'] or 0))
        except Exception:
            continue
        bytheme[r.get('theme') or '?'].append(v)
    tops = sorted(((statistics.median(v), len(v), k) for k, v in bytheme.items() if len(v) >= 2), reverse=True)[:6]
    print(acct, 'theme medians (30d):', [(k, int(m), n) for m, n, k in tops])
