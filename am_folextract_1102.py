#!/usr/bin/env python3
"""Extract follower series for Drey + Kevin from the 2026-11-02 pull."""
import json

RAW = json.load(open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/raw/morning_2026-11-02.json'))
fs = json.loads(RAW['drey_followers_raw']['body'])  # same payload covers both
ACC = {'drey': '6a1c7e1e2b2567671a7f25ee', 'kevin': '6a1c97b22b2567671a7ff845'}
stats = fs['stats']
unames = {a['_id']: a.get('username') for a in fs['accounts']}

out = {}
for name, acc in ACC.items():
    series = stats.get(acc)
    if not series:
        print(name, acc, 'NO SERIES')
        continue
    first, last = series[0], series[-1]
    delta = last['followers'] - first['followers']
    out[name] = {'series': series, 'first': first, 'last': last, 'delta': delta,
                 'username': unames.get(acc)}
    print(f"{name} @{unames.get(acc)}: {first['date']} {first['followers']} -> "
          f"{last['date']} {last['followers']} = {delta:+d}")

with open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/raw/am_followers_1102.json', 'w') as f:
    json.dump(out, f, indent=1)
