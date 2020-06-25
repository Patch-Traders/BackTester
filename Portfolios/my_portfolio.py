from AbstractClasses.portfolio import portfolio
import random
import pandas as pd
import numpy as np

class myPortfolio(portfolio):
    """
    # TODO should we execute OrderEvents (will probably help in the long run)
    # TODO make sure in backtesting_loop to update the portfolio after every loop with the current pricings
    # TODO update portfolio value at the beginning of the day and then initiate buy orders immediately afterwards
    """

    def __init__(self, tickers:list, cash:int):
        """
        #TODO consider other parameters that are useful for initialization
        :param cash: initial amount of tradeable cash
        """
        self.__tickers = tickers
        self.__cash = cash
        self.__original_value = cash
        self.__market_value = cash
        self.__slippage = .02
        self.__order_log = dict() #TODO is a dictionary the best data structure / implement
        self.__current_holdings = dict()

        # initialize all holdings as zero
        for ticker in self.__tickers:
            self.__current_holdings[ticker]= {'quantity': 0, 'value': 0}
            self.__order_log[ticker] = pd.DataFrame(columns=[
                'action','quantity','execution_price','order_value'])


    # TODO consider making all order methods take dataframe of data to simply implementation of strategy
    def buy(self, time_stamp:str, ticker:str, quantity:int, price:int) -> None:
        """
        Executes a buy order and changes portfolio holdings. Only executed at the beginning of the day.
        :param data: given in the ISO 8601 Format specification YYYY-MM-DD
        :param ticker: ticker symbol
        :param quantity: quantity to be traded
        """
        if  self.__cash < price*quantity:
            raise Exception('Error: There is not enough cash in portfolio to execute your trade')
        if ticker not in self.__current_holdings:
            raise Exception(f'Error: {ticker} is an invalid ticker symbol')

        execution_price = self.__execution_price(price)

        buy_value = quantity*execution_price
        self.__current_holdings[ticker]['quantity'] += quantity
        self.__current_holdings[ticker]['value'] += buy_value

        self.__market_value += buy_value
        self.__cash -= buy_value
        self.__update_order_log(ticker, time_stamp, execution_price, quantity, 'buy')


    def sell(self, time_stamp:str, ticker:str, quantity:int, price:int) -> None:
        """
        Executes a sell order and changes portfolio holdings. Only executed at the beginning of the day.
        :param data: given in the ISO 8601 Format specification YYYY-MM-DD
        :param ticker: ticker symbol
        :param quantity: quantity to be traded
        """

        if ticker not in self.__current_holdings:
            raise Exception(f'Error: {ticker} is an invalid ticker symbol')
        if self.__current_holdings[ticker]['quantity'] < quantity:
            raise Exception(f'Error: You do not have enough shares of {ticker}')

        execution_price = self.__execution_price(price)

        sell_value = quantity*execution_price
        self.__current_holdings[ticker]['quantity'] -= quantity
        self.__current_holdings[ticker]['value'] -= sell_value

        self.__market_value -= sell_value
        self.__cash += sell_value
        self.__update_order_log(ticker, time_stamp, execution_price, quantity, 'sell')

    def __execution_price(self, price: int) -> float:
        """
        Estimates the actual execution price of a transaction based on a static slippage factor of .02
        :param price: price of security transacted
        """
        min_price = price - (price * self.__slippage)
        max_price = price + (price * self.__slippage)

        execution_price = random.uniform(min_price, max_price)

        return execution_price

    def __update_order_log(self, ticker:str, time_stamp:str, execution_price:float, quantity:int, action:str):
        """
        Updates order self.__order_log for evaluating portfolio performance
        :return: None
        """
        # new_entry = {'action':action, 'quantity':quantity, 'execution_price':execution_price, 'order_value': quantity*execution_price}
        new_entry = [action, quantity, execution_price, quantity*execution_price]
        self.__order_log[ticker].loc[pd.to_datetime(time_stamp)] = new_entry


    @property
    def order_log(self):
        return self.__order_log

    def update_market_value(self, daily_data: dict, day_time: str) -> int:
        """
        Updates the market value of the portfolio. Utilized in the backtesting loop.
        :param daily_data: dictionary of tickers and their corresponding data frame
        :param day_time: e.g close or open
        """
        self.__market_value = 0
        for ticker in self.__tickers:
            new_price = daily_data[ticker].iloc[-1][day_time]
            quantity = self.__current_holdings[ticker]['quantity']

            self.__current_holdings[ticker]['value'] = new_price * quantity
            self.__market_value += new_price * quantity


    def net_return(self) -> int:
        """
        calculates the net return of the portfolio and return the percentage as a decimal
        """
        returns = ((self.__market_value + self.__cash)/self.__original_value) - 1
        return returns

    @property
    def cash(self):
        """
        Should return liquidity
        """
        return self.__cash

    @property
    def current_holdings(self):
        """
        Should return current holdings
        """
        return self.__current_holdings

    @property
    def market_value(self):
        """
        Returns market value of the portfolio
        """
        return self.__market_value

    def liquidity(self):
        """
        returns lqiuidity
        """
        pass

    def leverage(self):
        """
        Returns leverage
        """
        pass

    def plot_performance(self):
        """
        Need to plot holding_history
        Dictionary where each ticker is aligned with a dataframe
        Row/Index: timestamp
        Columns: quantity, order_price, total_value
        """
        pass