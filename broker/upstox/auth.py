from threading import Thread
import webbrowser

import requests
from flask import Flask, request

from config.settings import settings
from core.logger import logger


class UpstoxAuth:
    LOGIN_URL = "https://api.upstox.com/v2/login/authorization/dialog"
    TOKEN_URL = "https://api.upstox.com/v2/login/authorization/token"

    def __init__(self):
        self.authorization_code = None
        self.access_token = None

    def _start_callback_server(self):

        app = Flask(__name__)

        @app.route("/callback")
        def callback():

            self.authorization_code = request.args.get("code")

            logger.info(
                f"Authorization Code Received: {self.authorization_code}"
            )

            return """
            <h2>TradePilot Authentication Successful</h2>
            <h3>You can close this window.</h3>
            """

        thread = Thread(
            target=lambda: app.run(
                host="127.0.0.1",
                port=5000,
                debug=False,
                use_reloader=False,
            ),
            daemon=True,
        )

        thread.start()

    def get_login_url(self):

        return (
            f"{self.LOGIN_URL}"
            f"?response_type=code"
            f"&client_id={settings.upstox_api_key}"
            f"&redirect_uri={settings.upstox_redirect_uri}"
        )

    def login(self):

        self._start_callback_server()

        url = self.get_login_url()

        logger.info("Opening Upstox Login Page...")

        webbrowser.open(url)

        while self.authorization_code is None:
            pass

        logger.info("Authorization code captured.")

        payload = {
            "code": self.authorization_code,
            "client_id": settings.upstox_api_key,
            "client_secret": settings.upstox_api_secret,
            "redirect_uri": settings.upstox_redirect_uri,
            "grant_type": "authorization_code",
        }

        headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        response = requests.post(
            self.TOKEN_URL,
            headers=headers,
            data=payload,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        self.access_token = data["access_token"]

        logger.info("Access Token generated successfully.")

        return self.access_token