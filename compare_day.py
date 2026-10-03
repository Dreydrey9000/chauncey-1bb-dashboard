#!/usr/bin/env python3
"""Compare follower counts + key stats between yesterday's and today's data.js."""
import json, re, subprocess

def load(spec):
    txt = subprocess.run(['git', 'show', spec], capture_output=True, text=True,
                         cwd='/Users/andrethomas/.hermes/workspaces/chauncey/dashboard').stdout
    m = re.search(r'window\.DATA = (\{.*\})', txt, re.S)
    return json.loads(m.group(1))

old = load('HEAD~1:site/data.js')
new = open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/site/data.js').read()
new = json.loads(re.search(r'window\.DATA = (\{.*\})', new, re.S).group(1))

def fol(d, name):
    f = d.get('followers', {}).get(name) or {}
    return f.get('current')

print('generated:', old.get('generated'), '->', new.get('generated'))
for name in ('drey', 'kevin', 'club'):
    o, n = fol(old, name), fol(new, name)
    if o is not None and n is not None:
        print(f'{name}_ig followers: {o} -> {n} ({n-o:+d})')
    else:
        print(f'{name}_ig followers: unavailable (old={o}, new={n})')

for k in ('drey_ig', 'drey_tt', 'kevin_ig', 'kevin_tt', 'club_ig'):
    o, n = old.get(k) or {}, new.get(k) or {}
    print(f"{k}: posts {o.get('posts')}->{n.get('posts')} | medianViews {o.get('medianViews')}->{n.get('medianViews')} | maxViews {o.get('maxViews')}->{n.get('maxViews')}")

def folcur(d, key):
    f = d.get(key)
    if isinstance(f, list):
        return f[-1][1] if f else None
    return (f or {}).get('current')

for key, label in (('dreyFollowers', 'drey_ig'), ('kevinFollowers', 'kevin_ig'), ('clubFollowers', 'club_ig')):
    o, n = folcur(old, key), folcur(new, key)
    if o is not None and n is not None:
        print(f'{label} followers: {o} -> {n} ({n-o:+d})')
    else:
        print(f'{label} followers: unavailable (old={o}, new={n})')

# top new post by views in last 2 days
posts = new.get('posts', [])
recent = [p for p in posts if str(p.get('date', '')) >= '2026-10-01']
recent.sort(key=lambda p: p.get('views') or 0, reverse=True)
for p in recent[:3]:
    print('recent top:', p.get('date'), p.get('key'), p.get('views'), 'views —', str(p.get('content'))[:60])
