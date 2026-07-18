from broker.upstox.client import UpstoxBroker

broker = UpstoxBroker()

print(broker.get_instrument_key("RELIANCE"))