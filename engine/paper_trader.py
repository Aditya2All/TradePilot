from dataclasses import dataclass
from datetime import datetime
from database.trade_repository import TradeRepository


@dataclass
class Position:
    symbol: str
    quantity: int
    entry_price: float
    entry_time: datetime


class PaperTrader:

    def __init__(self, initial_capital: float = 100000):

        self.repository = TradeRepository()

        self.initial_capital = initial_capital
        self.cash = initial_capital

        self.position = None

        self.trade_history = []

        self.total_profit = 0.0
        self.winning_trades = 0
        self.losing_trades = 0

    def has_position(self):
        return self.position is not None

    def buy(self, symbol: str, price: float, quantity: int):

        if self.has_position():
            print("Already in position.")
            return False

        cost = price * quantity

        if cost > self.cash:
            print("Insufficient balance.")
            return False

        self.cash -= cost

        self.position = Position(
            symbol=symbol,
            quantity=quantity,
            entry_price=price,
            entry_time=datetime.now(),
        )

        print(f"\nBUY {quantity} {symbol} @ ₹{price:.2f}")

        return True

    def sell(self, price: float):

        if not self.has_position():
            print("No open position.")
            return False

        pnl = (
            price - self.position.entry_price
        ) * self.position.quantity

        self.cash += (
            price * self.position.quantity
        )

        self.total_profit += pnl

        if pnl >= 0:
            self.winning_trades += 1
        else:
            self.losing_trades += 1

        print(
            f"\nSELL {self.position.quantity} "
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
                "entry_time": self.position.entry_time,
                "exit_time": datetime.now(),
            }
        )

        self.repository.save_trade(
            self.trade_history[-1]
        )

        self.position = None

        return True

    def equity(self):

        if self.position is None:
            return self.cash

        return (
            self.cash
            + self.position.entry_price
            * self.position.quantity
        )

    def summary(self):

        total_trades = len(self.trade_history)

        win_rate = (
            (self.winning_trades / total_trades) * 100
            if total_trades
            else 0
        )

        print("\n========== PAPER ACCOUNT ==========")

        print(f"Cash            : ₹{self.cash:.2f}")
        print(f"Equity          : ₹{self.equity():.2f}")
        print(f"Open Position   : {self.has_position()}")
        print(f"Trades          : {total_trades}")
        print(f"Winning Trades  : {self.winning_trades}")
        print(f"Losing Trades   : {self.losing_trades}")
        print(f"Win Rate        : {win_rate:.2f}%")
        print(f"Total P&L       : ₹{self.total_profit:.2f}")