import pandas as pd
import numpy as np
from datetime import date


class SupportResistanceLines:

    @staticmethod
    def _getSupport(df, i):
        supportPrice = 0
        if df['Low'][i] < df['Low'][i-1] and df['Low'][i] < df['Low'][i+1] and df['Low'][i+1] < df['Low'][i+2] and df['Low'][i-1] < df['Low'][i-2]:
            supportPrice = df['Low'][i]

        return supportPrice

    @staticmethod
    def _getResistance(df, i):
        resistancePrice = 0
        if df['High'][i] > df['High'][i-1] and df['High'][i] > df['High'][i+1] and df['High'][i+1] > df['High'][i+2] and df['High'][i-1] > df['High'][i-2]:
            resistancePrice = df['High'][i]

        return resistancePrice

    def get_support_resistance_lines(self, df):
        allPrices = []
        for i in range(2, df.shape[0] - 2):
            supportPrice = SupportResistanceLines._getSupport(df, i)
            resistantPrice = SupportResistanceLines._getResistance(df, i)
            if supportPrice != 0:
                allPrices.append((i, supportPrice))
            elif resistantPrice != 0:
                allPrices.append((i, resistantPrice))

        # df['Date'] = pd.to_datetime(df.index)
        # df['Date'] = df['Date'].apply(mpl_dates.date2num)
        # df = df.loc[:, ['Date', 'Open', 'High', 'Low', 'Close']]

        # get rid of prices near to one another reduce noise

        mean = np.mean(df['High'] - df['Low'])  # rough estimate of volatility

        allPrices = []

        for i in range(2, df.shape[0] - 2):
            supportPrice = SupportResistanceLines._getSupport(df, i)
            resistantPrice = SupportResistanceLines._getResistance(df, i)
            if supportPrice != 0:
                if np.sum([abs(supportPrice-x) < mean for x in allPrices]) == 0:
                    allPrices.append((i, supportPrice))
            elif resistantPrice != 0:
                if np.sum([abs(resistantPrice-x) < mean for x in allPrices]) == 0:
                    allPrices.append((i, resistantPrice))

        sr_lines = []
        for item in allPrices:
            sr_lines.append((item[0], df.iloc[item[0]].name, item[1]))
        return sr_lines

    def get_overnight_gapper(df, minPrice=0.20, percentGapper=0.05):
        on_gappers = []
        for i in range(0, df.shape[0]-2):
            overnightGapper = 0
            gap = df.iloc[i].Close - df.iloc[i+1].Open
            calcPercent = abs(gap / df.iloc[i].Close)
            if calcPercent >= percentGapper and abs(gap) >= minPrice:
                on_gappers.append((i, df.iloc[i].Close, df.iloc[i].name))
                on_gappers.append((i, df.iloc[i+1].Open, df.iloc[i+1].name))

        return on_gappers

    def calculate_ema(df, days, smoothing=2):
        prices = df['close']
        ema = [sum(prices[:days]) / days]
        for price in prices[days:]:
            ema.append((price * (smoothing / (1 + days))) +
                       ema[-1] * (1 - (smoothing / (1 + days))))
        return ema

    # Create VWAP function
    def calculate_vwap(df):
        v = df['volume'].values
        tp = (df['low'] + df['close'] + df['high']).div(3).values
        return df.assign(vwap=(tp * v).cumsum() / v.cumsum())
