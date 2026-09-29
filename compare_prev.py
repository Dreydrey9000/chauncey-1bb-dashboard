#!/usr/bin/env python3
"""Compare current data.js vs HEAD-committed version: follower + post-view movers."""
import json, re, subprocess, sys

BASE = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard'

def head_file(path):
    try:
        return subprocess.run(['git', '-C', BASE, 'show', f'HEAD:{path}'],
                              capture_output=True, text=True, check=True).stdout
    except subprocess.CalledProcessError:
        return None

def load_data(src):
    m = re.search(r'window\.DATA\s*=\s*(\{.*\})\s*;?\s*$', src, re.S)
    body = m.group(1) if m else src[src.index('{'):src.rindex('}') + 1]
    return json.loads(body)

prev_src = head_file('site/data.js')
if not prev_src:
    print('COMPARE: no previous data.js in git')
    sys.exit(0)

# followers.json raw comparison (handles REST dict or {"result": "<repr>"} wrap)
prev_f = head_file('raw/followers.json')


def unwrap(o):
    if isinstance(o, dict) and isinstance(o.get('result'), str):
        import ast
        try:
            return ast.literal_eval(o['result'])
        except Exception:
            try:
                return json.loads(o['result'])
            except Exception:
                return o['result']
    return o


if prev_f is not None:
    cur_f = open(f'{BASE}/raw/followers.json').read()
    same = json.dumps(json.loads(prev_f), sort_keys=True) == json.dumps(json.loads(cur_f), sort_keys=True)
    if same:
        print('followers.json: byte-identical to yesterday')
    else:
        a, b = unwrap(json.loads(prev_f)), unwrap(json.loads(cur_f))


        def series(o):
            """account -> {date: count} from any list-of-dicts shape."""
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
                                d = pt.get('date') or pt.get('day') or pt.get('timestamp')
                                n = pt.get('followers') or pt.get('count') or pt.get('value')
                                if d is not None and isinstance(n, (int, float)):
                                    pts[str(d)[:10]] = n
                        if pts:
                            break
                if not pts:
                    for kk in ('followers', 'followerCount', 'currentFollowers'):
                        if isinstance(acc.get(kk), (int, float)):
                            pts['latest'] = acc[kk]
                            break
                out[name] = pts
            return out


        sa, sb = series(a), series(b)
        for name in sorted(set(sa) & set(sb)):
            da, db = sa[name], sb[name]
            if not da or not db:
                continue
            la = da[max(da)] if da else None
            lb = db[max(db)] if db else None
            if isinstance(la, (int, float)) and isinstance(lb, (int, float)) and la != lb:
                print(f'FOLLOWER {name}: {la:.0f} -> {lb:.0f} ({lb-la:+.0f})')
        if all(sa.get(n) == sb.get(n) for n in sa):
            print('follower series: no count changes (diff was cosmetic, e.g. cache URLs)')

prev = load_data(prev_src)
cur = load_data(open(f'{BASE}/site/data.js').read())

pf, cf = prev.get('followers', {}), cur.get('followers', {})


def walk_flat(d, prefix=''):
    out = {}
    if isinstance(d, dict):
        for k, v in d.items():
            kk = f'{prefix}.{k}' if prefix else str(k)
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                out[kk] = v
            elif isinstance(v, dict):
                out.update(walk_flat(v, kk))
    return out


fp, fc = walk_flat(pf), walk_flat(cf)
moved = False
for k in sorted(set(fp) & set(fc)):
    if fp[k] != fc[k]:
        print(f'FOLLOWER {k}: {fp[k]:.0f} -> {fc[k]:.0f} ({fc[k]-fp[k]:+.0f})')
        moved = True
if pf != cf and not moved:
    print('FOLLOWER: structure changed, no simple numeric deltas')

pp = {p.get('id') or p.get('url') or p.get('permalink'): p for p in prev.get('posts', [])}
deltas = []
for p in cur.get('posts', []):
    pid = p.get('id') or p.get('url') or p.get('permalink')
    if pid in pp:
        v1, v2 = pp[pid].get('views'), p.get('views')
        if isinstance(v1, (int, float)) and isinstance(v2, (int, float)) and v2 != v1:
            deltas.append((v2 - v1, v2, (p.get('caption') or p.get('title') or '')[:70]))
deltas.sort(reverse=True)
for d, v2, cap in deltas[:5]:
    print(f'VIEW {d:+.0f} (now {v2:.0f}) | {cap}')
if not deltas:
    print('VIEW: no changed posts vs yesterday')
if not moved and not deltas:
    print('COMPARE: nothing moved vs yesterday')
