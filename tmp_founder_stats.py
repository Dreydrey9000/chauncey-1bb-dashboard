# Morning brief founder-stats anchor (run by inspire-brief AM)
import csv, statistics, datetime, json

rows = list(csv.DictReader(open('posts_all.csv')))

def num(x):
    try:
        return int(float(str(x))) if str(x).strip() not in ('', 'None') else None
    except ValueError:
        return None

for acct in ('drey_ig', 'kclavier_ig') if False else ('drey_ig', 'kevin_ig'):
    sub = [r for r in rows if r['account'] == acct]
    print('=' * 15, acct, f'n={len(sub)}', '=' * 15)
    withv = [r for r in sub if num(r['views'])]
    reels = [r for r in withv if r['is_reel'].strip().lower() == 'true']
    statics = [r for r in withv if r['is_reel'].strip().lower() != 'true']
    if withv:
        print('  ALL median views:', statistics.median(num(r['views']) for r in withv))
    if reels:
        print(f'  REELS median views (n={len(reels)}):', statistics.median(num(r['views']) for r in reels))
    if statics:
        print(f'  STATICS median views (n={len(statics)}):', statistics.median(num(r['views']) for r in statics))
    themes = {}
    for r in withv:
        themes.setdefault(r['theme'], []).append(num(r['views']))
    tm = [(t, statistics.median(v), len(v)) for t, v in themes.items() if v]
    for t, m, n in sorted(tm, key=lambda x: -x[1]):
        print(f'    theme {t}: median {m} (n={n})')
    sub_sorted = sorted(sub, key=lambda r: r['ts'], reverse=True)
    print('  -- latest 6 posts --')
    for r in sub_sorted[:6]:
        print(f"    {r['ts'][:16]} | reel={r['is_reel']} | views={r['views']} | theme={r['theme']} | {r['url']}")
        print(f"      {str(r['content'])[:100].replace(chr(10), ' ')}")
