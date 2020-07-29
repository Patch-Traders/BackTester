from patch_quant.EventLoops.backtesting_loop import backTesting
from patch_quant.Portfolios.my_portfolio import myPortfolio
import plotly.graph_objects as go

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
        self.__full_data_set = None

    def initialize(self, trader_class) -> None:
        """
        Pulls trading data specified by trading settings and
        prepares portfolio based on trading settings
        :param trader_class: This is the class that must be implemented by the user
        """

        # initializes backtester and specified settings
        self.__back_tester = backTesting(trader_class())
        self.__back_tester.manage_settings()
        self.__settings = self.__back_tester.settings

        # initializes a portfolio for the backtester to utilize
        self.__portfolio = myPortfolio(self.__settings['Tickers'], self.__settings['Cash'], self.__settings['Slippage'])
        self.__back_tester.set_portfolio(self.__portfolio)

        # retrieves full data set for graphing
        self.__full_data_set = self.__back_tester.full_data_set

    def begin(self) -> None:
        """
        Begins looping through trading strategy
        :param trader_class: This is the class that must be implemented by the user
        """
        self.__back_tester.loop()

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

        execution_day = self.__back_tester.execution_day
        price = execution_day[ticker]['open']
        time_stamp = execution_day[ticker].name
        self.__portfolio.open_short(time_stamp, ticker, quantity, price)

    def close_short(self, ticker: str, quantity:int) -> None:
        """
        Closes a quantity of short positions on a specific symbol
        :param ticker: ticker symbol
        :param quantity: quantity to be traded
        """
        execution_day = self.__back_tester.execution_day
        price = execution_day[ticker]['open']
        time_stamp = execution_day[ticker].name
        self.__portfolio.close_short(time_stamp, ticker, quantity, price)

    def candlestick(self, start_date:str, end_date:str, *tickers):
        """
        Creates candlestick plot for each ticker symbol in the specified time period
        Dates must be given in the ISO 8601 Format specification YYYY-MM-DD

        :param tickers: variable length parameter of tickers to visualize
        :param start_date: starting data of graph
        :param end_date: ending date of graph
        """

        for ticker in tickers:
            stock = self.__full_data_set[ticker].loc[start_date:end_date]
            fig = go.Figure(data=[go.Candlestick(
                x = stock.index,
                open = stock['open'],
                high = stock['high'],
                low = stock['low'],
                close = stock['close'],
            )])

            fig.update_layout(
                title = ticker,
                yaxis_title = 'Price'
            )

            fig.show()

    def timeseries(self, start_date:str, end_date:str, *tickers):
        """
        Creates timeseries plot for each ticker symbol in the specified time period
        Dates must be given in the ISO 8601 Format specification YYYY-MM-DD

        :param tickers: variable length parameter of tickers to visualize
        :param start_date: starting data of graph
        :param end_date: ending date of graph
        """

        for ticker in tickers:

            stock = self.__full_data_set[ticker].loc[start_date:end_date]
            fig = go.Figure(data=[go.Scatter(
                x = stock.index,
                y = stock['high']
            )])

            fig.update_layout(
                title=ticker,
                yaxis_title='High Price',
            )

            fig.show()

    # TODO create default values for beginning and ending dates ( default arguments are only evaluated when function defined not called)
    def portfolio_performance(self, begin_date:str, end_date:str ):
        """
        Graphs the performance of the portfolio over the specified time period
        """
        self.__portfolio.graph_performance(begin_date, end_date)

    """
    Accessor Methods
    """
    @property
    def cash(self):
        return self.__portfolio.cash

    @property
    def order_log(self):
        return self.__portfolio.order_log

    @property
    def market_value(self):
        return self.__portfolio.market_value

patchQuant = __patchQuant()
