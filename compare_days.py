# Compare yesterday's data.js (HEAD) with today's: biggest view mover + follower deltas.
import json, re

def load(path):
    s = open(path, encoding='utf-8').read()
    m = re.search(r'window\.DATA\s*=\s*(\{.*\})\s*;?\s*$', s, re.S)
    return json.loads(m.group(1) if m else s[s.index('{'):s.rindex('}') + 1])

prev = load('/tmp/data_prev.js')
cur = load('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/site/data.js')
ACCTS = ['drey_ig', 'drey_tt', 'kevin_ig', 'kevin_tt', 'club_ig']

def get_all(d, a):
    node = d.get(a) or {}
    return node.get('all') or []

movers, new_posts = [], []
for a in ACCTS:
    pi = {r.get('url'): r for r in get_all(prev, a)}
    for r in get_all(cur, a):
        k = r.get('url')
        if k not in pi:
            new_posts.append((a, r))
        else:
            d = (r.get('v') or 0) - (pi[k].get('v') or 0)
            if d:
                movers.append((d, a, r))

print('TOP VIEW MOVERS (delta since yesterday):')
for d, a, r in sorted(movers, key=lambda x: -x[0])[:6]:
    print(f"  {d:+7}  {a}  {str(r.get('d'))[:10]}  now={r.get('v'):>7}  {str(r.get('t') or '')[:55]!r}")

print('\nNEW POSTS since yesterday:', len(new_posts))
for a, r in new_posts:
    print(f"  {a}  {str(r.get('d'))[:16]}  v={r.get('v')}  {str(r.get('t') or '')[:55]!r}")

def last_trend(node):
    t = node.get('trend') if isinstance(node, dict) else node
    return t[-1] if t else (None, None)

print('\nFOLLOWERS (last trend point prev -> cur):')
for f, name in [('dreyFollowers', 'drey'), ('kevinFollowers', 'kevin'), ('clubFollowers', 'club')]:
    pd, pv = last_trend(prev.get(f) or {})
    cd, cv = last_trend(cur.get(f) or {})
    delta = (cv - pv) if (isinstance(pv, (int, float)) and isinstance(cv, (int, float))) else 'n/a'
    print(f"  {name}: {pd} {pv} -> {cd} {cv}  (delta {delta})")
