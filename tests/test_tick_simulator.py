from services.market_data_service import MarketDataService
from services.tick_simulator import TickSimulator


market = MarketDataService()


def on_candle(candle):
    print("\n===== COMPLETED CANDLE =====")
    print(candle)


market.on_candle = on_candle

sim = TickSimulator(market.process_tick)

sim.run()