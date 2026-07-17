from broker.upstox.client import UpstoxBroker
from utils.dataframe import candles_to_dataframe
from indicators.ema import ema
from strategy.ema_crossover import EMACrossoverStrategy
from engine.paper_trader import PaperTrader


class TradingEngine:

    def __init__(self):
        self.broker = UpstoxBroker()
        self.strategy = EMACrossoverStrategy()
        self.paper_trader = PaperTrader(initial_capital=100000)

    def run(self):

        print("\n========== STARTING TRADEPILOT ==========\n")

        # Authenticate
        self.broker.authenticate()

        # Fetch Historical Data
        candles = self.broker.get_historical_data(
            instrument_key="NSE_EQ|INE002A01018",
            interval="day",
            from_date="2026-07-01",
            to_date="2026-07-17",
        )

        # Convert to DataFrame
        df = candles_to_dataframe(candles)

        # Calculate Indicators
        df["EMA9"] = ema(df["close"], 9)
        df["EMA21"] = ema(df["close"], 21)

        # Generate Signal
        signal = self.strategy.generate_signal(df)

        latest_price = float(df.iloc[-1]["close"])

        print(f"\nSignal : {signal}")
        print(f"Price  : ₹{latest_price}")

        # Execute Paper Trade
        if signal == "BUY":
            self.paper_trader.buy(
                symbol="RELIANCE",
                price=latest_price,
                quantity=10,
            )

        elif signal == "SELL":
            self.paper_trader.sell(
                price=latest_price,
            )

        self.paper_trader.summary()