#!/usr/bin/env python3
"""Print full day tables + alt WoW windows for the brief."""
import json

S = json.load(open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/raw/am_summary_1102.json'))
for name in ('drey', 'kevin'):
    print(f'== {name} ==')
    for d, r in S[name]['days'].items():
        er = f"{r['eng_rate']*100:.2f}%" if r['eng_rate'] is not None else 'n/a'
        print(f"  {d} posts={r['posts']} reach={r['reach']} impr={r['impressions']} "
              f"L{r['likes']} C{r['comments']} Sh{r['shares']} Sv{r['saves']} inter={r['interactions']} ER={er}")
    # alt window: complete days only (Oct 26-Nov 1 vs Oct 19-25)
    days = S[name]['days']
    def w(a, b):
        rows = [days[k] for k in days if a <= k <= b]
        return (sum(r['reach'] for r in rows), sum(r['interactions'] for r in rows), sum(r['posts'] for r in rows))
    r1, i1, p1 = w('2026-10-26', '2026-11-01')
    r0, i0, p0 = w('2026-10-19', '2026-10-25')
    print(f"  ALT WoW (10/26-11/1 vs 10/19-25): reach {r1} vs {r0} ({(r1-r0)/r0*100:+.1f}%) inter {i1} vs {i0} ({(i1-i0)/i0*100:+.1f}%) posts {p1} vs {p0}")
