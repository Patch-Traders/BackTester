from patch_quant.DataHandlers.alpaca import Alpaca
from patch_quant.EventLoops.backtesting_loop import backTesting
from patch_quant.Portfolios.my_portfolio import myPortfolio
from patch_quant.AbstractClasses.trader import trader

"""
##########################################
This file provides a wrapper for the 
functions that we have implemented so 
far.
##########################################
"""


class __patchQuant():
    def __init__(self):
        self.__portfolio = None
        self.__settings = None
        self.__back_tester = None

    def open_long(self, ticker: str, quantity: int) -> None:
        """
        Opens a quantity of long positions on a specific symbol
        :param ticker: ticker symbol
        :param quantity: quantity to be traded
        """
        execution_day = self.__back_tester.execution_day
        price = execution_day[ticker]['open']
        time_stamp = execution_day[ticker].name
        self.__portfolio.open_long(time_stamp, ticker, quantity, price)

    def close_long(self, ticker: str, quantity:int) -> None:
        """
        Closes a quantity of long positions on a specific symbol
        :param ticker: ticker symbol
        :param quantity: quantity to be traded
        """
        execution_day = self.__back_tester.execution_day
        price = execution_day[ticker]['open']
        time_stamp = execution_day[ticker].name
        self.__portfolio.close_long(time_stamp, ticker, quantity, price)

    def open_short(self, ticker: str, quantity: int) -> None:
        """
        Opens a quantity of short positions on a specific symbol
        :param ticker: ticker symbol
        :param quantity: quantity to be traded
        """

    def close_short(self, ticker: str, quantity:int) -> None:
        """
        Closes a quantity of short positions on a specific symbol
        :param ticker: ticker symbol
        :param quantity: quantity to be traded
        """

    def begin(self, trader_class) -> None:
        """
        Function that begins backtesting
        :param trader_class: This is the class that must be implemented by the user
        """
        trader_object = trader_class()
        self.__back_tester = backTesting(trader_object)
        self.__back_tester.manage_settings()
        self.__settings = self.__back_tester.settings
        self.__portfolio = myPortfolio(self.__settings['Tickers'], self.__settings['Cash'], self.__settings['Slippage'])
        self.__back_tester.set_portfolio(self.__portfolio)
        self.__back_tester.loop()


patchQuant = __patchQuant()
