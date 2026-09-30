#!/usr/bin/env python3
"""Fetch deployed inspire.js (production + this deployment's direct URL), check PM marker."""
import urllib.request

UA = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36'}

for url in [
    'https://1bb-dashboard.pages.dev/inspire.js',
    'https://228a7299.1bb-dashboard.pages.dev/inspire.js',
]:
    req = urllib.request.Request(url, headers=UA)
    body = urllib.request.urlopen(req, timeout=30).read().decode('utf-8', 'replace')
    print(url)
    print('  bytes:', len(body))
    print('  has PM marker:', '2026-09-30 (PM)' in body)
    print('  has AM marker:', '2026-09-30 (AM)' in body)
    print('  has DZddnLvOmMC (Rowan):', 'DZddnLvOmMC' in body)
    print('  has Ddv4YQMAWrh (AM Liam):', 'Ddv4YQMAWrh' in body)
