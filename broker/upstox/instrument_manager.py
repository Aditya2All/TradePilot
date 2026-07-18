import gzip
import json
from pathlib import Path

import requests

from core.logger import logger
from config.broker import INSTRUMENT_MASTER_URL


class InstrumentManager:
    # TODO: Replace with the official Upstox BOD JSON URL
    #INSTRUMENTS_URL = "<OFFICIAL_UPSTOX_BOD_JSON_URL>"

    def __init__(self):

        self.data_dir = Path("data")
        self.data_dir.mkdir(exist_ok=True)

        self.gz_file = self.data_dir / "instruments.json.gz"
        self.json_file = self.data_dir / "instruments.json"

        self.records = []
        self.symbol_index = {}

    def download(self):

        logger.info("Downloading instrument master...")

        response = requests.get(
            INSTRUMENT_MASTER_URL,
            timeout=120,
        )

        response.raise_for_status()

        self.gz_file.write_bytes(response.content)

        logger.info("Instrument master downloaded.")

    def load(self):

        if not self.gz_file.exists():
            self.download()

        self.extract()

        logger.info("Loading instruments...")

        with open(self.json_file, "r", encoding="utf-8") as f:           
            self.records = json.load(f)

        self.symbol_index = {}

        for item in self.records:

            symbol = item.get("trading_symbol", "").upper()

            if not symbol:
                continue

            self.symbol_index.setdefault(symbol, []).append(item)

        logger.info(f"Loaded {len(self.records)} instruments.")

    def get(self, symbol: str):

        symbol = symbol.upper()

        matches = self.symbol_index.get(symbol)

        if not matches:
            return None

        for item in matches:
            if item.get("segment") == "NSE_EQ":
                return item

        return matches[0]

    def get_instrument_key(self, symbol: str):

        instrument = self.get(symbol)

        if instrument is None:
            raise ValueError(f"Symbol '{symbol}' not found.")

        return instrument["instrument_key"]
    
    def extract(self):

        if self.json_file.exists():
            return

        logger.info("Extracting instrument master...")

        with gzip.open(self.gz_file, "rb") as gz:
            data = gz.read()

        self.json_file.write_bytes(data)

        logger.info("Extraction complete.")