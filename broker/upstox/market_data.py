from broker.upstox.rest_client import RestClient


class MarketData:

    def __init__(self, rest_client: RestClient):
        self.rest = rest_client

    def get_ltp(self, instrument_key: str):

        response = self.rest.get(
            "/market-quote/ltp",
            params={
                "instrument_key": instrument_key
            }
        )

        return response