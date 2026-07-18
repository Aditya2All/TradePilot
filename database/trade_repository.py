import sqlite3
from pathlib import Path


class TradeRepository:

    def __init__(self):

        project_root = Path(__file__).resolve().parent.parent

        data_dir = project_root / "data"
        data_dir.mkdir(exist_ok=True)

        db_path = data_dir / "tradepilot.db"

        print(f"Using database: {db_path}")

        self.conn = sqlite3.connect(db_path)

        self.create_table()

    def create_table(self):

        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS trades (

            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            entry_time TEXT,
            exit_time TEXT,
            quantity INTEGER,
            buy_price REAL,
            sell_price REAL,
            profit REAL

        )
        """)

        self.conn.commit()

    def save_trade(self, trade):

        self.conn.execute(
            """
            INSERT INTO trades
            (
                symbol,
                entry_time,
                exit_time,
                quantity,
                buy_price,
                sell_price,
                profit
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(trade["symbol"]),
                str(trade["entry_time"]),
                str(trade["exit_time"]),
                int(trade["quantity"]),
                float(trade["buy_price"]),
                float(trade["sell_price"]),
                float(trade["profit"]),
            ),
        )

        self.conn.commit()

    def all_trades(self):

        return self.conn.execute(
            "SELECT * FROM trades"
        ).fetchall()