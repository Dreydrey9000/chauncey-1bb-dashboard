#!/usr/bin/env python3
"""One-off: compare latest two `data refresh` commits' data.js — followers + post-view movers.
Rev resolution: newest two commits matching 'data refresh' (robust to script-only commits on top)."""
import json, re, subprocess

BASE = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard'

def refresh_revs():
    """Return (current_rev, previous_rev) = newest two 'data refresh' commits."""
    log = subprocess.run(['git', '-C', BASE, 'log', '--format=%h %s', '--grep=^data refresh', '-n', '5'],
                         capture_output=True, text=True, check=True).stdout.strip().splitlines()
    revs = [l.split(' ', 1)[0] for l in log]
    if len(revs) < 2:
        raise SystemExit(f'need two data-refresh commits, found: {revs}')
    return revs[0], revs[1]

CUR_REV, PREV_REV = refresh_revs()
print(f'comparing {PREV_REV} (prev refresh) -> {CUR_REV} (current refresh)')

def git_file(rev, path):
    return subprocess.run(['git', '-C', BASE, 'show', f'{rev}:{path}'],
                          capture_output=True, text=True, check=True).stdout

def load_data(src):
    m = re.search(r'window\.DATA\s*=\s*(\{.*\})\s*;?\s*$', src, re.S)
    body = m.group(1) if m else src[src.index('{'):src.rindex('}') + 1]
    return json.loads(body)

prev = load_data(git_file(PREV_REV, 'site/data.js'))
cur = load_data(git_file(CUR_REV, 'site/data.js'))

def unwrap(o):
    if isinstance(o, dict) and isinstance(o.get('result'), str):
        import ast
        try:
            return ast.literal_eval(o['result'])
        except Exception:
            return o['result']
    return o

# followers
def series(o):
    out = {}
    accts = o.get('accounts', []) if isinstance(o, dict) else []
    for acc in accts:
        name = acc.get('username') or acc.get('_id')
        pts = {}
        for kk in ('followerStats', 'followerHistory', 'stats', 'history', 'data'):
            v = acc.get(kk)
            if isinstance(v, list):
                for pt in v:
                    if isinstance(pt, dict):
                        dd = pt.get('date') or pt.get('day')
                        nn = pt.get('followers') or pt.get('count') or pt.get('value')
                        if dd and isinstance(nn, (int, float)):
                            pts[str(dd)[:10]] = nn
                if pts:
                    break
        if not pts:
            cur_f = acc.get('currentFollowers') or acc.get('followers')
            if isinstance(cur_f, (int, float)):
                pts['latest'] = cur_f
        out[name] = pts
    return out

try:
    pf = unwrap(json.loads(git_file('HEAD~1', 'raw/followers.json')))
    cf = unwrap(json.loads(git_file('HEAD', 'raw/followers.json')))
    sp, sc = series(pf), series(cf)
    for name in sc:
        if name in sp and sp[name] and sc[name]:
            last_prev = sp[name][max(sp[name])]
            last_cur = sc[name][max(sc[name])]
            d = last_cur - last_prev
            print(f'FOLLOWERS {name}: {last_prev} -> {last_cur} ({d:+d})')
        else:
            print(f'FOLLOWERS {name}: prev unavailable')
except Exception as e:
    print('followers compare failed:', e)

# posts: views by platform+id
def post_map(data):
    out = {}
    posts = data.get('posts') or data.get('allPosts') or []
    if isinstance(posts, dict):
        for k, v in posts.items():
            if isinstance(v, list):
                for p in v:
                    out[(p.get('platform') or k, p.get('id') or p.get('postId'))] = p
    elif isinstance(posts, list):
        for p in posts:
            out[(p.get('platform') or p.get('account') or '?', p.get('id') or p.get('postId'))] = p
    return out

pp, pc = post_map(prev), post_map(cur)
movers = []
for k, p in pc.items():
    v = p.get('views') or p.get('viewCount') or (p.get('stats') or {}).get('views')
    q = pp.get(k)
    if q is not None and isinstance(v, (int, float)):
        pv = q.get('views') or q.get('viewCount') or (q.get('stats') or {}).get('views')
        if isinstance(pv, (int, float)) and v != pv:
            movers.append((v - pv, k, pv, v, (p.get('caption') or '')[:45]))
new_posts = [k for k in pc if k not in pp]
print(f'NEW POSTS today: {len(new_posts)}')
for k in new_posts:
    p = pc[k]
    v = p.get('views') or p.get('viewCount') or (p.get('stats') or {}).get('views')
    print(f'  NEW {k[0]} views={v} caption="{(p.get("caption") or "")[:45]}"')
movers.sort(reverse=True)
for d, k, a, b, cap in movers[:5]:
    print(f'MOVER {k[0]} {k[1]}: {a} -> {b} ({d:+d}) "{cap}"')
