import requests

from broker.base import Broker
from broker.upstox.auth import UpstoxAuth
from core.logger import logger
from broker.upstox.rest_client import RestClient


class UpstoxBroker(Broker):

    PROFILE_URL = "https://api.upstox.com/v2/user/profile"

    def __init__(self):
        self.auth = UpstoxAuth()
        self.access_token = None

    def authenticate(self):
        self.access_token = self.auth.login()
        self.rest = RestClient(self.access_token)
        logger.info("Authentication successful.")

    def get_profile(self):
        return self.rest.get("/user/profile")

    def place_order(self, **kwargs):
        raise NotImplementedError

    def get_positions(self):
        raise NotImplementedError