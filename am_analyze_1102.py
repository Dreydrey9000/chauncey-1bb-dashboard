#!/usr/bin/env python3
"""Full analysis for morning brief 2026-11-02."""
import json, datetime

RAW = json.load(open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/raw/morning_2026-11-02.json'))
ACC = {'drey': '6a1c7e1e2b2567671a7f25ee', 'kevin': '6a1c97b22b2567671a7ff845'}
today = datetime.date(2026, 11, 2)
yday = (today - datetime.timedelta(days=1)).isoformat()

summary = {}
for name in ('drey', 'kevin'):
    d = json.loads(RAW[f'{name}_daily_raw']['body'])
    days = {row['date']: row for row in d['dailyData']}
    out = {'days': {}}
    for date, row in sorted(days.items()):
        m = row['metrics']
        inter = m['likes'] + m['comments'] + m['shares'] + m['saves']
        out['days'][date] = {
            'posts': row['postCount'], 'reach': m['reach'], 'impressions': m['impressions'],
            'likes': m['likes'], 'comments': m['comments'], 'shares': m['shares'], 'saves': m['saves'],
            'clicks': m['clicks'], 'interactions': inter,
            'eng_rate': round(inter / m['reach'], 4) if m['reach'] else None,
        }
    # WoW: last 7 days (10-27..11-02) vs prior 7 (10-20..10-26)
    def window(a, b):
        rows = [out['days'][k] for k in out['days'] if a <= k <= b]
        return (sum(r['reach'] for r in rows), sum(r['interactions'] for r in rows),
                sum(r['posts'] for r in rows), sum(r['impressions'] for r in rows))
    r1, i1, p1, m1 = window('2026-10-27', '2026-11-02')
    r0, i0, p0, m0 = window('2026-10-20', '2026-10-26')
    out['wow'] = {
        'this': {'reach': r1, 'inter': i1, 'posts': p1, 'impr': m1,
                 'dates': 'Oct 27-Nov 2'},
        'prev': {'reach': r0, 'inter': i0, 'posts': p0, 'impr': m0,
                 'dates': 'Oct 20-26'},
        'reach_pct': round((r1 - r0) / r0 * 100, 1) if r0 else None,
        'inter_pct': round((i1 - i0) / i0 * 100, 1) if i0 else None,
    }
    out['yesterday'] = out['days'].get(yday)
    out['yesterday_date'] = yday
    summary[name] = out

# follower stats structure probe
fs = json.loads(RAW['drey_followers_raw']['body'])
print('FOLLOWER keys:', list(fs.keys()) if isinstance(fs, dict) else type(fs))
s = json.dumps(fs)
print('sample:', s[:800])

with open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/raw/am_summary_1102.json', 'w') as f:
    json.dump(summary, f, indent=1)

for name in ('drey', 'kevin'):
    o = summary[name]
    print(f"\n== {name} ==")
    print('yesterday', o['yesterday_date'], o['yesterday'])
    w = o['wow']
    print(f"WoW reach {w['this']['reach']} vs {w['prev']['reach']} ({w['reach_pct']}%) | inter {w['this']['inter']} vs {w['prev']['inter']} ({w['inter_pct']}%) | posts {w['this']['posts']} vs {w['prev']['posts']}")
