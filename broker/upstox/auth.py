from config.settings import settings
from core.logger import logger


class UpstoxAuth:

    def __init__(self):
        self.api_key = settings.upstox_api_key
        self.api_secret = settings.upstox_api_secret
        self.redirect_uri = settings.upstox_redirect_uri

        logger.info("UpstoxAuth initialized")

    def login(self):
        logger.info("Login process will start here.")