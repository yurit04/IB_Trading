from ibapi.client import *
from ibapi.wrapper import *
from ibapi.tag_value import *
import time

class TestApp(EClient, EWrapper):

    def __init__(self):
        EClient.__init__(self, self)

    def nextValidId(self, orderId: int):
        self.reqScannerParameters()

    def scannerParameters(self, xml: str):
        dir = "D:\\scanner.xml"
        open(dir, 'w').write(xml)
        print("Scanner parameters received!")
        self.disconnect()

def main():
    app = TestApp()
    app.connect("127.0.0.1", 7497, clientId=1)
    app.run()    

if __name__ == "__main__":
    main()