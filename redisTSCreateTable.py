##
# Create various Redis TimeSeries for storing stock prices
# and technical indicators
# Author: Prasanna Rajagopal
##

import alpaca_trade_api as alpaca
from alpaca_trade_api.rest import TimeFrame
from datetime import datetime, timedelta
from redisUtil import TimeStamp, bar_key, RedisTimeFrame, AlpacaAccess
from redistimeseries.client import Client


# def bar_key(symbol, suffix, time_frame):
#     return "data_" + suffix + "_" + time_frame + ":" + symbol


class CreateRedisStockTimeSeriesKeys:

    def __init__(self, rts=None):
        if (rts == None):
            self.rts = Client(host='127.0.0.1', port=6379)
        else:
            self.rts = rts
        api = alpaca.REST(
            AlpacaAccess.ALPACA_API_KEY, AlpacaAccess.ALPACA_SECRET_KEY, AlpacaAccess.ALPACA_API_URL)
        self.assets = api.list_assets(status='active')

    def _createSymbolItem(self, rts, symbol, suffix, aggr, index, description, companyName, timeframe):
        name0 = bar_key(symbol, suffix, timeframe)
        retention = TimeStamp.retention_in_ms(timeframe)
        labels0 = {'SYMBOL': symbol, 'DESC': 'RELATIVE_STRENGTH_INDEX', 'INDEX': 'DJIA',
                   'TIMEFRAME': timeframe.name, 'INDICATOR': aggr}
        rts.create(name0, retention_msecs=retention,
                   labels=labels0)
        return name0

    def _createSymbol(self, rts, symbol, suffix, aggr, index, description, companyName):
        name0 = self._createSymbolItem(rts, symbol,  suffix, aggr,
                                       index, description, companyName, RedisTimeFrame.REALTIME)
        name1 = self._createSymbolItem(rts, symbol,  suffix, aggr,
                                       index, description, companyName, RedisTimeFrame.MIN1)
        name2 = self._createSymbolItem(rts, symbol,  suffix, aggr,
                                       index, description, companyName, RedisTimeFrame.MIN2)
        name5 = self._createSymbolItem(rts, symbol,  suffix, aggr,
                                       index, description, companyName, RedisTimeFrame.MIN5)

        rts.createrule(name0, name1, aggr, 60*1000)
        rts.createrule(name0, name2, aggr, 2*60*1000)
        rts.createrule(name0, name5, aggr, 5*60*1000)

    def _get_new_assets(self, rts, active_assets):
        new_symbols = []
        for asset in active_assets:
            key = bar_key(asset.symbol, "volume", RedisTimeFrame.REALTIME)
            if (asset.tradable):
                try:
                    rts.get(key)
                except:
                    new_symbols.append(asset)
            # if rts.get(key) is None:
            #     new_symbols.append(asset)
        return new_symbols

    def _createRedisStockSymbol(self, rts, symbol, index, description, companyName):
        self._createSymbol(rts, symbol, "high", "max",
                           index, description, companyName)
        self._createSymbol(rts, symbol, "low", "min",
                           index, description, companyName)
        self._createSymbol(rts, symbol, "open", "first",
                           index, description, companyName)
        self._createSymbol(rts, symbol, "close", "last",
                           index, description, companyName)
        self._createSymbol(rts, symbol, "volume", "sum",
                           index, description, companyName)

    def run(self):
        new_assets = self._get_new_assets(self.rts, self.assets)
        for asset in new_assets:
            print(f"{asset.symbol}  \t{asset.name}")
            self._createRedisStockSymbol(
                self.rts, asset.symbol, '', '', asset.name)


# def get_bar_list(data, timeframe):
#     ts = data.timestramp
#     bar_list = []
#     bar_list.append(bar_key(data.symbol, "close", timeframe), ts, data.close)
#     bar_list.append(bar_key(data.symbol, "high", timeframe), ts, data.high)
#     bar_list.append(bar_key(data.symbol, "low", timeframe), ts, data.low)
#     bar_list.append(bar_key(data.symbol, "open", timeframe), ts, data.open)
#     bar_list.append(bar_key(data.symbol, "volume", timeframe), ts, data.volumn)
#     return bar_list


# def redis_add_bar(rts, data):
#     timeframe = "0"
#     bar_list = get_bar_list(data, timeframe)
#     rts.madd(bar_list)


# def timeframe_start(timeframe):
#     switcher = {
#         TimeFrame.Minue: datetime.now() - timedelta(days=7),
#         TimeFrame.Hour: datetime.now() - timedelta(days=90),
#         TimeFrame.Day: datetime.now() - timedelta(days=360),
#     }
#     dt = switcher.get(timeframe, datetime.now())
#     date_string = dt.strftime('%Y-%m-%d')
#     return date_string
#     # return "2021-02-08"


# def timeframe_end(timeframe):
#     dt = datetime.now()
#     date_string = dt.strftime('%Y-%m-%d %h:%M:%s')
#     return date_string
#     # return "2021-02-10"


# def backfill_bar(rts, api, symbol, timeframe):
#     bar_iter = api.get_bars_iter(
#         symbol, timeframe, timeframe_start(timeframe), timeframe_end(timeframe), limit=10, adjustment='raw')
#     for bar in bar_iter:
#         bar_list = get_bar_list(bar.symbol, timeframe)
#         rts.madd(bar_list)


# def backfill_bars(rts, api, symbol):
#     backfill_bar(rts, api, symbol, TimeFrame.Day)


# def get_active_stocks(rts, assets):
#     # remove all active stocks
#     rts.zrembyrank('active_stocks', 0, -1)
#     for asset in assets:
#         rts.zadd('active_stocks', 0, assets.symbol)
#     print ('get active stocks')
