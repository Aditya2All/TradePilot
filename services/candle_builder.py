from dataclasses import dataclass
from datetime import datetime


@dataclass
class Candle:

    start_time: datetime

    open: float
    high: float
    low: float
    close: float

    volume: int = 0


class CandleBuilder:

    def __init__(self):

        self.current_candle = None

    def update(self, price: float, timestamp: datetime):

        minute = (timestamp.minute // 5) * 5

        candle_start = timestamp.replace(
            minute=minute,
            second=0,
            microsecond=0,
        )

        # First candle
        if self.current_candle is None:

            self.current_candle = Candle(
                start_time=candle_start,
                open=price,
                high=price,
                low=price,
                close=price,
            )

            return None

        # Same candle
        if candle_start == self.current_candle.start_time:

            self.current_candle.high = max(
                self.current_candle.high,
                price,
            )

            self.current_candle.low = min(
                self.current_candle.low,
                price,
            )

            self.current_candle.close = price

            return None

        # New candle started

        completed = self.current_candle

        self.current_candle = Candle(
            start_time=candle_start,
            open=price,
            high=price,
            low=price,
            close=price,
        )

        return completed