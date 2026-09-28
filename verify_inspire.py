#!/usr/bin/env python3
"""Verify live deploy of inspire.js: HTTP status + today's date marker on Cloudflare Pages."""
import urllib.request, time

url = 'https://1bb-dashboard.pages.dev/inspire.js'
markers = ['2026-09-28 (PM)', 'DdXVicFBYb1', 'Dd1dXMMgS_a']
for attempt in range(1, 4):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'})
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read().decode('utf-8', 'replace')
            print('HTTP', r.status, '| bytes:', len(body))
            for m in markers:
                print(f'marker "{m}" present:', m in body)
            break
    except Exception as e:
        print(f'attempt {attempt} failed: {e}')
        time.sleep(20)
