# AM/PM brief stats: medians for founder lanes from posts_all.csv (cron-safe: file, not heredoc)
# Stories are EXCLUDED everywhere: they are is_reel=False with empty content and a /stories/ URL.
# (Fixed 2026-11-24: the old 'sub' filter had an operator-precedence bug and never filtered anything,
#  so feed-statics medians silently included stories. Verified against the ad-hoc recheck.)
import csv
import datetime
import statistics as st
from collections import defaultdict

CSV = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/posts_all.csv'


def is_story(r):
    return '/stories/' in r['url'] or not r['content'].strip()


def posts(acct):
    """[(views, row)] for FEED posts (stories excluded) with a numeric view count, oldest first."""
    out = []
    for r in csv.DictReader(open(CSV, newline='', encoding='utf-8')):
        if r['account'] != acct or is_story(r):
            continue
        try:
            out.append((float(r['views']), r))
        except (TypeError, ValueError):
            continue
    out.sort(key=lambda p: p[1]['ts'])
    return out


for acct in ('drey_ig', 'kevin_ig'):
    print('=' * 12, acct, '=' * 12)
    feed = posts(acct)
    feed30 = [p for p in feed if p[1]['date'] >= '2026-10-25']
    reels30 = [v for v, r in feed30 if r['is_reel'] == 'True']
    stats30 = [v for v, r in feed30 if r['is_reel'] == 'False']
    print(f"30d FEED ONLY: reels n={len(reels30)} median={st.median(reels30)} | statics n={len(stats30)} median={st.median(stats30)}")
    themes = defaultdict(list)
    for v, r in feed30:
        if r['theme'] != 'other':
            themes[r['theme']].append(v)
    for t, vs in sorted(themes.items(), key=lambda kv: -st.median(kv[1])):
        print(f"  theme {t}: n={len(vs)} median={st.median(vs)} max={max(vs)}")
    print('  last 8 feed posts (date | REEL/STAT | theme | views | comments | likes):')
    for v, r in feed[-8:]:
        print(f"    {r['date']} {'REEL ' if r['is_reel']=='True' else 'STAT '} {r['theme']:12s} views={v:>6.0f} com={r['comments']:>3} likes={r['likes']:>4}")
    if acct == 'drey_ig':
        ai14 = [v for v, r in feed30 if r['theme'] == 'ai_systems' and r['is_reel'] == 'True' and r['date'] >= '2026-11-10']
        print(f"  AI-lane reels 14d: n={len(ai14)} median={st.median(ai14)} max={max(ai14)} under500={sum(1 for v in ai14 if v < 500)}")
        since18 = [(v, r) for v, r in feed30 if r['theme'] == 'ai_systems' and r['is_reel'] == 'True' and r['date'] >= '2026-11-18']
        coms = [float(r['comments'] or 0) for _, r in since18]
        print(f"  AI-lane reels since Nov 18: n={len(coms)} views={sorted(v for v, _ in since18)} comments_total={sum(coms)}")
    if acct == 'kevin_ig':
        print(f"  top reels 30d: {sorted(reels30, reverse=True)[:5]}")
        print(f"  top statics 30d: {sorted(stats30, reverse=True)[:5]}")
        byday = defaultdict(list)
        for v, r in feed30:
            byday[datetime.date.fromisoformat(r['date']).strftime('%a')].append(v)
        print('  by-weekday medians: ' + ', '.join(f"{d}={st.median(vs):.0f}(n={len(vs)})" for d, vs in sorted(byday.items())))

newest = max(r['date'] for r in csv.DictReader(open(CSV, newline='', encoding='utf-8')))
print()
print('newest post date in csv:', newest)
