from broker.upstox.client import UpstoxBroker
from utils.dataframe import candles_to_dataframe

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

    print(df)
    print(df.info())


if __name__ == "__main__":
    main()