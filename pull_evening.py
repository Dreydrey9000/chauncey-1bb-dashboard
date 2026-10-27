#!/usr/bin/env python3
"""Evening check pull: Zernio analytics/daily-metrics for both founder IGs.
Window: 4 days ago -> today, attribution=received. Saves raw + prints table."""
import json, urllib.request, urllib.error, datetime

KEY = json.load(open('/Users/andrethomas/.zernio/config.json'))['apiKey']
OUT = '/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/raw/evening_daily_2026-10-27.json'

ACCOUNTS = [
    ('drey_ig', '6a1c7e1e2b2567671a7f25ee'),
    ('kevin_ig', '6a1c97b22b2567671a7ff845'),
]
FROM, TO = '2026-10-23', '2026-10-27'

def get(url):
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {KEY}'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())

payload = {}
for key, acc in ACCOUNTS:
    url = (f'https://getlate.dev/api/v1/analytics/daily-metrics?platform=instagram'
           f'&accountId={acc}&fromDate={FROM}&toDate={TO}&attribution=received')
    payload[key] = get(url)

with open(OUT, 'w') as f:
    json.dump(payload, f, indent=1)

for key, data in payload.items():
    print(f'=== {key} ===')
    for d in data.get('dailyData', []):
        m = d.get('metrics', {})
        inter = (m.get('likes', 0) or 0) + (m.get('comments', 0) or 0) + \
                (m.get('shares', 0) or 0) + (m.get('saves', 0) or 0)
        reach = m.get('reach', 0) or 0
        er = (inter / reach * 100) if reach else None
        print(f"{d['date']} posts={d.get('postCount')} reach={reach} "
              f"likes={m.get('likes')} comments={m.get('comments')} "
              f"shares={m.get('shares')} saves={m.get('saves')} "
              f"views={m.get('views')} clicks={m.get('clicks')} "
              f"inter={inter} ER={'%.1f%%' % er if er is not None else 'n/a'}")
    print()
