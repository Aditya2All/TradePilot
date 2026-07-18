from broker.upstox.client import UpstoxBroker

from config.trading import INSTRUMENT_KEY


broker = UpstoxBroker()

broker.authenticate()

broker.start_market_stream(INSTRUMENT_KEY)