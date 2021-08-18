# Data Model for Stock Prices and Technical Indicators (using RedisTimeSeries)

This repository demonstrate a sample code for using RedisTimeSeries to store, aggregate/query stock prices, technical indicators and time-series data sets used by investors. These sets of scripts create various timeseries for prices and indicators. It shows how to create aggregations on top of the raw time series, and demonstrate how easily bulk time series can be ingested and queried using various RedisTimeSeries commands.

The blog that discusses this code in detail and walks through the Redis datamodel and the various Redis TimeSeries commands can be found in the references section below.

## Pre-requisite

There are multiple services that offer stock prices and technical indicator data. The code presented here uses data from https://iexcloud.io/
Get a trial account in iexcloud.

### Clone this Repository

```
git clone https://github.com/redis-developer/redis-datasets
cd redis-datasets/redistimeseries/StockPrice
```

### Install Python3

Ensure that python3 and pip3 is installed in your system.

### Install Prerequisite software

Using pip3 to install redistimeseries, iexfinance & pandas software.

```
pip3 install -r requirements.txt
```

Once you have the Redis TimeSeries container up and running you can connect to the server (make sure you have the right IP address or hostname) using Python script:

## Running the scripts

Before running these scripts, ensure that you modify host and port number(6379) for Redis as per your infrastructure setup.

```
 % python3 redisTSCreateKeysSample.py
 % python3 redisTimeSeriesQuerySamples.py
```

## Running RedisTimeSeries in a Docker Container

```
sudo service redis stop
sudo docker run -p 6379:6379 -it --rm redislabs/redistimeseries
redis-cli
```

# Generate test data

python3 redisTestDataGenerator.
python3 redis3bar.py

## Scanning the Keys

```
127.0.0.1:6379> scan 0
1) "15"
2)  1) "INTRADAYPRICES15MINSTDP:GS"
    2) "DAILYRSI:CAT"
    3) "DAILYRSI15MINMAX:GS"
    4) "DAILYRSI15MINMIN:GS"
    5) "INTRADAYPRICES15MINRNG:GS"
    6) "INTRADAYPRICES15MINMIN:GS"
    7) "DAILYRSI15MINLAST:GS"
    8) "INTRADAYPRICES:GS"
    9) "DAILYRSI:GS"
   10) "INTRADAYPRICES15MINMAX:GS"
   11) "DAILYRSI15MINFIRST:GS"
   12) "DAILYRSI15MINRNG:GS"
127.0.0.1:6379> type INTRADAYPRICES15MINSTDP:GS
TSDB-TYPE
127.0.0.1:6379
```

## References

- [Build Your Financial Application on RedisTimeSeries](https://redislabs.com/blog/build-your-financial-application-on-redistimeseries/)
- [Why the Financial Industry Needs Redis Enterprise](https://redislabs.com/blog/why-the-financial-industry-needs-redis-enterprise/)

## alpaca returns

quote Quote({ 'ask_exchange': 'U',
'ask_price': 20.53,
'ask_size': 1,
'bid_exchange': 'T',
'bid_price': 20.52,
'bid_size': 1,
'conditions': ['R'],
'symbol': 'DNB',
'tape': 'A',
'timestamp': 1627487138544951592})
trade Trade({ 'conditions': [' ', 'F', 'I'],
'exchange': 'T',
'id': 62879500359534,
'price': 20.52,
'size': 10,
'symbol': 'DNB',
'tape': 'A',
'timestamp': 1627487138544984019})
trade Trade({ 'conditions': [' ', 'I'],
'exchange': 'T',
'id': 62879500359535,
'price': 20.52,
'size': 28,
'symbol': 'DNB',
'tape': 'A',
'timestamp': 1627487138545036660})
quote Quote({ 'ask_exchange': 'T',
'ask_price': 20.53,
'ask_size': 2,
'bid_exchange': 'P',
'bid_price': 20.52,
'bid_size': 1,
'conditions': ['R'],
'symbol': 'DNB',
'tape': 'A',
'timestamp': 1627487138545020147})
quote Quote({ 'ask_exchange': 'P',
'ask_price': 19.32,
'ask_size': 1197,
'bid_exchange': 'U',
'bid_price': 19.31,
'bid_size': 703,
'conditions': ['R'],
'symbol': 'QID',
'tape': 'B',
'timestamp': 1627487138545929216})

bar Bar({ 'close': 136.02,
'high': 136.06,
'low': 136.0,
'open': 136.04,
'symbol': 'ALLE',
'timestamp': 1627493640000000000,
'trade_count': 22,
'volume': 712,
'vwap': 136.030153})
bar Bar({ 'close': 15.83,
'high': 15.86,
'low': 15.8218,
'open': 15.825,
'symbol': 'TLRY',
'timestamp': 1627493640000000000,
'trade_count': 327,
'volume': 64326,
'vwap': 15.841783})
bar Bar({ 'close': 53.02,
'high': 53.03,
'low': 53.0,
'open': 53.03,
'symbol': 'TNL',
'timestamp': 1627493640000000000,
'trade_count': 63,
'volume': 2730,
'vwap': 53.02548})
bar Bar({ 'close': 46.09,
'high': 46.1199,
'low': 46.09,
'open': 46.095,
'symbol': 'UBER',
'timestamp': 1627493640000000000,
'trade_count': 101,
'volume': 9629,
'vwap': 46.10465})
bar Bar({ 'close': 93.615,
'high': 94.13,
'low': 93.615,
'open': 94.01,
'symbol': 'BILI',
'timestamp': 1627493640000000000,
'trade_count': 257,
'volume': 16913,
'vwap': 93.93039})
bar Bar({ 'close': 8.565,
'high': 8.57,
'low': 8.45,
'open': 8.4584,
'symbol': 'BTBT',
'timestamp': 1627493640000000000,
'trade_count': 602,
'volume': 213907,
'vwap': 8.510506})

curl --header 'Accept: text/event-stream' https://cloud-sse.iexapis.com/stable/stocksUS\?token\=pk_4c4cea17cf834cafadd2a57e5bd7f2cc
curl --header 'Accept: text/event-stream' https://cloud-sse.iexapis.com/stable/stocksUS?token=pk_4c4cea17cf834cafadd2a57e5bd7f2cc

[
(1603704600, 1.75999999999999),
(1603705500, 0.775000000000006),
(1603706400, 0.730000000000018),
(1603707300, 0.449999999999989),
(1603708200, 0.370000000000005),
(1603709100, 1.01000000000002),
(1603710000, 0.490000000000009),
(1603710900, 0.89500000000001),
(1603711800, 0.629999999999995),
(1603712700, 0.490000000000009),
(1603713600, 0.27000000000001)
]
