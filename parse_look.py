#!/usr/bin/env python3
"""Parse TokScript lookalike pulls (read-only) for the PM inspire brief."""
import json, statistics

def load(p):
    t = open(p).read()
    d = json.loads(t.split('data: ', 1)[1])
    return json.loads(d['result']['content'][0]['text'])

for p, who in [('look_rowan.json', 'rowancheung'), ('look_bedros.json', 'bedroskeuilian')]:
    r = load(p)
    posts = r.get('posts', [])
    print(f"\n=== {who} status={r.get('status')} n={len(posts)} ===")
    views = [po['stats']['views'] for po in posts if po['stats']['views'] is not None]
    if views:
        print(f"median views={statistics.median(views):.0f}")
    for po in posts:
        s = po['stats']
        cap = (po['caption'] or '')[:90].replace(chr(10), ' / ')
        print(f"{po['timestamp'][:10]} {po['url']} views={s['views']} likes={s['likes']} comments={s['comments']} | {cap}")
