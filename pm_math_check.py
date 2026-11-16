#!/usr/bin/env python3
"""Verify ratios cited in the 2026-11-16 PM brief."""
rowan = [343228, 157782, 24310, 18392, 27247, 33965, 29140, 31865, 123426]
rowan_med = sorted(rowan)[len(rowan)//2]
print(f"rowan n=9 median={rowan_med}  343228/med={343228/rowan_med:.2f}x")
melt = sorted([2203, 3673, 1376, 30498, 1533, 7258, 4008, 2753, 1691, 4822])
melt_med = (melt[4]+melt[5])/2
print(f"meltzer n=10 median={melt_med}  30498/med={30498/melt_med:.2f}x")
print(f"kevin brother 4506/1384={4506/1384:.2f}x  vs morning 3491: {4506/3491-1:+.0%}")
print(f"kevin lion 1225/1384={1225/1384:.2f}x")
print(f"drey nov12 1350/243.5={1350/243.5:.1f}x  tool reel 143/243.5={143/243.5:.2f}x  A/B ratio={1350/143:.1f}x")
print(f"drey room/ai gap 1387/243.5={1387/243.5:.1f}x")
