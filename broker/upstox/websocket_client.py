import upstox_client

from core.logger import logger


class UpstoxWebSocket:

    def __init__(self, access_token: str):

        configuration = upstox_client.Configuration()
        configuration.access_token = access_token

        api_client = upstox_client.ApiClient(configuration)

        self.streamer = upstox_client.MarketDataStreamerV3(
            api_client
        )

    def connect(self, instrument_key: str, on_tick):

        def on_open():
            logger.info("WebSocket Connected")

            self.streamer.subscribe(
                [instrument_key],
                "ltpc",
            )

        def on_message(message):
            on_tick(message)

        def on_error(error):
            logger.error(error)

        def on_close():
            logger.info("WebSocket Closed")

        self.streamer.on("open", on_open)
        self.streamer.on("message", on_message)
        self.streamer.on("error", on_error)
        self.streamer.on("close", on_close)

        self.streamer.auto_reconnect(True, 5, 10)

        self.streamer.connect()