# Founder stats snapshot for inspire brief — reads posts_all.csv, prints verified numbers only
import csv, statistics as st
from collections import defaultdict
from datetime import datetime, timezone

rows = list(csv.DictReader(open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv')))

def num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None

for acct in ('drey_ig', 'kevin_ig'):
    sub = [r for r in rows if r['account'] == acct]
    sub.sort(key=lambda r: r['ts'], reverse=True)
    print('=' * 15, acct, f'n={len(sub)}', '=' * 15)
    print('-- latest 8 posts --')
    for r in sub[:8]:
        print(f"  {r['date']} reel={r['is_reel']} theme={r['theme']:<10} views={r['views']:>7} likes={r['likes']:>4} comments={r['comments']:>3} | {r['url']}")
        print(f"      {r['content'][:100].replace(chr(10),' ')}")
    views = [num(r['views']) for r in sub if num(r['views']) is not None]
    print(f'-- all-post views median: {st.median(views):,.0f} (n={len(views)}) mean={st.mean(views):,.0f}')
    for label, filt in [
        ('reels', lambda r: r['is_reel'] == 'True'),
        ('statics', lambda r: r['is_reel'] == 'False'),
    ]:
        v = [num(r['views']) for r in sub if filt(r) and num(r['views']) is not None]
        if v:
            print(f'-- {label} median: {st.median(v):,.0f} (n={len(v)})')
    themes = defaultdict(list)
    for r in sub:
        vv = num(r['views'])
        if vv is not None:
            themes[r['theme']].append(vv)
    for t, v in sorted(themes.items(), key=lambda kv: -st.median(kv[1])):
        print(f'-- theme {t:<12} median={st.median(v):>8,.0f} (n={len(v)})')
