#!/usr/bin/env python3
"""Ratio checks for the 2026-11-17 PM brief."""
checks = [
    ('kevin moments static vs static median', 4920, 1980),
    ('kevin moments growth today', 4920 - 4753, None),
    ('kevin lion static vs static median', 1333, 1980),
    ('drey nov16 static vs overall median', 305, 241),
    ('drey nov16 static vs ai_systems median', 305, 295),
    ('liam big reel comment rate', 294, 11672),
    ('liam new nov11 reel comment rate', 97, 5385),
    ('drey 11am vs 1pm hour medians', 1630, 227),
    ('drey 11am vs 8pm hour medians', 2016, 227),
]
for label, a, b in checks:
    if b is None:
        print(f'{label}: {a}')
    else:
        print(f'{label}: {a}/{b} = {a/b:.2f}x')
