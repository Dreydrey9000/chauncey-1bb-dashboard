# Verify live inspire.js: date marker, reel URLs, quote parity with local file (ignoring \')
import urllib.request, re, hashlib

LOCAL = "/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/site/inspire.js"
URL = "https://1bb-dashboard.pages.dev/inspire.js"
MARKER = "2026-10-04 (AM)"
REELS = [
    "https://www.instagram.com/reel/DdcoYROAjjk/",
    "https://www.instagram.com/reel/Dd5YakesocC/",
]

req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36"})
live = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")
local = open(LOCAL, encoding="utf-8").read()

print("HTTP fetch ok, bytes:", len(live))
print("date marker present:", MARKER in live)
for r in REELS:
    print("reel present:", r, "->", r in live)

def norm(s):
    return re.sub(r"\\'", "", s)

print("content parity (quotes normalized):", norm(live) == norm(local))
print("sha256 local :", hashlib.sha256(local.encode()).hexdigest()[:16])
print("sha256 live  :", hashlib.sha256(live.encode()).hexdigest()[:16])
print("unescaped-quote count local/live:", len(re.findall(r"(?<!\\)'", local)), len(re.findall(r"(?<!\\)'", live)))
