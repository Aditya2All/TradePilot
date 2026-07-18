import time
from datetime import datetime

from config.market import MARKET_OPEN, MARKET_CLOSE
from engine.trading_engine import TradingEngine
from config.trading import SCHEDULER_INTERVAL_SECONDS

class Scheduler:

    def __init__(self):
        self.engine = TradingEngine()

    def market_is_open(self):

        now = datetime.now().strftime("%H:%M")

        return MARKET_OPEN <= now <= MARKET_CLOSE

    def seconds_until_next_5min(self):

        now = datetime.now()

        seconds = (
            (5 - now.minute % 5) * 60
            - now.second
        )

        if seconds <= 0:
            seconds += 300

        return seconds

    def start(self):

        print("\n===== Scheduler Started =====\n")

        while True:

            if self.market_is_open():

                print(
                    f"\n[{datetime.now()}] Running trading cycle..."
                )

                try:
                    self.engine.run_cycle()

                except Exception as e:
                    print(e)

                wait = SCHEDULER_INTERVAL_SECONDS

                print(f"Sleeping {wait} seconds...\n")

                time.sleep(wait)
            else:

                print("Market Closed")

                time.sleep(60)