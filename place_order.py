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

        self.reqContractDetails(orderId, contract)

    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        print(contractDetails.contract)

        order = Order()
        order.orderId = reqId
        order.action = "BUY"
        order.orderType = "MKT"
        order.totalQuantity = 10

        order.eTradeOnly = False
        order.firmQuoteOnly = False

        order.tif = "GTC"

        self.placeOrder(reqId, contractDetails.contract, order)

        time.sleep(5)
        self.disconnect()

    def openOrder(self, orderId: OrderId, contract: Contract, order: Order, orderState: OrderState):
        print(f"openOrder. orderId: {orderId}, contract: {contract}, order: {order}")

    def orderStatus(
            self, orderId: OrderId, status: str, filled: float, remaining: float, avgFillPrice: float, permId: int, parentId: int, lastFillPrice: float, clientId: int, whyHeld: str, mktCapPrice: float
    ):
        print(
            f"""
            orderStatus. orderId: {orderId}, status: {status}, filled: {filled}, remaining: {remaining}, avgFillPrice: {avgFillPrice}, 
            permId: {permId}, parentId: {parentId}, lastFillPrice: {lastFillPrice}, clinedId: {clientId}, whyHeld: {whyHeld}, mktCapPrice: {mktCapPrice}
            """
        )
        
    def execDetails(self, reqId: int, contract: Contract, execution: Execution):
        print(f"execDetails. redId: {reqId}, contract: {contract}, execution: {execution}")

def main():
    app = TestApp()
    app.connect("127.0.0.1", 7497, clientId=1)
    app.run()

if __name__ == "__main__":
    main()