#!/usr/bin/env python3
"""Compare posts_all.csv (HEAD) vs HEAD~1 — biggest per-post view movers + new posts."""
import csv, io, subprocess

BASE = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard'

def git_csv(rev):
    src = subprocess.run(['git', '-C', BASE, 'show', f'{rev}:posts_all.csv'],
                         capture_output=True, text=True, check=True).stdout
    return list(csv.DictReader(io.StringIO(src)))

prev, cur = git_csv('HEAD~1'), git_csv('HEAD')
print('DEBUG csv cols:', list(cur[0].keys()) if cur else 'empty')

def key(r):
    return (r.get('platform') or r.get('account') or '?', r.get('id') or r.get('post_id') or r.get('url') or r.get('permalink') or '')

pv = {key(r): r for r in prev}
cv = {key(r): r for r in cur}

def views(r):
    for c in ('views', 'view_count', 'viewCount', 'ig_play_count', 'play_count'):
        if r.get(c) not in (None, '', 'None'):
            try:
                return float(r[c])
            except ValueError:
                pass
    return None

new = [k for k in cv if k not in pv]
print(f'NEW POSTS: {len(new)}')
for k in new:
    r = cv[k]
    print(f'  NEW {k[0]} views={views(r)} date={r.get("date") or r.get("ts") or r.get("created")!s:.10s} cap="{(r.get("caption") or r.get("content") or "")[:50]}"')

movers = []
for k, r in cv.items():
    if k in pv:
        a, b = views(pv[k]), views(r)
        if a is not None and b is not None and b != a:
            movers.append((b - a, k, a, b, (r.get('caption') or r.get('content') or '')[:45]))
movers.sort(reverse=True)
for d, k, a, b, cap in movers[:5]:
    print(f'MOVER {k[0]} {k[1][:24]}: {int(a)} -> {int(b)} ({int(d):+d}) "{cap}"')
if not movers:
    print('MOVERS: none (no view changes on existing posts)')
