#!/usr/bin/env python3
"""Kevin reel completion median, last 60d, from posts_all.csv."""
import csv, statistics, datetime, os
BASE = os.path.dirname(os.path.abspath(__file__))
cutoff = (datetime.date.today() - datetime.timedelta(days=60)).isoformat()
comps = []
with open(os.path.join(BASE, 'posts_all.csv')) as f:
    for r in csv.DictReader(f):
        if r['account'] == 'kevin_ig' and r['is_reel'] == 'True' and r['date'] >= cutoff:
            try:
                wm = float(r['watch_ms'] or 0)
                dur = float(r['dur_s'] or 0)
                if wm > 0 and dur > 0:
                    comps.append(min(wm / (dur * 1000), 1.0) * 100)
            except Exception:
                pass
print(f'kevin reel completion: n={len(comps)} median={statistics.median(comps):.1f}%')
