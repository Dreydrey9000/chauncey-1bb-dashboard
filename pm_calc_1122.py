#!/usr/bin/env python3
"""Evening 2026-11-22: beat/miss vs medians from posts_all.csv (through this morning's refresh)
plus fresh Zernio same-day numbers from raw/pm_delta_2026-11-22.json."""
import csv, json, statistics, datetime, collections

BASE = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard'
rows = []
with open(f'{BASE}/posts_all.csv') as f:
    for r in csv.DictReader(f):
        rows.append(r)

def toint(x):
    try:
        return int(float(x))
    except (TypeError, ValueError):
        return None

# --- Filter to permanent posts (exclude stories) using URL shape ---
def is_story(u):
    u = (u or '').lower()
    return '/stories/' in u or '/s/' in u

def parse_ts(ts):
    try:
        return datetime.datetime.fromisoformat(ts.replace('Z', '+00:00'))
    except Exception:
        return None

# Reels-only medians, last 14 days (reels are the compared format)
now = datetime.datetime.now(datetime.timezone.utc)
d14 = now - datetime.timedelta(days=14)
d30 = now - datetime.timedelta(days=30)

def reel_median(acct, lo, hi_days):
    vals = []
    for r in rows:
        if r['account'] != acct or is_story(r['url']):
            continue
        ts = parse_ts(r['ts'])
        if not ts:
            continue
        if lo <= ts <= now - datetime.timedelta(days=hi_days) if hi_days else lo <= ts:
            pass
        vals.append((ts, toint(r['views']), r.get('theme', ''), r.get('is_reel', '')))
    return vals

# simpler: last-14d reel medians overall
def med(acct, days=None, reel_only=True, theme=None):
    vals = []
    for r in rows:
        if r['account'] != acct:
            continue
        if reel_only and is_story(r['url']):
            continue
        if theme is not None and r.get('theme') != theme:
            continue
        ts = parse_ts(r['ts'])
        if days and ts and ts >= now - datetime.timedelta(days=days):
            vals.append(toint(r['views']))
        elif not days:
            vals.append(toint(r['views']))
    vals = [v for v in vals if v is not None]
    return statistics.median(vals) if vals else None, len(vals)

print('=== DREY reels (no stories), various windows ===')
for label, kw in [
    ('reels 14d', dict(acct='drey_ig', days=14)),
    ('reels 30d', dict(acct='drey_ig', days=30)),
    ('all posts 14d', dict(acct='drey_ig', days=14, reel_only=False)),
]:
    m, n = med(**kw)
    print(f'{label}: median={m} n={n}')

print()
print('=== Drey: room/confession theme vs ai_tool theme (30d, permanent posts) ===')
themes = collections.Counter(r.get('theme') for r in rows if r['account'] == 'drey_ig')
print('theme counts (all time in csv):', dict(themes))
for t in ('room', 'confession', 'ai_tool', 'ai_systems', 'identity'):
    m, n = med('drey_ig', days=30, theme=t, reel_only=False)
    m2, n2 = med('drey_ig', theme=t, reel_only=False)
    print(f'  theme={t!r}: 30d median={m} n={n} | all-time median={m2} n={n2}')

print()
print('=== KEVIN medians ===')
for label, kw in [
    ('reels 14d', dict(acct='kevin_ig', days=14)),
    ('reels 30d', dict(acct='kevin_ig', days=30)),
    ('statics 30d', dict(acct='kevin_ig', days=30, reel_only=False)),
]:
    m, n = med(**kw)
    print(f'{label}: median={m} n={n}')
for t in ('identity', 'room', 'discipline'):
    m, n = med('kevin_ig', days=30, theme=t, reel_only=False)
    print(f'  theme={t!r} 30d median={m} n={n}')

print()
print('=== DREY last 8 permanent posts (csv, for streak context) ===')
dre = [(parse_ts(r['ts']), r) for r in rows if r['account'] == 'drey_ig' and not is_story(r['url']) and parse_ts(r['ts'])]
dre.sort(key=lambda x: x[0])
for ts, r in dre[-8:]:
    print(f"  {ts.date()} {ts.astimezone(datetime.timezone(datetime.timedelta(hours=-5))).strftime('%H:%M')} ET | views={r['views']} | {r['url'].split('/')[4] if len(r['url'].split('/'))>4 else r['url'][:40]} | theme={r.get('theme')} | {r['content'][:60]!r}")

print()
print('=== KEVIN last 6 permanent posts (csv) ===')
kev = [(parse_ts(r['ts']), r) for r in rows if r['account'] == 'kevin_ig' and not is_story(r['url']) and parse_ts(r['ts'])]
kev.sort(key=lambda x: x[0])
for ts, r in kev[-6:]:
    print(f"  {ts.date()} {ts.astimezone(datetime.timezone(datetime.timedelta(hours=-5))).strftime('%H:%M')} ET | views={r['views']} | {r['url'].split('/')[4] if len(r['url'].split('/'))>4 else r['url'][:40]} | theme={r.get('theme')} | {r['content'][:60]!r}")

print()
print('=== Fresh Zernio same-day (2026-11-22) posts ===')
fresh = json.load(open(f'{BASE}/raw/pm_delta_2026-11-22.json'))['fresh']
for acct, posts in fresh.items():
    if isinstance(posts, dict) and 'error' in posts:
        print(acct, 'ERROR', posts['error']); continue
    for p in posts:
        ts = parse_ts(p['posted_at'])
        if ts and ts.date().isoformat() == '2026-11-22':
            et = ts.astimezone(datetime.timezone(datetime.timedelta(hours=-5)))
            print(f"  {acct} | {et.strftime('%H:%M')} ET | views={p['views']} | {p['url']}")
            print(f"    caption: {p['caption'][:100]!r}")
