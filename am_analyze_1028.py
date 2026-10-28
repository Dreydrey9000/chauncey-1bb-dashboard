#!/usr/bin/env python3
"""AM 2026-10-28: founder own-data analysis for the morning inspire brief."""
import csv, statistics as st
from collections import defaultdict

CSV = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv'
rows = []
for r in csv.DictReader(open(CSV)):
    try:
        r['views_n'] = int(float(r['views'] or 0))
    except ValueError:
        r['views_n'] = 0
    try:
        r['comments_n'] = int(float(r['comments'] or 0))
    except ValueError:
        r['comments_n'] = 0
    try:
        r['likes_n'] = int(float(r['likes'] or 0))
    except ValueError:
        r['likes_n'] = 0
    r['is_reel_b'] = str(r.get('is_reel', '')).strip().lower() == 'true'
    rows.append(r)

for acct in ('drey_ig', 'kevin_ig'):
    sub = sorted([r for r in rows if r['account'] == acct], key=lambda r: r['ts'])
    reels = [r for r in sub if r['is_reel_b']]
    statics = [r for r in sub if not r['is_reel_b']]
    rmed = st.median([r['views_n'] for r in reels]) if reels else 0
    smed = st.median([r['views_n'] for r in statics]) if statics else 0
    print(f"\n===== {acct} (n={len(sub)}: {len(reels)} reels, {len(statics)} statics) =====")
    print(f"medians: reel={rmed}  static={smed}")
    # theme medians
    th = defaultdict(list)
    for r in sub:
        th[r['theme']].append(r['views_n'])
    themed = sorted(((t, st.median(v), len(v)) for t, v in th.items()), key=lambda x: -x[1])
    print("theme medians:", ', '.join(f"{t}={m}(n={n})" for t, m, n in themed[:6]))
    print("--- last 12 posts ---")
    for r in sub[-12:]:
        kind = 'REEL' if r['is_reel_b'] else 'STAT'
        print(f"{r['ts'][:16]} {kind:4} {r['theme'][:12]:12} v={r['views_n']:>6} l={r['likes_n']:>4} c={r['comments_n']:>3} {r['url']}")
        print(f"    {r['content'][:100]}")
    # comment drought check
    last10 = sub[-10:]
    zeroc = sum(1 for r in last10 if r['comments_n'] == 0)
    print(f"zero-comment posts in last 10: {zeroc}")
    # posts since yesterday evening pull (2026-10-27 22:00 UTC ~ 6p ET)
    fresh = [r for r in sub if r['ts'] >= '2026-10-27T22:00']
    print(f"posts since 10-27 6p ET: {len(fresh)}")
    for r in fresh:
        print(f"  FRESH {r['ts'][:16]} {'REEL' if r['is_reel_b'] else 'STAT'} v={r['views_n']} l={r['likes_n']} c={r['comments_n']} {r['url']} :: {r['content'][:80]}")
    # last 7 days reels vs statics
    wk = [r for r in sub if r['date'] >= '2026-10-21']
    wv_r = [r['views_n'] for r in wk if r['is_reel_b']]
    wv_s = [r['views_n'] for r in wk if not r['is_reel_b']]
    if wv_r: print(f"7d reels: n={len(wv_r)} med={st.median(wv_r)}")
    if wv_s: print(f"7d statics: n={len(wv_s)} med={st.median(wv_s)}")
