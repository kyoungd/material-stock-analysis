import logging

import alpaca_trade_api as alpaca
from alpaca_trade_api.stream import Stream
from alpaca_trade_api.common import URL

##
# Connect to Redis TimeSeries
##
log = logging.getLogger(__name__)


async def print_trade(t):
    print('trade', t)


async def print_quote(q):
    print('quote', q)


async def print_trade_update(tu):
    print('trade update', tu)

ALPACA_API_KEY = 'AKAV2Z5H0NJNXYF7K24D'
ALPACA_SECRET_KEY = '262cAEeIRrL1KEZYKSTjZA79tj25XWrMtvz0Bezu'
ALPACA_API_URL = 'api.alpaca.markets'


def main():
    logging.basicConfig(level=logging.INFO)
    feed = 'sip'  # <- replace to SIP if you have PRO subscription
    stream = Stream(ALPACA_API_KEY,
                    ALPACA_SECRET_KEY,
                    base_url=URL('wss://stream.data.alpaca.markets/v2'),
                    data_feed=feed)
    # stream.subscribe_trade_updates(print_trade_update)
    # stream.subscribe_trades(print_trade, 'AAPL')
    stream.subscribe_quotes(print_quote, 'ERYP')
    stream.subscribe_quotes(print_quote, 'AAPL')
    stream.subscribe_quotes(print_quote, 'GOOG')

    @stream.on_bar('*')
    async def _(bar):
        # print('bar', bar)
        # print('type', type(bar))
        print('')

    @stream.on_status("*")
    async def _(status):
        print('status', status)

    stream.run()


if __name__ == "__main__":
    main()

# batch insert
# execute_values(cursor, "INSERT INTO TEST(id, v1, v2) VALUES [(1,2,3), (4,5,6), (7,8,9)]")

# how to use pgcopy
# https://docs.timescale.com/timescaledb/latest/quick-start/python/#step-instantiate-a-copymanager-with-your-target-table-and-column-definition
