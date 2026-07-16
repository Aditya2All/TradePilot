from dataclasses import dataclass
from dotenv import load_dotenv
import os

load_dotenv()


@dataclass(frozen=True)
class Settings:
    upstox_api_key: str = os.getenv("UPSTOX_API_KEY", "")
    upstox_api_secret: str = os.getenv("UPSTOX_API_SECRET", "")
    upstox_redirect_uri: str = os.getenv("UPSTOX_REDIRECT_URI", "")

    trading_mode: str = os.getenv("TRADING_MODE", "paper")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()