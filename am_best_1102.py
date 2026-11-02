#!/usr/bin/env python3
"""Extract best post per account from full per-post analytics."""
import json

R = json.load(open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/raw/am_postan_1102.json'))
for name in ('drey', 'kevin'):
    ranked = []
    for r in R[name]:
        an = (r.get('analytics') or {}).get('analytics') or {}
        imp = an.get('impressions') or 0
        inter = (an.get('likes') or 0) + (an.get('comments') or 0) + (an.get('shares') or 0) + (an.get('saves') or 0)
        ranked.append({'imp': imp, 'inter': inter, 'likes': an.get('likes'),
                       'comments': an.get('comments'), 'shares': an.get('shares'),
                       'saves': an.get('saves'), 'reach': an.get('reach'),
                       'url': r.get('url'), 'publishedAt': r.get('publishedAt'),
                       'caption': r.get('caption')})
    ranked.sort(key=lambda x: -x['imp'])
    print(f'== {name} ==')
    for x in ranked[:5]:
        print(f"  {str(x['publishedAt'])[:10]} impr={x['imp']} inter={x['inter']} "
              f"(L{x['likes']}/C{x['comments']}/Sh{x['shares']}/Sv{x['saves']}) | {x['caption'][:60]!r}")
    best = ranked[0]
    print(f"  BEST URL: {best['url']}")
    print(f"  BEST caption: {best['caption'][:200]!r}")
