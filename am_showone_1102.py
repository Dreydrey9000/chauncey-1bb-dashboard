#!/usr/bin/env python3
"""Print full analytics payload of one post to see actual field names."""
import json

R = json.load(open('/Users/andrethomas/.hermes/workspaces/chauncey/dashboard/raw/am_postan_1102.json'))
p = R['drey'][0]
print(json.dumps(p['analytics'], indent=1)[:2500])
