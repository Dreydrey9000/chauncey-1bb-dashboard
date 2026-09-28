#!/usr/bin/env python3
"""Verify live deploy: HTTP status + freshness marker of data.js on Cloudflare Pages."""
import urllib.request, time

url = 'https://1bb-dashboard.pages.dev/data.js'
for attempt in range(1, 4):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'})
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read().decode('utf-8', 'replace')
            print('HTTP', r.status, '| bytes:', len(body))
            print('fresh marker present:', '"2026-09-28 06:32AM ET"' in body)
            print('head:', body[:100].replace('\n', ' '))
            break
    except Exception as e:
        print(f'attempt {attempt} failed: {e}')
        time.sleep(20)
