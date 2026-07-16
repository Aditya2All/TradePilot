from broker.upstox.client import UpstoxBroker
from core.logger import logger


def main():

    broker = UpstoxBroker()

    broker.authenticate()

    profile = broker.get_profile()

    logger.info("Connected Successfully")

    print("\n========== PROFILE ==========\n")

    print(profile)


if __name__ == "__main__":
    main()