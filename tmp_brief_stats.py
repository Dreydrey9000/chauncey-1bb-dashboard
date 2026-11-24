# AM brief stats: medians for founder lanes from posts_all.csv (cron-safe: file, not heredoc)
import csv, statistics as st
from collections import defaultdict

rows = []
with open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv', newline='', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        rows.append(r)

def num(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None

# Window: last 30 days = 2026-10-25..2026-11-24; 14-day = 2026-11-10..2026-11-24
def in_win(r, start):
    return r['date'] >= start

for acct in ('drey_ig', 'kevin_ig'):
    print('=' * 12, acct, '=' * 12)
    for start, label in (('2026-10-25', '30d'), ('2026-11-10', '14d')):
        sub = [r for r in rows if r['account'] == acct and in_win(r, start) and r['theme'] != 'other' or (r['account'] == acct and in_win(r, start) and r['theme'] == 'other' and False)]
        # fix: keep it simple, recompute below
    themes = defaultdict(list)
    reels30 = []
    stats30 = []
    for r in rows:
        if r['account'] != acct or not in_win(r, '2026-10-25'):
            continue
        v = num(r['views'])
        if v is None:
            continue
        is_reel = r['is_reel'] == 'True'
        if is_reel:
            reels30.append(v)
        else:
            stats30.append(v)
        if r['theme'] != 'other':
            themes[r['theme']].append(v)
    print(f"30d: reels n={len(reels30)} median={st.median(reels30) if reels30 else 'NA'} | statics n={len(stats30)} median={st.median(stats30) if stats30 else 'NA'}")
    for t, vs in sorted(themes.items(), key=lambda kv: -st.median(kv[1])):
        print(f"  theme {t}: n={len(vs)} median={st.median(vs)} max={max(vs)}")
    # recent per-post log, last 8 non-story posts (stories have empty content)
    print('  last 8 feed posts (date | reel? | theme | views | comments | likes):')
    feed = [r for r in rows if r['account'] == acct and r['content'].strip()][-8:]
    for r in reversed(feed):
        print(f"    {r['date']} {'REEL ' if r['is_reel']=='True' else 'STAT '} {r['theme']:12s} views={r['views']:>6} com={r['comments']:>3} likes={r['likes']:>4}")
    # AI-lane streak for drey
    if acct == 'drey_ig':
        ai = [r for r in rows if r['account'] == acct and r['theme'] == 'ai_systems' and r['is_reel'] == 'True' and r['date'] >= '2026-11-10']
        ai_v = [num(r['views']) for r in ai if num(r['views']) is not None]
        if ai_v:
            print(f"  AI-lane reels 14d: n={len(ai_v)} median={st.median(ai_v)} max={max(ai_v)} under250={sum(1 for v in ai_v if v < 250)}")
        coms = [num(r['comments']) for r in ai if num(r['comments']) is not None]
        if coms:
            print(f"  AI-lane comments 14d: total={sum(coms)}, nonzero={sum(1 for c in coms if c and c > 0)}/{len(coms)}")
    if acct == 'kevin_ig':
        reels_sorted = sorted(reels30, reverse=True)
        print(f"  top reels 30d: {reels_sorted[:5]}")
        st_sorted = sorted(stats30, reverse=True)
        print(f"  top statics 30d: {st_sorted[:5]}")
print()
print('newest post date in csv:', max(r['date'] for r in rows))
