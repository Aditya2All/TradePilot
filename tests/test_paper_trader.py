from engine.paper_trader import PaperTrader

trader = PaperTrader(initial_capital=100000)

print("Creating BUY...")
trader.buy(
    symbol="RELIANCE",
    price=1000,
    quantity=10,
)

print("Creating SELL...")
trader.sell(
    price=1050,
)

trader.summary()