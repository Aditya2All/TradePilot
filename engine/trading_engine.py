from config.trading import (
    SYMBOL,
    INSTRUMENT_KEY,
    TIMEFRAME,
    EMA_FAST,
    EMA_SLOW,
    INITIAL_CAPITAL,
    DEFAULT_QUANTITY,
    LOOKBACK_DAYS,
)

from datetime import date, timedelta


from broker.upstox.client import UpstoxBroker
from utils.dataframe import candles_to_dataframe
from indicators.ema import ema
from strategy.ema_crossover import EMACrossoverStrategy
from engine.paper_trader import PaperTrader
from services.market_data_service import MarketDataService
from services.candle_store import CandleStore
from services.candle_builder import Candle


class TradingEngine:

    def __init__(self):

        self.websocket = None

        self.candle_store = CandleStore()
        self.market_data = MarketDataService()

        self.market_data.on_candle = self.on_new_candle

        self.broker = UpstoxBroker()
        self.strategy = EMACrossoverStrategy()
        self.paper_trader = PaperTrader(
            initial_capital=INITIAL_CAPITAL
        )
    
    def start_live_feed(self):

        instrument_key = self.broker.get_instrument_key(SYMBOL)

        self.websocket = self.broker.create_websocket()

        self.websocket.connect(
            instrument_key,
            self.on_tick,
        )

    def bootstrap_history(self):

        print("Loading historical candles...")

        today = date.today()
        from_date = today - timedelta(days=LOOKBACK_DAYS)

        candles = self.broker.get_historical_data(
            instrument_key=INSTRUMENT_KEY,
            interval=TIMEFRAME,
            from_date=str(from_date),
            to_date=str(today),
        )

        df = candles_to_dataframe(candles)

        for _, row in df.iterrows():

            candle = Candle(
                start_time=row["datetime"],
                open=float(row["open"]),
                high=float(row["high"]),
                low=float(row["low"]),
                close=float(row["close"]),
                volume=int(row["volume"]),
            )

            self.candle_store.add(candle)

        print(
            f"Loaded {self.candle_store.size()} historical candles."
        )

    def run(self):

        print("\n========== STARTING TRADEPILOT ==========\n")

        # Authenticate
        self.broker.authenticate()

        # Load historical candles into CandleStore
        self.bootstrap_history()

        # Start live market feed
        self.start_live_feed()

    def on_tick(self, message):

        print("\n========== LIVE TICK ==========")
        self.market_data.process_tick(message)

    def on_new_candle(self, candle):

        self.candle_store.add(candle)

        print("\n========== NEW CANDLE ==========")
        print(candle)

        df = self.candle_store.to_dataframe()

        df[f"EMA{EMA_FAST}"] = ema(df["close"], EMA_FAST)
        df[f"EMA{EMA_SLOW}"] = ema(df["close"], EMA_SLOW)

        signal = self.strategy.generate_signal(df)

        latest_price = float(df.iloc[-1]["close"])

        print("\n========== STRATEGY ==========")
        print(f"Price  : ₹{latest_price:.2f}")
        print(f"Signal : {signal}")

        if signal == "BUY":
            self.paper_trader.buy(
                symbol=SYMBOL,
                price=latest_price,
                quantity=DEFAULT_QUANTITY,
            )

        elif signal == "SELL":
            self.paper_trader.sell(
                price=latest_price,
            )

        self.paper_trader.summary()
        
