"""
Trading configuration
"""

# Instrument
SYMBOL = "RELIANCE"
INSTRUMENT_KEY = "NSE_EQ|INE002A01018"

# Timeframe
TIMEFRAME = "day"

# Historical data
LOOKBACK_DAYS = 60

# Indicators
EMA_FAST = 9
EMA_SLOW = 21

# Trading
INITIAL_CAPITAL = 100000
DEFAULT_QUANTITY = 10

# Scheduler interval
# Development = 15
# Live 5-minute trading = 300

SCHEDULER_INTERVAL_SECONDS = 15