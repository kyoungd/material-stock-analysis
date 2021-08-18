##
# Invoke IEX Cloud API to retrieve various stock prices
# and technical indicators and store it in Redis TimeSeries
# Author: Prasanna Rajagopal
##
##
# Here's a sample code for how you can retrieve stock market data from IEX Cloud.
# You will need to register with IEX cloud and get an API key from their website.
# https://iexcloud.io/
# The API Key will have to be copied to the API calls made below in the locations that
# states <Your IEX API Key>
# IEX Cloud has a free tier that allows for a certain number of API calls
# The API documentation for IEX Cloud can be found here:
# https://iexcloud.io/docs/api/
##

import time
from datetime import datetime
from iexfinance.stocks import get_historical_data, get_historical_intraday, Stock
import pandas as pd
import requests
import json

##
# make a connection to Redis TimeSeries
##

# Use the epoch time to convert timestamps to integer values.
dtFmt = '%Y-%m-%d'
epoch = datetime(1970, 1, 1)
intradayPriceList = []

##
# Daily RSI For Goldman Sachs Group
# https://sandbox.iexapis.com/stable/stock/IBM/quote?token=pk_4c4cea17cf834cafadd2a57e5bd7f2cc

dailydtFmt = '%Y-%m-%d %H:%M'
resp = requests.get(
    'https://cloud.iexapis.com/stable/stock/GS/indicator/rsi?range=1d&token=pk_4c4cea17cf834cafadd2a57e5bd7f2cc')
if resp.status_code != 200:
    # This means something went wrong.
    raise Exception('GET /tasks/ {}'.format(resp.status_code))
rsiJSON = resp.json()
chartList = rsiJSON['chart']
indicatorList = rsiJSON['indicator']
RSIIndicatorList = []
##
# Parsing the JSON for Goldman Sachs' RSI and adding the tuple into a list of tuples.
##
for x in range(5, len(chartList)):
    rsiDate = str(chartList[x]['date'])
    rsiTime = str(chartList[x]['minute'])
    rsiDateTime = rsiDate + ' ' + rsiTime
    newdt = datetime.utcfromtimestamp(
        (datetime.strptime(str(rsiDateTime), dailydtFmt) - epoch).total_seconds())
    ##
    # Creating a tuple of each time series entry.
    # Converting regular string timestamp that was created above to integer.
    ##
    eachIntradayPrice = ('DAILYRSI:GS', int((datetime.strptime(
        str(rsiDateTime), dailydtFmt) - epoch).total_seconds()*1000), indicatorList[0][x])
    ##
    # Add each tuple to the list
    ##
    RSIIndicatorList.append(eachIntradayPrice)
##
# Adding the list of tuples to Redis TimeSeries database using the MADD command
##
print('RSIIndicatorList: ' + RSIIndicatorList)
# rts.madd(RSIIndicatorList)

##
# Intraday Stock Prices For Goldman Sachs Group
##
# Date for which intraday stock prices will be retrieved.
# Change it as you deem necessary
firstWkDate = datetime(2020, 11, 13)
intraDayPricesDF = get_historical_intraday(
    "GS", firstWkDate, output_format='pandas', token="<Your IEX API Key>")

dtFmt = '%Y-%m-%d %H:%M:%S'
epoch = datetime(1970, 1, 1)
intradayPriceList = []
for row in intraDayPricesDF.itertuples():
    eachIntradayPrice = ('INTRADAYPRICES:GS', int(
        (datetime.strptime(str(row[0]), dtFmt) - epoch).total_seconds()), row[3])
    intradayPriceList.append(eachIntradayPrice)
##
# Adding the list of tuples to Redis TimeSeries database using the MADD command
##

print('intradayPriceList: ' + intradayPriceList)
