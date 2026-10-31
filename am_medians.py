# AM inspire medians: 7-day per-account/type medians + CSV freshness (cron-safe, file-based)
import csv, statistics, datetime, os
from collections import defaultdict

BASE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(BASE, 'posts_all.csv'))))
latest = defaultdict(str)
for r in rows:
    if r['date'] > latest[r['account']]:
        latest[r['account']] = r['date']
print('CSV rows:', len(rows))
print('latest date per account:', dict(latest))

cutoff = (datetime.date(2026, 10, 31) - datetime.timedelta(days=7)).isoformat()
print('7d cutoff:', cutoff)
for acct in ('drey_ig', 'kevin_ig'):
    for kind in ('reel', 'static'):
        vals = []
        for r in rows:
            flag = (r.get('is_reel') or '').strip().lower()
            is_reel = flag in ('true', '1', '1.0')
            if r['account'] == acct and ((kind == 'reel') == is_reel) and r['date'] >= cutoff and r.get('views'):
                try:
                    vals.append(int(float(r['views'])))
                except ValueError:
                    pass
        if vals:
            print(f'{acct} {kind} 7d: n={len(vals)} median={statistics.median(vals)} values={sorted(vals)}')
# last 10 per founder for context
for acct in ('drey_ig', 'kevin_ig'):
    sub = sorted([r for r in rows if r['account'] == acct], key=lambda r: r['date'])[-10:]
    print(f'--- {acct} last 10:')
    for r in sub:
        print(' ', r['date'], 'reel' if (r.get('is_reel') or '').strip().lower() in ('true', '1', '1.0') else 'static', r['views'], (r.get('content') or '')[:55].replace('\n', ' '))
