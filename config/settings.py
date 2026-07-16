from dataclasses import dataclass
import os

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    api_key: str = os.getenv("UPSTOX_API_KEY", "")
    api_secret: str = os.getenv("UPSTOX_API_SECRET", "")
    redirect_uri: str = os.getenv("REDIRECT_URI", "")
    access_token: str = os.getenv("ACCESS_TOKEN", "")
    trading_mode: str = os.getenv("TRADING_MODE", "paper")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()