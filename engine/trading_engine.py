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


class TradingEngine:

    def __init__(self):

        self.websocket = None

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

    def on_tick(self, message):

        print("\n========== LIVE TICK ==========")
        self.market_data.process_tick(message)

    def on_new_candle(self, candle):

        print("\n========== NEW 5-MIN CANDLE ==========")

        print(candle)

    def run_cycle(self):

        print("\n========== STARTING TRADEPILOT ==========\n")

        # Authenticate
        self.broker.authenticate()

        # Fetch Historical Data
        today = date.today()
        from_date = today - timedelta(days=LOOKBACK_DAYS)

        candles = self.broker.get_historical_data(
            instrument_key=INSTRUMENT_KEY,
            interval=TIMEFRAME,
            from_date=str(from_date),
            to_date=str(today),
        )

        # Convert to DataFrame
        df = candles_to_dataframe(candles)

        # Calculate Indicators
        df[f"EMA{EMA_FAST}"] = ema(df["close"], EMA_FAST)
        df[f"EMA{EMA_SLOW}"] = ema(df["close"], EMA_SLOW)

        # Generate Signal
        signal = self.strategy.generate_signal(df)

        latest_price = float(df.iloc[-1]["close"])

        print(f"\nSignal : {signal}")
        print(f"Price  : ₹{latest_price}")

        # Execute Paper Trade
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