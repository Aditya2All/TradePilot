from engine.trading_engine import TradingEngine

engine = TradingEngine()

engine.broker.authenticate()

engine.start_live_feed()