from config.settings import settings
from core.logger import logger


def main() -> None:
    logger.info("====================================")
    logger.info("TradePilot starting...")
    logger.info(f"Mode: {settings.trading_mode}")
    logger.info("Configuration loaded")
    logger.info("====================================")


if __name__ == "__main__":
    main()