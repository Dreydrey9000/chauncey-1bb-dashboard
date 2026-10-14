#!/usr/bin/env python3
"""Cache-busting check for inspire.js deploy."""
import urllib.request, time

for suffix in ('', '?v=' + str(int(time.time()))):
    url = 'https://1bb-dashboard.pages.dev/inspire.js' + suffix
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'})
    with urllib.request.urlopen(req, timeout=30) as r:
        body = r.read().decode('utf-8', 'replace')
    print(f"suffix '{suffix}': HTTP {r.status} chars={len(body)} AM-marker={'2026-10-14 (AM)' in body} PM-marker={'2026-10-13 (PM)' in body}")
    print('  head:', body[:130].replace('\n', ' '))
