#!/usr/bin/env python3
"""Verify live deploy: HTTP status + freshness marker of data.js on Cloudflare Pages."""
import urllib.request, time, datetime

url = 'https://1bb-dashboard.pages.dev/data.js'
today = datetime.date.today().isoformat()
for attempt in range(1, 4):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'})
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read().decode('utf-8', 'replace')
            print('HTTP', r.status, '| bytes:', len(body))
            print('fresh (generated today', today + '):', f'"generated": "{today}' in body)
            print('head:', body[:100].replace('\n', ' '))
            break
    except Exception as e:
        print(f'attempt {attempt} failed: {e}')
        time.sleep(20)
