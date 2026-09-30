#!/usr/bin/env python3
"""Print latest follower counts per account from raw/followers.json."""
import json, ast, os

BASE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(BASE, 'raw', 'followers.json')))

def unwrap(o):
    if isinstance(o, dict) and isinstance(o.get('result'), str):
        try:
            return ast.literal_eval(o['result'])
        except Exception:
            return o['result']
    return o

u = unwrap(d)
accts = u.get('accounts', u if isinstance(u, list) else [])
for a in accts:
    if isinstance(a, dict):
        latest = a.get('followers') or a.get('followerCount') or a.get('currentFollowers')
        # fall back: newest dated point
        if latest is None:
            pts = {}
            for kk in ('followerStats', 'followerHistory', 'stats', 'history', 'data'):
                v = a.get(kk)
                if isinstance(v, list):
                    for pt in v:
                        if isinstance(pt, dict):
                            dd = pt.get('date') or pt.get('day')
                            nn = pt.get('followers') or pt.get('count') or pt.get('value')
                            if dd and isinstance(nn, (int, float)):
                                pts[str(dd)[:10]] = nn
                    if pts:
                        break
            latest = pts[max(pts)] if pts else 'unavailable'
        print(a.get('username') or a.get('_id'), '| latest followers:', latest)
