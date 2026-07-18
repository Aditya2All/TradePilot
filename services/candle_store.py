import pandas as pd


class CandleStore:

    def __init__(self, max_candles=500):

        self.max_candles = max_candles
        self.candles = []

    def add(self, candle):

        self.candles.append(candle)

        if len(self.candles) > self.max_candles:
            self.candles.pop(0)

    def size(self):

        return len(self.candles)

    def latest(self):

        if not self.candles:
            return None

        return self.candles[-1]

    def to_dataframe(self):

        if not self.candles:
            return pd.DataFrame()

        return pd.DataFrame([
            {
                "datetime": c.start_time,
                "open": c.open,
                "high": c.high,
                "low": c.low,
                "close": c.close,
                "volume": c.volume,
            }
            for c in self.candles
        ])