#!/usr/bin/env python3
"""Verify live inspire.js deploy on Cloudflare Pages (browser UA)."""
import urllib.request

url = 'https://1bb-dashboard.pages.dev/inspire.js'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'})
with urllib.request.urlopen(req, timeout=30) as r:
    body = r.read().decode('utf-8', 'replace')
print('HTTP', r.status, '| bytes:', len(body))
print('PM edition live:', '2026-10-12 (PM)' in body)
print('drey reel url live:', 'Dd4UT-POMub' in body)
print('kevin reel url live:', 'DeUQ4aJsUbE' in body)
print('window.INSPIRE shape ok:', body.lstrip().startswith('// Daily inspiration brief'))
