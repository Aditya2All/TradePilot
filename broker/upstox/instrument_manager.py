import json
from pathlib import Path

import requests

from core.logger import logger


class InstrumentManager:
    # Replace this URL with the official "Complete JSON" URL from the Upstox
    # Instruments documentation.
    INSTRUMENTS_URL = "<OFFICIAL_UPSTOX_COMPLETE_JSON_URL>"

    def __init__(self):
        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)

        self.file_path = self.data_dir / "instruments.json"

        self.instruments = {}

    def download(self):

        logger.info("Downloading instrument master...")

        response = requests.get(
            self.INSTRUMENTS_URL,
            timeout=120,
        )

        response.raise_for_status()

        self.file_path.write_bytes(response.content)

        logger.info("Instrument master downloaded.")

    def load(self):

        if not self.file_path.exists():
            self.download()

        logger.info("Loading instruments...")

        with open(self.file_path, "r", encoding="utf-8") as f:
            records = json.load(f)

        self.instruments = {
            item["trading_symbol"]: item
            for item in records
        }

        logger.info(f"Loaded {len(self.instruments)} instruments.")

    def get(self, symbol: str):

        return self.instruments.get(symbol.upper())

    def get_instrument_key(self, symbol: str):

        item = self.get(symbol)

        if item is None:
            return None

        return item["instrument_key"]