import urllib.request

url = 'https://1bb-dashboard.pages.dev/inspire.js'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'})
with urllib.request.urlopen(req, timeout=30) as r:
    body = r.read().decode()

checks = {
    'today marker (2026-09-29 (PM))': '2026-09-29 (PM)' in body,
    'drey reel URL (Ddy7G_Mstov)': 'https://www.instagram.com/reel/Ddy7G_Mstov/' in body,
    'kevin reel URL (Dd4GN0OgBkZ)': 'https://www.instagram.com/reel/Dd4GN0OgBkZ/' in body,
    'no unescaped raw apostrophes inside strings': body.count("'") == body.count("'") and '\\x27' in body,
    'deployed bytes match local file': len(body) == len(open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/site/inspire.js').read()),
}
print('HTTP OK, bytes:', len(body))
for name, ok in checks.items():
    print(('PASS' if ok else 'FAIL'), '-', name)
print('ALL PASS' if all(checks.values()) else 'SOMETHING FAILED')
