import requests

from core.logger import logger


class RestClient:
    BASE_URL = "https://api.upstox.com/v2"

    def __init__(self, access_token: str):
        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
        })

    def get(self, endpoint: str, params=None):
        url = f"{self.BASE_URL}{endpoint}"

        logger.info(f"GET {url}")

        response = self.session.get(
            url,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()

    def post(self, endpoint: str, data=None):
        url = f"{self.BASE_URL}{endpoint}"

        logger.info(f"POST {url}")

        response = self.session.post(
            url,
            json=data,
            timeout=30,
        )

        response.raise_for_status()

        return response.json()