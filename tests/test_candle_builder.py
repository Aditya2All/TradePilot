from datetime import datetime

from services.candle_builder import CandleBuilder


builder = CandleBuilder()

ticks = [

    (2948.2, datetime(2026, 7, 18, 9, 15, 1)),
    (2948.7, datetime(2026, 7, 18, 9, 15, 20)),
    (2947.8, datetime(2026, 7, 18, 9, 17, 10)),
    (2949.1, datetime(2026, 7, 18, 9, 19, 55)),

    (2950.0, datetime(2026, 7, 18, 9, 20, 2)),
]

for price, ts in ticks:

    candle = builder.update(price, ts)

    if candle:

        print(candle)