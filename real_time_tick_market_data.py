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

        self.reqMarketDataType(1)
        self.reqMktData(orderId, contract, "", 0, 0, [])
        
    def tickPrice(self, reqId: TickerId, tickType: TickType, price: float, attrib: TickAttrib):
        if TickTypeEnum.to_str(tickType) == "ASK":
            print(f"tickPrice. reqId: {reqId}, tickType: {TickTypeEnum.to_str(tickType)}, price: {price}, attribs: {attrib}")

    def tickSize(self, reqId: TickerId, tickType: TickType, size: int):
        # print(f"tickSize. reqId: {reqId}, tickType: {TickTypeEnum.to_str(tickType)}, size: {size}")
        pass

def main():
    app = TestApp()
    app.connect("127.0.0.1", 7497, clientId=1)
    app.run()
    app.disconnect()

if __name__ == "__main__":
    main()