#!/usr/bin/env python3
"""Evening analysis v2: correct columns (theme, is_reel), 30-day medians, comment baseline."""
import csv, statistics, datetime, os, collections

BASE = os.path.dirname(os.path.abspath(__file__))
rows = list(csv.DictReader(open(os.path.join(BASE, 'posts_all.csv'))))

def to_int(v):
    try:
        return int(float(v))
    except Exception:
        return None

cutoff = (datetime.date.today() - datetime.timedelta(days=30)).isoformat()
def in30(r):
    return (r.get('date') or '') >= cutoff

for acct in ('drey_ig', 'kevin_ig'):
    print(f'=== {acct} (last 30d, rows {cutoff}..)')
    sub = [r for r in rows if r.get('account') == acct and in30(r)]
    vs = [to_int(r['views']) for r in sub]
    vs = [v for v in vs if v is not None]
    print(f'  ALL: n={len(vs)} median={statistics.median(vs) if vs else "n/a"}')
    bytheme = collections.defaultdict(list)
    for r in sub:
        v = to_int(r['views'])
        if v is not None:
            bytheme[r.get('theme') or '?'].append(v)
    for t, tv in sorted(bytheme.items(), key=lambda kv: -statistics.median(kv[1])):
        print(f'  theme {t}: n={len(tv)} median={statistics.median(tv):.0f}')
    if acct == 'kevin_ig':
        for flag, label in (('1', 'reel'), ('0', 'static'), ('True', 'reel'), ('False', 'static')):
            tv = [to_int(r['views']) for r in sub if r.get('is_reel') == flag]
            tv = [v for v in tv if v is not None]
            if tv:
                print(f'  is_reel={flag} ({label}): n={len(tv)} median={statistics.median(tv):.0f}')
        com = [to_int(r['comments']) for r in sub]
        com = [c for c in com if c is not None]
        print(f'  comments: median={statistics.median(com) if com else "n/a"} max={max(com) if com else "n/a"}; posts with >=11 comments: {sum(1 for c in com if c >= 11)}')

# Drey recent openers: first 6 words of caption, with views — check the advice-frame streak
print('\n=== drey_ig last 12 reels (date, views, opener)')
sub = [r for r in rows if r.get('account') == 'drey_ig']
sub.sort(key=lambda r: r.get('date') or '', reverse=True)
for r in sub[:12]:
    opener = ' '.join(str(r.get('content') or '').split()[:7])
    print(f"  {r.get('date')} v={r.get('views'):>6} | {opener}")

# confession-open pair referenced this morning
print('\n=== drey_ig high-view posts (top 6 by views)')
for r in sub[:0]:
    pass
top = sorted([r for r in sub], key=lambda r: to_int(r['views']) or 0, reverse=True)[:6]
for r in top:
    print(f"  {r.get('date')} v={r.get('views'):>6} theme={r.get('theme')} | {' '.join(str(r.get('content') or '').split()[:10])}")

# Kevin recent posts for context
print('\n=== kevin_ig last 10 (date, views, comments, theme)')
ksub = [r for r in rows if r.get('account') == 'kevin_ig']
ksub.sort(key=lambda r: r.get('date') or '', reverse=True)
for r in ksub[:10]:
    print(f"  {r.get('date')} v={r.get('views'):>6} c={r.get('comments'):>3} {r.get('theme')} | {' '.join(str(r.get('content') or '').split()[:8])}")
