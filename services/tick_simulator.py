from datetime import datetime, timedelta


class TickSimulator:

    def __init__(self, on_tick):
        self.on_tick = on_tick

    def run(self):

        start = datetime(2026, 7, 18, 9, 15)

        prices = [
            100.00,
            100.20,
            100.10,
            100.50,
            100.40,
            100.80,
            100.60,
            100.90,
            101.10,
            101.00,
            101.30,
            101.20,
        ]

        for i, price in enumerate(prices):

            timestamp = start + timedelta(minutes=i)

            message = {
                "currentTs": int(timestamp.timestamp() * 1000),
                "feeds": {
                    "SIM": {
                        "ltpc": {
                            "ltp": price
                        }
                    }
                }
            }

            self.on_tick(message)