from patch_quant.AbstractClasses.portfolio import portfolio
import random
import pandas as pd

class myPortfolio(portfolio):
    """
    # TODO should we execute OrderEvents (will probably help in the long run)
    """

    def __init__(self, tickers: list, cash: int , slippage: float):
        """
        :param cash: initial amount of tradeable cash
        """
        self.__tickers = tickers
        self.__cash = cash
        self.__original_value = cash
        self.__market_value = cash
        self.__slippage = slippage
        self.__order_log = dict()
        self.__current_holdings = dict()
        for ticker in self.__tickers:
            self.__current_longs[ticker]= {'quantity': 0, 'value': 0}
            #self.__current_shorts[ticker]= {'quantity': 0, 'value': 0}
            self.__order_log[ticker] = pd.DataFrame(columns=[
                'action','quantity','execution_price','order_value'])

    # TODO Should the time_stamp be a datetime object?
    # TODO consider making all order methods take dataframe of data to simply implementation of strategy
    def open_long(self, time_stamp: str, ticker: str, quantity: int, price: float) -> None:
        """
        Opens a quantity of long positions on a specific symbol
        :param time_stamp: Time stamp of order
        :param ticker: ticker symbol
        :param quantity: quantity to be traded
        :param price: Execution price, pre slippage calculations
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


    def close_long(self, time_stamp:str, ticker:str, quantity:int, price:int) -> None:
        """
        Closes a quantity of long positions on a specific symbol
        :param time_stamp: time stamp of order
        :param ticker: ticker symbol
        :param quantity: quantity to be traded
        :param price: execution price of order
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

    #TODO How can shorts be represented and calculated? Do you need to store the purchase price?
    def open_short(self, ticker: str, quantity: int) -> None:
        """
        Opens a quantity of short positions on a specific symbol
        :param ticker: ticker symbol
        :param quantity: quantity to be traded
        """
        raise NotImplementedError("Error: Implementation for 'buy' is required")

    def close_short(self, ticker: str, quantity:int) -> None:
        """
        Closes a quantity of short positions on a specific symbol
        :param ticker: ticker symbol
        :param quantity: quantity to be traded
        """
        raise NotImplementedError("Error: Implementation for 'sell' is required")

    def __execution_price(self, price: int) -> float:
        """
        Estimates the actual execution price of a transaction based on a static slippage factor of .02
        :param price: price of security transacted
        """

        min_price = price - (price * self.__slippage)
        max_price = price + (price * self.__slippage)

        execution_price = random.uniform(min_price, max_price)

        return execution_price

    def __update_order_log(self, ticker:str, time_stamp:str, execution_price:float, quantity:int, action:str) -> None:
        """
        Updates the order log for all orders executed in the portfolio
        :param ticker: ticker symbol
        :param time_stamp: time of trade
        :param execution_price: price of order execution
        :param quantity: quantity of security traded
        :param action: e.g buy, sell, short
        """

        new_entry = [action, quantity, execution_price, quantity*execution_price]
        self.__order_log[ticker].loc[pd.to_datetime(time_stamp)] = new_entry

    @property
    def order_log(self) -> dict:
        """
        Getter for giving the trader the order log
        """
        return self.__order_log

    def update_market_value(self, daily_data: dict, day_time: str) -> int:
        """
        Updates the market value of the portfolio. Utilized in the backtesting loop.
        :param daily_data: dictionary of tickers and their corresponding data frame
        :param day_time: e.g close or open
        """
        self.__market_value = 0
        for ticker in self.__tickers:
            new_price = daily_data[ticker][day_time]
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
    def cash(self) -> int:
        """
        Should return liquidity
        """
        return self.__cash

    @property
    def current_holdings(self) -> dict:
        """
        Should return current holdings
        """
        return self.__current_holdings

    @property
    def market_value(self) -> float:
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
