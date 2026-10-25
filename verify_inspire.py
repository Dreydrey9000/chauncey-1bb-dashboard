#!/usr/bin/env python3
"""Verify live inspire.js deploy on Cloudflare Pages (browser UA)."""
import urllib.request

url = 'https://1bb-dashboard.pages.dev/inspire.js'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'})
with urllib.request.urlopen(req, timeout=30) as r:
    body = r.read().decode('utf-8', 'replace')
print('HTTP', r.status, '| bytes:', len(body))
print('AM edition live:', '2026-10-25 (AM)' in body)
print('drey reel url live:', 'DeuubqRujjS' in body)
print('kevin reel url live:', 'DeuRrm_sPRL' in body)
print('window.INSPIRE shape ok:', body.lstrip().startswith('// Daily inspiration brief'))
import hashlib, os
local = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'site', 'inspire.js'), 'rb').read()
print('sha256 parity:', hashlib.sha256(local).hexdigest() == hashlib.sha256(body.encode()).hexdigest())
