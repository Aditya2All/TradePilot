from broker.base import Broker
from broker.upstox.auth import UpstoxAuth
from core.logger import logger


class UpstoxBroker(Broker):

    def __init__(self):
        self.auth = UpstoxAuth()

    def authenticate(self):
        self.auth.login()

    def get_profile(self):
        logger.info("Profile API")

    def place_order(self, **kwargs):
        logger.info("Place Order")

    def get_positions(self):
        logger.info("Positions")