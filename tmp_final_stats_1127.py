#!/usr/bin/env python3
"""Final quoted-stat computations for PM brief 2026-11-27. Every number that
will appear in the brief prints here, computed from THIS run's data."""
import csv, statistics, json

BASE = "/Users/andrethomas/.hermes/workspaces/chauncey/dashboard"
TODAY = "2026-11-27"

with open(f"{BASE}/posts_all.csv", newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

def is_feed(r):
    return ('/stories/' not in (r.get('url') or '')) and bool((r.get('content') or '').strip())

def v(r):
    try:
        return float(r['views'])
    except (ValueError, TypeError):
        return None

def med(xs):
    ys = [x for x in xs if x is not None and x > 0]
    return (statistics.median(ys), len(ys)) if ys else (None, 0)

# 1) What is Kevin's 56,644 max post? (all-time #1 check)
kmax = max((r for r in rows if r['account'] == 'kevin_ig' and is_feed(r) and (v(r) or 0) > 0), key=lambda r: (v(r) or 0))
print('KEVIN CSV MAX:', kmax['date'], kmax['ts'], kmax['url'], 'views', kmax['views'], 'reel', kmax['is_reel'], 'theme', kmax['theme'])
print('  caption:', (kmax['content'] or '')[:150].replace('\n', ' '))

# fresh overlay for kevin top: room reel fresh = 7146
fresh = json.load(open(f"{BASE}/raw/pm_delta_{TODAY}.json"))['fresh']
fr = {p['url']: p for p in fresh['kevin_ig']}
room_fresh = fr.get('https://www.instagram.com/reel/DgIUQyCjMAT/')
print('KEVIN room reel fresh:', room_fresh['views'] if room_fresh else 'n/a', 'CSV 7055')

# 2) Kevin top-5 feed posts by views with fresh overlay
combined = []
for r in rows:
    if r['account'] == 'kevin_ig' and is_feed(r):
        vv = v(r) or 0
        if r['url'] in fr and fr[r['url']]['views'] is not None:
            vv = max(vv, float(fr[r['url']]['views']))
        combined.append((vv, r['date'], r['url'], r['is_reel'], r['theme']))
for c in sorted(combined, reverse=True)[:5]:
    print('KEVIN TOP5:', c)

# 3) Drey confession+room combined median (feed, views>0)
dr_cr = [v(r) for r in rows if r['account'] == 'drey_ig' and is_feed(r) and r['theme'] in ('confession', 'room') and (v(r) or 0) > 0]
print('DREY confession+room: n=%d median=%r' % (len(dr_cr), statistics.median(dr_cr)))

# 4) Drey last 20 feed posts slogan/comments incl. today's noon reel (fresh)
drey_feed = [r for r in rows if r['account'] == 'drey_ig' and is_feed(r)]
drey_recent = drey_feed[-19:]
noon = {'url': 'https://www.instagram.com/reel/DgQK_4Nox2Q/',
        'content': "Would you let AI watch your screen to get your time back? Follow for AI systems instead of hiring an employee.",
        'comments': 0}
slog = sum(1 for r in drey_recent if 'Follow for' in (r.get('content') or ''))
slog += 1 if 'Follow for' in noon['content'] else 0
coms = sum(float(r['comments'] or 0) for r in drey_recent) + noon['comments']
print('DREY last 20 feed posts: %d carry slogan, %.1f comments total' % (slog, coms))

# 5) Rowan: reels in last 10 days + comment median of last 9
rowan_pull = [
    ('2026-11-27', 17), ('2026-11-25', 13), ('2026-11-24', 20), ('2026-11-23', 40),
    ('2026-11-21', 48), ('2026-11-20', 5), ('2026-11-19', 34), ('2026-11-18', 69), ('2026-11-17', 13)]
n10 = sum(1 for d, _ in rowan_pull if d >= '2026-11-17')
c9 = [c for _, c in rowan_pull]
print('ROWAN: %d reels since 11-17 (10 days); comment median of last 9 = %r' % (n10, statistics.median(c9)))

# 6) Kevin statics/reels timing (re-verified)
def hour_et(r):
    try:
        return (int(r['ts'][11:13]) - 5) % 24
    except Exception:
        return None
kr37 = [v(r) for r in rows if r['account'] == 'kevin_ig' and is_feed(r) and r['is_reel'] == 'True' and (h := hour_et(r)) is not None and 15 <= h < 19 and (v(r) or 0) > 0]
kroth = [v(r) for r in rows if r['account'] == 'kevin_ig' and is_feed(r) and r['is_reel'] == 'True' and ((h := hour_et(r)) is None or not (15 <= h < 19)) and (v(r) or 0) > 0]
ks49 = [v(r) for r in rows if r['account'] == 'kevin_ig' and is_feed(r) and r['is_reel'] == 'False' and (h := hour_et(r)) is not None and 16 <= h < 21 and (v(r) or 0) > 0]
ksoth = [v(r) for r in rows if r['account'] == 'kevin_ig' and is_feed(r) and r['is_reel'] == 'False' and ((h := hour_et(r)) is None or not (16 <= h < 21)) and (v(r) or 0) > 0]
print('KEVIN reels 3-7p ET: n=%d median=%r | other: n=%d median=%r' % (len(kr37), statistics.median(kr37), len(kroth), statistics.median(kroth)))
print('KEVIN statics 4-9p ET: n=%d median=%r | other: n=%d median=%r' % (len(ks49), statistics.median(ks49), len(ksoth), statistics.median(ksoth)))

# 7) Kevin statics median and today's static age
print('KEVIN statics median: %r (n=%d)' % (statistics.median([v(r) for r in rows if r['account'] == 'kevin_ig' and is_feed(r) and r['is_reel'] == 'False' and (v(r) or 0) > 0]), len([r for r in rows if r['account'] == 'kevin_ig' and is_feed(r) and r['is_reel'] == 'False' and (v(r) or 0) > 0])))
k_today = [p for p in fresh['kevin_ig'] if p['url'] == 'https://www.instagram.com/p/DgP2IHuiHn7/'][0]
print('KEVIN today static:', k_today['views'], 'views', k_today['comments'], 'comments posted', k_today['posted_at'])

# 8) Kevin room theme median + drey medians re-verify
print('KEVIN room theme: %r' % statistics.median([v(r) for r in rows if r['account'] == 'kevin_ig' and is_feed(r) and r['theme'] == 'room' and (v(r) or 0) > 0]))
print('DREY all feed: %r | ai_systems: %r' % (statistics.median([v(r) for r in rows if r['account'] == 'drey_ig' and is_feed(r) and (v(r) or 0) > 0]), statistics.median([v(r) for r in rows if r['account'] == 'drey_ig' and is_feed(r) and r['theme'] == 'ai_systems' and (v(r) or 0) > 0])))

# 9) Meltzer yesterday count + Liam silence
print('LIAM last post: 2026-11-19 ->', (27 - 19), 'days silent as of today')
