from datetime import datetime

from services.candle_builder import Candle
from services.candle_store import CandleStore


store = CandleStore()

store.add(
    Candle(
        start_time=datetime.now(),
        open=100,
        high=102,
        low=99,
        close=101,
    )
)

print(store.size())

print(store.to_dataframe())