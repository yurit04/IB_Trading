from ibapi.client import *
from ibapi.wrapper import *
import time

class TestApp(EClient, EWrapper):

    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: int):
        contract = Contract()
        # contract.conId = 265598 # can use contract Id instead of evereything else
        contract.symbol = "AAPL"
        contract.secType = "STK"
        contract.exchange = "SMART"
        contract.currency = "USD"
        contract.primaryExchange = "ISLAND"

        self.reqHistoricalData(
            orderId, contract, "20230410 15:00:00 US/Eastern", "2 W", "1 min", "TRADES", # TRADES MIDPOINT BID ASK BID_ASK HISTORICAL_VOLATILITY OPTION_IMPLIED_VOLATILITY
            0, #  0 - all data is returned even where the market in question was outside of its regular trading hours. 1 - only data within the regular trading hours is returned, even if the requested time span falls partially or completely outside of the RTH.
            1, # for standard date time
            False, # want streaming updated? No
            [] # internal use only
        )
        
    def historicalData(self, reqId, bar):
        print(f"Historical data: {bar}")

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        print(f"End of historical data")
        print(f"Start: {start}, End: {end}")
        self.disconnect()

def main():
    app = TestApp()
    app.connect("127.0.0.1", 7497, clientId=1)
    app.run()

if __name__ == "__main__":
    main()