import logging
from redisTSCreateTable import CreateRedisStockTimeSeriesKeys
from redisUtil import AlpacaAccess, AlpacaStreamAccess
from redisPubsub import StreamBarsPublisher, StreamBarsSubscriber, ThreeBarScoreSubscriber
# import alpaca_trade_api as alpaca
# from alpaca_trade_api.stream import Stream
# from alpaca_trade_api.common import URL
# from redistimeseries.client import Client
# from alpaca_trade_api.rest import REST
# from redisTSBars import RealTimeBars


class RealTimeStream:

    def __init__(self):
        # Connect to Redis TimeSeries
        ##
        self.log = logging.getLogger(__name__)
        self.publisher = StreamBarsPublisher()
        self.subscriber = StreamBarsSubscriber()
        self.subscriber.start()
        self.studyThreeBar = ThreeBarScoreSubscriber()
        self.studyThreeBar.start()

    # async def print_trade(t):
    #     print('trade', t)

    # async def print_quote(q):
    #     print('quote', q)

    # async def print_trade_update(tu):
    #     print('trade update', tu)

    # you could leave out the status to also get the inactive ones
    # https://forum.alpaca.markets/t/how-do-i-get-all-stocks-name-from-the-market-into-a-python-list/2070/2
    # https://alpaca.markets/docs/api-documentation/api-v2/assets/#asset-entity

    def setup(self):
        app = CreateRedisStockTimeSeriesKeys()
        app.run()

    def run(self):
        logging.basicConfig(level=logging.INFO)
        stream = AlpacaStreamAccess.Connection()
        # feed = 'sip'  # <- replace to SIP if you have PRO subscription
        # stream = Stream(AlpacaAccess.ALPACA_API_KEY,
        #                 AlpacaAccess.ALPACA_SECRET_KEY,
        #                 base_url=URL(AlpacaAccess.ALPACA_WS),
        #                 data_feed=feed)
        # stream.subscribe_trade_updates(print_trade_update)
        # stream.subscribe_trades(print_trade, 'AAPL')
        # stream.subscribe_quotes(print_quote, 'IBM')
        # stream.subscribe_quotes(print_quote, 'AAPL')
        # stream.subscribe_quotes(print_quote, 'GOOG')

        @stream.on_bar('*')
        async def _(self, bar):
            # print('bar', bar)
            # print('type', type(bar))
            self.publisher.publish(bar)
            # RealTimeBars.redis_add_bar(self.rts, bar)

        @stream.on_status("*")
        async def _(self, status):
            print('status', status)

        stream.run()


if __name__ == "__main__":
    app = RealTimeStream()
    app.setup()
    app.run()


# batch insert
# execute_values(cursor, "INSERT INTO TEST(id, v1, v2) VALUES [(1,2,3), (4,5,6), (7,8,9)]")

# how to use pgcopy
# https://docs.timescale.com/timescaledb/latest/quick-start/python/#step-instantiate-a-copymanager-with-your-target-table-and-column-definition
