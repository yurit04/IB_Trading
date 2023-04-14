from ibapi.client import *
from ibapi.wrapper import *
import pandas as pd

class HistoricalBarDataLoader(EClient, EWrapper):

    def __init__(self, port=7497):
        EClient.__init__(self, self)
        self.port = port
        self.bars = []
        self.contract = None

    def fetch(
        self, 
        symbol, 
        endDateTime: str,
        durationStr: str,
        barSizeSetting: str, # 1 sec 5 secs 15 secs 30 secs 1 min 2 mins 3 mins 5 mins 15 mins 30 mins 1 hour 1 day
        whatToShow: str, # TRADES MIDPOINT BID ASK BID_ASK HISTORICAL_VOLATILITY OPTION_IMPLIED_VOLATILITY
        useRTH: int=1,
        formatDate: int=1,
        secType="STK", 
        exchange="SMART", 
        currency="USD", 
        primaryExchange="ISLAND"            
    ):
        self.bars = []

        self.contract = Contract()
        self.contract.symbol = symbol
        self.contract.secType = secType
        self.contract.exchange = exchange
        self.contract.currency = currency
        self.contract.primaryExchange = primaryExchange

        self.endDateTime = endDateTime
        self.durationStr = durationStr
        self.barSizeSetting = barSizeSetting
        self.whatToShow = whatToShow
        self.useRTH = useRTH
        self.formatDate = formatDate

        if not self.isConnected():
            self.connect("127.0.0.1", self.port, clientId=1)
        self.run()

    def nextValidId(self, orderId: int):

        self.reqHistoricalData(            
            orderId, self.contract,self.endDateTime, self.durationStr, self.barSizeSetting, self.whatToShow, self.useRTH, self.formatDate, False, []
        )
        
    def historicalData(self, reqId, bar):
        self.bars.append(bar)

    def historicalDataEnd(self, reqId: int, start: str, end: str):
        self.disconnect()

    def bars_to_df(self):
        date, open, high, low, close, volume, barCount, average = [], [], [], [], [], [], [], []
        for bar in self.bars:
            date.append(bar.date)
            open.append(bar.open)
            high.append(bar.high)
            low.append(bar.low)
            close.append(bar.close)
            volume.append(bar.volume)
            barCount.append(bar.barCount)
            average.append(bar.average)

        bars_df = pd.DataFrame({
            "Date": date, 
            "Open": open,
            "High": high,
            "Low": low,
            "Close": close,
            "Volume": volume, 
            "BarCount": barCount,
            "Average": average
        })

        return bars_df

    def bars_to_csv(self, csv_file):
        bars_df = self.bars_to_df()
        bars_df.to_csv(csv_file, index=False)


if __name__ == "__main__":
    dloader = HistoricalBarDataLoader()
    dloader.fetch("AAPL", "20230410 23:59:59 US/Eastern", "1 D", "1 min", "TRADES", useRTH=0)
    for bar in dloader.bars:
        print(bar)

    dloader.bars_to_csv("AAPL_TRADES.csv")
