#!/usr/bin/env python3
"""Summarize raw/followers.json — latest follower counts per account."""
import json, ast

raw = json.load(open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/raw/followers.json'))
res = raw.get('result', raw)
if isinstance(res, str):
    try:
        res = ast.literal_eval(res)
    except Exception:
        res = json.loads(res)

def summarize(o, path=''):
    if isinstance(o, dict):
        keys = {k.lower(): k for k in o}
        name = None
        for cand in ('accountusername', 'username', 'accountid', 'platform'):
            if cand in keys:
                name = o[keys[cand]]
                break
        for k, v in o.items():
            lk = k.lower()
            if 'follower' in lk and isinstance(v, (int, float)):
                print(f'{path} {name or ""} {k}={v}')
            elif lk in ('currentfollowers', 'followerscount', 'totalfollowers') :
                print(f'{path} {name or ""} {k}={v}')
        for k, v in o.items():
            if isinstance(v, (dict, list)):
                summarize(v, f'{path}/{k}')
    elif isinstance(o, list):
        for i, v in enumerate(o):
            summarize(v, f'{path}[{i}]')

summarize(res)
print('---raw keys---')
print(list(res.keys()) if isinstance(res, dict) else type(res))
