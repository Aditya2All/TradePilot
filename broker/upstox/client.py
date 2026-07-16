from broker.base import Broker
from core.logger import logger


class UpstoxBroker(Broker):

    def authenticate(self):
        logger.info("Authenticating with Upstox...")

    def get_profile(self):
        logger.info("Fetching profile...")

    def place_order(self, **kwargs):
        logger.info("Placing order...")

    def get_positions(self):
        logger.info("Fetching positions...")