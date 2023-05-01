import os
import numpy as np
import pandas as pd
import datetime
import time
from pandas.tseries.offsets import BDay
from yahoo_fin import stock_info as si
import argparse

from ib_historical_data import *


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
                    prog='Historical Bars data downloader',
                    description='Backfills historical bars data thru last business day',
                    epilog='------------------------------------------------------------')
    
    parser.add_argument("dataDir", type=str, help="directory where data is stored", default=None)
    parser.add_argument("-barSizeSetting", type=str, help="duration of bars. i.e 1 min, etc.", default="1 min")
    parser.add_argument("-whatToShow", type=str, help="TRADES MIDPOINT BID ASK", default="TRADES")

    args = parser.parse_args()

    dataDir = args.dataDir
    barSizeSetting = args.barSizeSetting
    whatToShow = args.whatToShow

    data_files = os.listdir(dataDir)

    last_BDay = datetime.datetime.today() - BDay(1)
    last_BDay = pd.Timestamp(last_BDay)
    last_BDay = last_BDay.replace(hour=23, minute=59, second=59, microsecond=0)

    endDateTime = (str(last_BDay) + " US/Eastern").replace("-","")

    for file in data_files:
        if ".csv" in file:
            stock = file.split(".")[0]
            print(f"Processing {stock}")
            start_time = time.time()

            df = pd.read_csv(os.path.join(dataDir, file))
            last_data_date = pd.Timestamp(df.Date.max()).date()
            bdays = pd.bdate_range(start=last_data_date, end=last_BDay.date(), freq="1 D")[1:]
            ndays = len(bdays)

            dloader = HistoricalBarsDataLoader()

            dloader.fetch(
                stock, endDateTime, f"{ndays} D", barSizeSetting, whatToShow, useRTH=0
            )

            df_new = dloader.bars_to_df()

            assert df.Date.max() < df_new.Date.max()

            df = pd.concat([df, df_new])

            df.to_csv(os.path.join(dataDir, file), index=False)

            end_time = time.time()
            print(f"processing {stock} for {endDateTime} took {end_time - start_time : 6.2f} sec")

    print("Finished historical bars data backfill........................................................")

