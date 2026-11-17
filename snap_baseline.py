#!/opt/homebrew/bin/python3
"""Capture prior-day baseline (posts, followers) before refresh overwrites raw/."""
import json, re, os, sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# post counts + generation stamp from current data.js
try:
    s = open("site/data.js").read()
    m = re.search(r'generated[\"\' :=]+([0-9T:\-.]+)', s)
    print("prev_stamp:", m.group(1) if m else "n/a")
except Exception as e:
    print("data.js read fail:", e)

# follower baseline from current followers.json
try:
    d = json.load(open("raw/followers.json"))
    print(json.dumps(d, indent=None)[:2000])
except Exception as e:
    print("followers.json read fail:", e)
