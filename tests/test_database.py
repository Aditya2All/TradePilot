from database.trade_repository import TradeRepository

repo = TradeRepository()

print("Database initialized.")

print(repo.all_trades())