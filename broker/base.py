from abc import ABC, abstractmethod


class Broker(ABC):
    """Base interface that every broker implementation must follow."""

    @abstractmethod
    def authenticate(self) -> None:
        """Authenticate with the broker."""
        raise NotImplementedError

    @abstractmethod
    def get_profile(self):
        """Fetch the logged-in user's profile."""
        raise NotImplementedError

    @abstractmethod
    def place_order(self, **kwargs):
        """Place an order."""
        raise NotImplementedError

    @abstractmethod
    def get_positions(self):
        """Fetch open positions."""
        raise NotImplementedError