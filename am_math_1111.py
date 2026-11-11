# Verify Liam slot medians + timing math for 2026-11-11 AM brief
import statistics as st
from datetime import datetime, timezone

noon = [(3417, 39), (3922, 54), (8887, 247), (4069, 84), (9343, 318), (9056, 212)]  # 1pm ET slot, Nov 5-10
five = [(2878, 28), (9385, 214), (3078, 27), (7725, 57), (4841, 69), (5256, 52)]      # 5pm ET slot, Nov 5-10
print('Liam 1pm slot: views med', st.median([v for v, _ in noon]), 'comments med', st.median([c for _, c in noon]))
print('Liam 5pm slot: views med', st.median([v for v, _ in five]), 'comments med', st.median([c for _, c in five]))
print('comment ratio:', round(st.median([c for _, c in noon]) / st.median([c for _, c in five]), 2))

pull = datetime(2026, 11, 11, 12, 5, tzinfo=timezone.utc)
for label, ts in [('meltzer new', '2026-11-10T23:50:51'), ('liam 5pm', '2026-11-10T17:09:22'), ('bedros last', '2026-11-09T17:21:44'), ('kevin last', '2026-11-09T14:58:22')]:
    d = datetime.fromisoformat(ts + '+00:00')
    h = (pull - d).total_seconds() / 3600
    print(f'{label}: {h:.1f}h old')
print('drey noon AI reel age at pull:', (pull - datetime.fromisoformat('2026-11-10T17:02:55+00:00')).total_seconds()/3600, 'h')
