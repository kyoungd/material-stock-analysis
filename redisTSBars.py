##
# Create various Redis TimeSeries for storing stock prices
# and technical indicators
# Author: Prasanna Rajagopal
##

from alpaca_trade_api.rest import TimeFrame
from datetime import datetime, timedelta
from redisUtil import bar_key, TimeStamp, RedisTimeFrame
from redistimeseries.client import Client


# def bar_key(symbol, suffix, time_frame):
#     return "data_" + suffix + "_" + time_frame + ":" + symbol


class RealTimeBars:
    def __init__(self, rts=None):
        if (rts == None):
            self.rts = Client(host='127.0.0.1', port=6379)
        else:
            self.rts = rts

    def _get_bar_list(self, data, timeframe):
        ts = data['timestamp']
        symbol = data['symbol']
        bar_list = []
        bar1 = (bar_key(symbol, "close", timeframe), ts, data['close'])
        bar2 = (bar_key(symbol, "high", timeframe), ts, data['high'])
        bar3 = (bar_key(symbol, "low", timeframe), ts, data['low'])
        bar4 = (bar_key(symbol, "open", timeframe), ts, data['open'])
        bar5 = (bar_key(symbol, "volume", timeframe), ts, data['volume'])
        bar_list.append(bar1)
        bar_list.append(bar2)
        bar_list.append(bar3)
        bar_list.append(bar4)
        bar_list.append(bar5)
        return bar_list

    def redis_add_bar(self, data):
        timeframe = RedisTimeFrame.REALTIME
        bar_list = self._get_bar_list(data, timeframe)
        # for bar in bar_list:
        #     rts.add(bar[0], bar[1], bar[2])
        self.rts.madd(bar_list)

    def _timeframe_start(self, timeframe):
        switcher = {
            TimeFrame.Minue: datetime.now() - timedelta(days=7),
            TimeFrame.Hour: datetime.now() - timedelta(days=90),
            TimeFrame.Day: datetime.now() - timedelta(days=360),
        }
        dt = switcher.get(timeframe, datetime.now())
        date_string = dt.strftime('%Y-%m-%d')
        return date_string
        # return "2021-02-08"

    def _timeframe_end(self, timeframe):
        dt = datetime.now()
        date_string = dt.strftime('%Y-%m-%d %h:%M:%s')
        return date_string
        # return "2021-02-10"

    def _bar_realtime(self, rts, api, symbol, timeframe):
        ts = TimeStamp()
        key = bar_key(symbol, "close", timeframe)
        startt = ts.get_starttime(timeframe)
        endt = ts.get_endtime(timeframe)
        close_prices = rts.revrange(key, from_time=startt, to_time=endt)
        return close_prices

    def _bar_historical(self, rts, api, symbol, timeframe):
        bar_iter = api.get_bars_iter(
            symbol, timeframe, self._timeframe_start(timeframe), self._timeframe_end(timeframe), limit=10, adjustment='raw')
        return bar_iter

    def redis_get_data(self, api, symbol, timeframe):
        switcher = {
            RedisTimeFrame.REALTIME: self._bar_realtime,
            RedisTimeFrame.MIN1:  self._bar_realtime,
            RedisTimeFrame.MIN2:  self._bar_realtime,
            RedisTimeFrame.MIN5:  self._bar_realtime,
            RedisTimeFrame.DAILY: self._bar_historical
        }
        callMethod = switcher.get(timeframe)
        return callMethod(self.rts, api, symbol, timeframe)

    def _get_active_stocks(self, rts, assets):
        # remove all active stocks
        rts.zrembyrank('active_stocks', 0, -1)
        for asset in assets:
            rts.zadd('active_stocks', 0, assets.symbol)
        print('get active stocks')

    def all_keys(self):
        symbols = []
        for key in self.rts.keys("data_close_0:*"):
            symbol = bytes.decode(key).split(':')[1]
            symbols.append(symbol)
        return symbols
