from broker.upstox.rest_client import RestClient


class History:

    def __init__(self, rest_client: RestClient):
        self.rest = rest_client

    def get_historical_data(
        self,
        instrument_key: str,
        interval: str,
        from_date: str,
        to_date: str,
    ):

        endpoint = (
            f"/historical-candle/"
            f"{instrument_key}/"
            f"{interval}/"
            f"{to_date}/"
            f"{from_date}"
        )

        return self.rest.get(endpoint)