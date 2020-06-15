import matplotlib.pyplot as plt
#import alpaca_trade_api as tradeapi
from polygon import RESTClient
from backtest import backTest
import os
#TODO TEST EVERYTHING AND CLEAN CODE
def TradingSystem(prices):
    """
    This functioned is called every day with the new price data made available to it
    :param prices: this is a list of dictionaries with index zero being the oldest price data
    """
    global a
    if a == 0:
        back_tester.buy('AAPL', 1)
        a = 1



if __name__ == '__main__':
    global a
    a = 0
    tickers = ['AAPL']
    back_tester = backTest('2019-01-16', '2020-02-13', 5, 1000, tickers, TradingSystem)
    back_tester.trade()
    counter = 1
