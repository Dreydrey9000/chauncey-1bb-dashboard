#!/usr/bin/env python3
"""Supplemental: Kevin statics vs reels by window; Kevin Sunday history; verify format split."""
import csv, datetime, statistics

BASE = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard'
ET = datetime.timezone(datetime.timedelta(hours=-5))
rows = list(csv.DictReader(open(f'{BASE}/posts_all.csv')))

def toint(x):
    try:
        return int(float(x))
    except (TypeError, ValueError):
        return None

def parse_ts(ts):
    try:
        return datetime.datetime.fromisoformat(ts.replace('Z', '+00:00'))
    except Exception:
        return None

def is_story(u):
    u = (u or '').lower()
    return '/stories/' in u or '/s/' in u

now = datetime.datetime.now(datetime.timezone.utc)

def kev(fmt, days, theme=None):
    vals = []
    for r in rows:
        if r['account'] != 'kevin_ig' or is_story(r['url']):
            continue
        reel = r['url'].lower().find('/reel/') >= 0
        if fmt == 'reel' and not reel: continue
        if fmt == 'static' and reel: continue
        if theme and r.get('theme') != theme: continue
        ts = parse_ts(r['ts'])
        if ts and ts >= now - datetime.timedelta(days=days):
            v = toint(r['views'])
            if v is not None: vals.append(v)
    return (statistics.median(vals), len(vals)) if vals else (None, 0)

print('KEVIN reels vs statics:')
for days in (14, 30):
    mr, nr = kev('reel', days)
    ms, ns = kev('static', days)
    print(f'  {days}d: reels median={mr} (n={nr}) | statics median={ms} (n={ns})')
for t in ('identity', 'room', 'discipline', 'confession'):
    ms, ns = kev('static', 30, t)
    mr, nr = kev('reel', 30, t)
    print(f'  30d theme={t}: statics median={ms} (n={ns}) | reels median={mr} (n={nr})')

print()
print('KEVIN posts by weekday (30d, permanent posts):')
import collections
bywd = collections.defaultdict(list)
for r in rows:
    if r['account'] != 'kevin_ig' or is_story(r['url']): continue
    ts = parse_ts(r['ts'])
    if ts and ts >= now - datetime.timedelta(days=30):
        bywd[ts.astimezone(ET).strftime('%a')].append(toint(r['views']))
for wd in ('Mon','Tue','Wed','Thu','Fri','Sat','Sun'):
    v = [x for x in bywd.get(wd, []) if x is not None]
    if v:
        print(f'  {wd}: n={len(v)} median={statistics.median(v)} max={max(v)}')

print()
print('KEVIN Sunday posts, last 5 (date, ET time, views, kind):')
sun = []
for r in rows:
    if r['account'] != 'kevin_ig' or is_story(r['url']): continue
    ts = parse_ts(r['ts'])
    if ts and ts.astimezone(ET).weekday() == 6:
        sun.append((ts.astimezone(ET), toint(r['views']), 'reel' if '/reel/' in r['url'].lower() else 'static', r.get('theme')))
sun.sort()
for ts, v, k, t in sun[-5:]:
    print(f'  {ts.date()} {ts.strftime("%H:%M")} ET | {k} | views={v} | {t}')

print()
print('DREY room reels all-time (date, ET time, views) — verify winning window:')
rooms = []
for r in rows:
    if r['account'] != 'drey_ig' or is_story(r['url']): continue
    if r.get('theme') != 'room': continue
    ts = parse_ts(r['ts'])
    if ts: rooms.append((ts.astimezone(ET), toint(r['views'])))
rooms.sort()
for ts, v in rooms:
    print(f'  {ts.date()} {ts.strftime("%H:%M")} ET | views={v}')
