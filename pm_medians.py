#!/usr/bin/env python3
"""Evening medians from posts_all.csv (per founder x theme, IG only, reels vs statics)."""
import csv, statistics, collections

BASE = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard'

def load():
    rows = []
    with open(f'{BASE}/posts_all.csv') as f:
        for r in csv.DictReader(f):
            try:
                v = int(float(r['views'] or 0))
            except Exception:
                continue
            rows.append({'account': r['account'], 'date': r['date'], 'views': v,
                         'is_reel': r.get('is_reel') == 'True', 'theme': r.get('theme') or 'none',
                         'url': r['url'], 'content': r['content'][:80]})
    return rows

rows = load()
for acc in ('drey_ig', 'kevin_ig'):
    sub = [r for r in rows if r['account'] == acc]
    def med(label, rs):
        if rs:
            print(f'  {label}: n={len(rs)} median={statistics.median([x["views"] for x in rs]):,.0f}')
        else:
            print(f'  {label}: n=0')
    print(f'== {acc} (n={len(sub)})')
    med('all', sub)
    med('reels', [r for r in sub if r['is_reel']])
    med('statics', [r for r in sub if not r['is_reel']])
    for theme, trs in sorted(collections.defaultdict(list, {t: [r for r in sub if r['theme'] == t] for t in {r['theme'] for r in sub}}).items(), key=lambda kv: -len(kv[1])):
        med(f'theme {theme}', trs)
    print()

print('== posts dated 2026-10-19 (from this morning 6:30a refresh)')
for r in rows:
    if r['date'] == '2026-10-19':
        print(f"  {r['account']} reel={r['is_reel']} views={r['views']:,} theme={r['theme']} | {r['url']} | {r['content']}")
print('== posts dated 2026-10-18, for completeness')
for r in rows:
    if r['date'] == '2026-10-18':
        print(f"  {r['account']} reel={r['is_reel']} views={r['views']:,} theme={r['theme']} | {r['url']} | {r['content']}")
