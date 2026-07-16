from broker.upstox.client import UpstoxBroker
from config.settings import settings
from core.logger import logger


def main():
    logger.info("TradePilot starting...")
    logger.info(f"Running in {settings.trading_mode} mode")

    broker = UpstoxBroker()
    broker.authenticate()


if __name__ == "__main__":
    main()