import urllib.request

url = 'https://1bb-dashboard.pages.dev/inspire.js'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'})
with urllib.request.urlopen(req, timeout=30) as r:
    body = r.read().decode()

payload = body.split('window.INSPIRE')[1]
checks = {
    'today marker (2026-09-30 (AM))': '2026-09-30 (AM)' in body,
    'drey reel URL (Ddv4YQMAWrh)': 'https://www.instagram.com/reel/Ddv4YQMAWrh/' in body,
    'kevin reel URL (Dd5YakesocC)': 'https://www.instagram.com/reel/Dd5YakesocC/' in body,
    'escaped apostrophes present': '\\x27' in body,
    'raw single quotes all structural (even count)': payload.count("'") % 2 == 0,
    'deployed bytes match local file': len(body) == len(open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/site/inspire.js').read()),
}
print('HTTP OK, bytes:', len(body))
for name, ok in checks.items():
    print(('PASS' if ok else 'FAIL'), '-', name)
print('ALL PASS' if all(checks.values()) else 'SOMETHING FAILED')
