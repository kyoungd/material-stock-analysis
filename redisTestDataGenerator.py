import logging

import alpaca_trade_api as alpaca
from alpaca_trade_api.stream import Stream
from alpaca_trade_api.common import URL
from redistimeseries.client import Client
from redisTSCreateTable import CreateRedisStockTimeSeriesKeys
from alpaca_trade_api.rest import REST
from redisTSBars import RealTimeBars
from redisUtil import RedisTimeFrame, SetInterval, TimeStamp
import random
from datetime import datetime
import time

ALPACA_API_KEY = 'AKAV2Z5H0NJNXYF7K24D'
ALPACA_SECRET_KEY = '262cAEeIRrL1KEZYKSTjZA79tj25XWrMtvz0Bezu'
ALPACA_API_URL = 'https://api.alpaca.markets'


rts = Client(host='127.0.0.1', port=6379)
api = alpaca.REST(
    ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_API_URL)

# rtb = RealTimeBars()
# data = rtb.redis_get_data(rts, api, 'FANG', RedisTimeFrame.MIN5)
# print(data)
# for ts, price in data:
#     print(ts, "  ", price)

symbol = 'FANG'

rootpoint = {
    'close': 11.10,
    'high': 11.13,
    'low': 11.0,
    'open': 11.03,
    'symbol': symbol,
    'timestamp': 1627493640000000000,
    'trade_count': 63,
    'volume': 2730,
    'vwap': 53.02548
}
testData = []


def create_test_data():
    datapoint = rootpoint
    close = datapoint['close']
    for _ in range(24):
        testData.append(datapoint.copy())
        close += 0.04
        datapoint['high'] = close + 0.10
        datapoint['close'] = close
    for _ in range(24):
        testData.append(datapoint.copy())
        close -= 0.04
        datapoint['high'] = close + 0.2
        datapoint['close'] = close
    for _ in range(48):
        testData.append(datapoint.copy())
        close += 0.3
        datapoint['high'] = close + 0.1
        datapoint['close'] = close
    for _ in range(24):
        testData.append(rootpoint.copy())


class NextData():
    idx = 0

    @staticmethod
    def getone():
        data = testData[NextData.idx]
        NextData.idx += 1
        if NextData.idx >= len(testData):
            NextData.idx = 0
        return data

    @staticmethod
    def printone():
        print("index: ", NextData.idx, " -> ", testData[NextData.idx])


def run_test():
    NextData.printone()
    ts = TimeStamp.now()
    bar = NextData.getone()
    bar['timestamp'] = ts
    RealTimeBars.redis_add_bar(rts, data=bar)


if __name__ == "__main__":
    create_test_data()
    tableKeys = CreateRedisStockTimeSeriesKeys()
    tableKeys._createRedisStockSymbol(
        rts, symbol, "NADQ", "test table", "fang company")
    obj_now = datetime.now()
    secWait = 60 - obj_now.second
    time.sleep(secWait)
    SetInterval(5, run_test)


# import time
# import threading

# StartTime = time.time()


# def action():
#     print('action ! -> time : {:.1f}s'.format(time.time()-StartTime))


# class setInterval:
#     def __init__(self, interval, action):
#         self.interval = interval
#         self.action = action
#         self.stopEvent = threading.Event()
#         thread = threading.Thread(target=self.__setInterval)
#         thread.start()

#     def __setInterval(self):
#         nextTime = time.time()+self.interval
#         while not self.stopEvent.wait(nextTime-time.time()):
#             nextTime += self.interval
#             self.action()

#     def cancel(self):
#         self.stopEvent.set()


# # start action every 0.6s
# inter = setInterval(0.6, action)
# print('just after setInterval -> time : {:.1f}s'.format(time.time()-StartTime))

# # will stop interval in 5s
# t = threading.Timer(5, inter.cancel)
# t.start()
