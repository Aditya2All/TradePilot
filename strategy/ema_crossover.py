import pandas as pd


class EMACrossoverStrategy:
    """
    EMA 9 / EMA 21 crossover strategy.
    """

    def generate_signal(self, df: pd.DataFrame) -> str:

        # Need enough candles
        if len(df) < 21:
            return "HOLD"

        prev = df.iloc[-2]
        curr = df.iloc[-1]

        # BUY Signal
        if (
            prev["EMA9"] <= prev["EMA21"]
            and curr["EMA9"] > curr["EMA21"]
        ):
            return "BUY"

        # SELL Signal
        if (
            prev["EMA9"] >= prev["EMA21"]
            and curr["EMA9"] < curr["EMA21"]
        ):
            return "SELL"

        return "HOLD"