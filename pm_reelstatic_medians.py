#!/usr/bin/env python3
"""Reel vs static medians from posts_all.csv via is_reel flag (evening beat/miss baseline)."""
import csv, statistics, os
BASE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(BASE, 'posts_all.csv'))))
for acct in ('drey_ig', 'kevin_ig'):
    reels, statics = [], []
    for r in rows:
        if r['account'] != acct or not r.get('views'):
            continue
        try:
            v = int(float(r['views']))
        except ValueError:
            continue
        flag = str(r.get('is_reel', '')).strip().lower()
        if flag in ('true', '1', 'yes'):
            reels.append(v)
        elif flag in ('false', '0', 'no', ''):
            statics.append(v)
    print('%s: reels median=%s (n=%d)  statics median=%s (n=%d)  is_reel values=%s' % (
        acct,
        statistics.median(reels) if reels else 'n/a', len(reels),
        statistics.median(statics) if statics else 'n/a', len(statics),
        sorted({str(r.get('is_reel')) for r in rows if r['account'] == acct})[:6]))
