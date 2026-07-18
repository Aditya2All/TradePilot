from datetime import datetime

from core.logger import logger
from services.candle_builder import CandleBuilder


class MarketDataService:

    def __init__(self):

        self.candle_builder = CandleBuilder()

        self.on_candle = None

    def process_tick(self, message):

        feeds = message.get("feeds")

        if not feeds:
            return

        timestamp = datetime.fromtimestamp(
            int(message["currentTs"]) / 1000
        )

        for _, feed in feeds.items():

            ltpc = feed.get("ltpc")

            if ltpc is None:
                continue

            price = float(ltpc["ltp"])

            candle = self.candle_builder.update(
                price=price,
                timestamp=timestamp,
            )

            if candle:

                logger.info(
                    f"Completed Candle : {candle}"
                )

                if self.on_candle:
                    self.on_candle(candle)