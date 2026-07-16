from dataclasses import dataclass
from datetime import datetime


@dataclass
class Position:
    symbol: str
    quantity: int
    entry_price: float
    entry_time: datetime


class PaperTrader:

    def __init__(self, initial_capital: float = 100000):

        self.initial_capital = initial_capital
        self.cash = initial_capital

        self.position = None

        self.trade_history = []

    def buy(self, symbol: str, price: float, quantity: int):

        if self.position is not None:
            print("Already in position.")
            return

        cost = price * quantity

        if cost > self.cash:
            print("Insufficient balance.")
            return

        self.cash -= cost

        self.position = Position(
            symbol=symbol,
            quantity=quantity,
            entry_price=price,
            entry_time=datetime.now(),
        )

        print(f"BUY {quantity} {symbol} @ ₹{price:.2f}")

    def sell(self, price: float):

        if self.position is None:
            print("No open position.")
            return

        pnl = (
            price - self.position.entry_price
        ) * self.position.quantity

        self.cash += price * self.position.quantity

        print(
            f"SELL {self.position.quantity} "
            f"{self.position.symbol} @ ₹{price:.2f}"
        )

        print(f"PnL : ₹{pnl:.2f}")

        self.trade_history.append(
            {
                "symbol": self.position.symbol,
                "buy_price": self.position.entry_price,
                "sell_price": price,
                "quantity": self.position.quantity,
                "profit": pnl,
            }
        )

        self.position = None

    def summary(self):

        print("\n========== PAPER ACCOUNT ==========")

        print(f"Cash : ₹{self.cash:.2f}")

        print(
            f"Trades : {len(self.trade_history)}"
        )