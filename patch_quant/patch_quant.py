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


class patchQuant():
    def __init__(self):
        self.__portfolio = None
        self.__settings = None

    def open_long(self, ticker: str, quantity: int) -> None:
        self.__portfolio.open_long()
        """
        Opens a quantity of long positions on a specific symbol
        :param ticker: ticker symbol
        :param quantity: quantity to be traded
        """

    def close_long(self, ticker: str, quantity:int) -> None:
        """
        Closes a quantity of long positions on a specific symbol
        :param ticker: ticker symbol
        :param quantity: quantity to be traded
        """

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
        :param traderObj: This is the class that must be implemented by the user
        """
        trader_object = trader_class()
        back_tester = backTesting(trader_object)
        self.__settings = back_tester.manage_settings()
        self.__portfolio = myPortfolio(self.__settings['Tickers'], self.__settings['Cash'], self.__settings['Slippage'])




pq = patchQuant()
