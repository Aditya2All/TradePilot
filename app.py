from broker.upstox.client import UpstoxBroker
from utils.dataframe import candles_to_dataframe
from indicators.ema import ema
from strategy.ema_crossover import EMACrossoverStrategy


def main():

    broker = UpstoxBroker()

    broker.authenticate()

    candles = broker.get_historical_data(
        instrument_key="NSE_EQ|INE002A01018",
        interval="day",
        from_date="2026-07-01",
        to_date="2026-07-17",
    )

    df = candles_to_dataframe(candles)

    df["EMA9"] = ema(df["close"], 9)
    df["EMA21"] = ema(df["close"], 21)

    strategy = EMACrossoverStrategy()

    signal = strategy.generate_signal(df)

    print("\n========== SIGNAL ==========")
    print(signal)

    print("\n========== LATEST DATA ==========\n")
    print(df[["datetime", "close", "EMA9", "EMA21"]].tail(10))

    # line 37 to 51 were added temporarily

    from engine.paper_trader import PaperTrader

    paper = PaperTrader()

    paper.buy(
        symbol="RELIANCE",
        price=float(df.iloc[-1]["close"]),
        quantity=10,
    )

    paper.sell(
        price=float(df.iloc[-1]["close"]) + 25
    )

    paper.summary()


if __name__ == "__main__":
    main()