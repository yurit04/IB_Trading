from ibapi.client import *
from ibapi.wrapper import *
import time

class TestApp(EClient, EWrapper):

    def __init__(self):
        EClient.__init__(self, self)

    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        print(f"reqId={reqId} | validExchanges ={contractDetails.validExchanges}")
        print(f"reqId={reqId} | category       ={contractDetails.category}")
        print(f"reqId={reqId} | contract       ={contractDetails.contract}")
        print(f"reqId={reqId} | descAppend     ={contractDetails.descAppend}")
        print(f"reqId={reqId} | industry       ={contractDetails.industry}")
        print(f"reqId={reqId} | longName       ={contractDetails.longName}")
        print(f"reqId={reqId} | marketName     ={contractDetails.marketName}")
        print(f"reqId={reqId} | tradingHours   ={contractDetails.tradingHours}")
        print(f"reqId={reqId} | liquidHours    ={contractDetails.liquidHours}")
        print(f"reqId={reqId} | minTick        ={contractDetails.minTick}")
        print(f"reqId={reqId} | orderTypes     ={contractDetails.orderTypes}")
        print(f"reqId={reqId} | stockType      ={contractDetails.stockType}")
    
    def contractDetailsEnd(self, reqId: int):
        self.disconnect()

def main():
    app = TestApp()
    app.connect("127.0.0.1", 7497, clientId=1)
    time.sleep(1)

    contract = Contract()
    # contract.conId = 265598 # can use contract Id instead of evereything else
    contract.symbol = "AAPL"
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
    contract.primaryExchange = "ISLAND"

    app.reqContractDetails(1, contract)

    app.run()

if __name__ == "__main__":
    main()