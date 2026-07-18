import requests

from broker.base import Broker
from broker.upstox.auth import UpstoxAuth
from core.logger import logger
from broker.upstox.rest_client import RestClient
from broker.upstox.market_data import MarketData
from broker.upstox.instrument_manager import InstrumentManager
from broker.upstox.history import History
from broker.upstox.websocket_client import UpstoxWebSocket

class UpstoxBroker(Broker):

    PROFILE_URL = "https://api.upstox.com/v2/user/profile"

    def __init__(self):
        self.auth = UpstoxAuth()
        self.instrument_manager = InstrumentManager()
        self.instrument_manager.load()
        self.access_token = None

    def authenticate(self):
        self.access_token = self.auth.login()
        self.rest = RestClient(self.access_token)
        self.market_data = MarketData(self.rest)
        self.history = History(self.rest)
        self.websocket = UpstoxWebSocket(self.access_token)
        logger.info("Authentication successful.")

    def get_profile(self):
        return self.rest.get("/user/profile")

    def place_order(self, **kwargs):
        raise NotImplementedError

    def get_positions(self):
        raise NotImplementedError
    
    def get_ltp(self, instrument_key: str):
        return self.market_data.get_ltp(instrument_key)
    
    def start_market_stream(self, instrument_key: str):
        self.websocket.connect(instrument_key)

    def get_instrument_key(self, symbol: str):
        return self.instrument_manager.get_instrument_key(symbol)
    
    def create_websocket(self):
        return UpstoxWebSocket(self.access_token)
    

   # def get_ltp_by_symbol(self, symbol: str):

    #    instrument_key = self.instrument_manager.get_instrument_key(symbol)

    #   if instrument_key is None:
    #      raise ValueError(f"{symbol} not found")
    #
    #   return self.get_ltp(instrument_key)
     
    def get_historical_data(
        self,
        instrument_key,
        interval,
        from_date,
        to_date,
    ):
        return self.history.get_historical_data(
            instrument_key,
            interval,
            from_date,
            to_date,
        )