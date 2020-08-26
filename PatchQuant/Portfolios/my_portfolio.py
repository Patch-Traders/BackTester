from PatchQuant.AbstractClasses.portfolio import portfolio
import random
import pandas as pd
import plotly.graph_objects as go

class myPortfolio(portfolio):
    """
    Executes long, shorts, visualizations, and history of actions for the given trading strategy
    """

    def __init__(self, tickers: list, cash: int , slippage: float):
        """
        :param tickers: array of tickers in portfolio
        :param cash: initial amount of tradeable cash
        "param slippage: slippage factor between 0 and 1
        """

        # initialize parameter values
        self.__tickers = tickers
        self.__original_value = cash
        self.__slippage = slippage


        self.__cash = cash  # cash on hand
        self.__short_collateral = 0 # necessary collateral to cover shorts
        self.__market_value = cash # market value of all positions if liquidated today

        # historical logs
        self.__order_log = dict()
        self.__returns_log = pd.DataFrame(columns=['value'])

        # tracking long and short positions
        self.__current_longs = dict()
        self.__current_shorts = dict()

        # initialize positions and order_log
        for ticker in self.__tickers:
            self.__current_longs[ticker]= {'quantity': 0, 'market_value': 0}
            self.__current_shorts[ticker]= {}
            self.__order_log[ticker] = pd.DataFrame(columns=[
                'action','quantity','execution_price','order_value'])


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
        if ticker not in self.__current_longs:
            raise Exception(f'Error: {ticker} is an invalid ticker symbol')

        execution_price = self.__execution_price(price)

        buy_value = quantity*execution_price
        self.__current_longs[ticker]['quantity'] += quantity
        self.__current_longs[ticker]['market_value'] += buy_value

        self.__market_value += buy_value
        self.__cash -= buy_value
        self.__update_order_log(ticker, time_stamp, execution_price, quantity, 'open_long')

    def close_long(self, time_stamp:str, ticker:str, quantity:int, price: float) -> None:
        """
        Closes a quantity of long positions on a specific symbol
        :param time_stamp: time stamp of order
        :param ticker: ticker symbol
        :param quantity: quantity to be traded
        :param price: execution price of order
        """
        if ticker not in self.__current_longs:
            raise Exception(f'Error: {ticker} is an invalid ticker symbol')
        if self.__current_longs[ticker]['quantity'] < quantity:
            raise Exception(f'Error: You do not have enough shares of {ticker}')

        execution_price = self.__execution_price(price)

        sell_value = quantity*execution_price
        self.__current_longs[ticker]['quantity'] -= quantity
        self.__current_longs[ticker]['market_value'] -= sell_value

        self.__market_value -= sell_value
        self.__cash += sell_value
        self.__update_order_log(ticker, time_stamp, execution_price, quantity, 'close_long')

    def open_short(self, time_stamp:str, ticker: str, quantity: int, price: float) -> None:
        """
        Opens a quantity of short positions on a specific symbol
        :param time_stamp: time of order execution
        :param ticker: ticker symbol
        :param quantity: quantity to be traded
        :param price: price of ticker
        """

        if  self.__cash < price*quantity:
            raise Exception('Error: There is not enough cash in portfolio to be provided as collateral')
        if ticker not in self.__current_longs:
            raise Exception(f'Error: {ticker} is an invalid ticker symbol')

        execution_price = self.__execution_price(price)
        sell_short_value = quantity * execution_price

        self.__current_shorts[ticker][time_stamp] = {
            'execution_price': execution_price, 'quantity':quantity, 'market_value': 0}

        self.__cash -= sell_short_value
        self.__short_collateral += sell_short_value
        self.__update_order_log(ticker, time_stamp, execution_price, quantity, 'open_short')

    def close_short(self, time_stamp:str, ticker: str, quantity: int, price: float) -> None:
        """
        # TODO consider other methods for prioritizing closing short positions
        Closes a quantity of short positions on a specific symbol
        "param time_stamp: time of order execution
        :param ticker: ticker symbol
        :param quantity: quantity to be traded
        :param price: price of ticker
        """

        # TODO add exceptions concerning the quantity wanted to short
        if not self.__current_shorts:
            raise Exception('Error: There are no open shorts for given ticker')

        original_quantity = quantity
        sorted_shorts = sorted(self.__current_shorts[ticker].items(), key = lambda x: x[1]['execution_price'], reverse=True)
        for short in sorted_shorts:

            if not quantity:
                break

            # fulfilling most profitable short positions first
            shorted_quantity = short[1]['quantity']
            shorted_price = short[1]['execution_price']
            shorted_date = short[0]

            # if desired amount to short greater than most profitable position
            if quantity >= shorted_quantity:
                quantity -= shorted_quantity
                del self.__current_shorts[ticker][shorted_date]

            # desired amount to short less than most profitable shorts
            else:
                self.__current_shorts[ticker][shorted_date]['quantity'] -= quantity
                quantity = 0


            # updating cash on hand and cash needed to cover shorts
            self.__cash += (shorted_price * shorted_quantity) - (price * quantity)
            self.__short_collateral -= (shorted_price * shorted_quantity)


        self.__update_order_log(ticker, time_stamp, price, original_quantity, 'close_short')


    def __execution_price(self, price: int) -> float:
        """
        Estimates the actual execution price of a transaction based on slippage factor
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
        :param action: e.g open_long, close_long, open_short, close_short
        """

        new_entry = [action, quantity, execution_price, quantity*execution_price]
        self.__order_log[ticker] = self.__order_log[ticker].append(
            pd.DataFrame([new_entry], index=[time_stamp], columns=self.__order_log[ticker].columns)
        )


    def update_market_value(self, daily_data: dict, bar_time: str) -> int:
        """
        Updates the market value of the portfolio. Utilized in the back testing loop.
        :param daily_data: dictionary of tickers and their corresponding data frame
        :param day_time: e.g close or open
        """
        self.__market_value = 0

        for ticker in self.__tickers:

            current_price = daily_data[ticker][bar_time]

            # recalculate market value of longs
            num_longs = self.__current_longs[ticker]['quantity']
            self.__current_longs[ticker]['market_value'] = current_price * num_longs
            self.__market_value += current_price * num_longs

            # market value of shorts
            for time, order in self.__current_shorts[ticker].items():

                # sell value at time of short and current market price of buy back
                original_sell_value = order['execution_price'] * order['quantity']
                current_buyback_value = current_price * order['quantity']

                order['market_value'] = original_sell_value - current_buyback_value
                self.__market_value += order['market_value']

        # add new input for order log with time and values
        time_stamp = daily_data[self.__tickers[0]].name
        self.__returns_log.loc[pd.to_datetime(time_stamp)] = [self.__market_value + self.__cash + self.__short_collateral]


    def graph_performance(self, start_date: str, end_date: str):
        """
        Graphs the performance over the specified time period
        :param start_date:
        :param end_date:
        """

        # time period trader wants to visualize portfolio performance over
        sub_set = self.__returns_log.loc[start_date:end_date]

        # figure to make timeseries graph of portfolio performance
        fig = go.Figure(data=[go.Scatter(
            x=sub_set.index,
            y=sub_set['value']
        )])

        fig.update_layout(
            title='Portfolio Performance',
            yaxis_title='Value'
        )

        fig.show()

    def net_return(self) -> int:
        """
        Calculates the net return of the portfolio and return the percentage as a decimal
        """
        returns = ((self.__market_value + self.__cash)/self.__original_value) - 1
        return returns



    @property
    def order_log(self) -> dict:
        """
        Getter for giving the trader the order log
        """
        return self.__order_log

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
        return self.__current_longs

    @property
    def market_value(self) -> float:
        """
        Returns market value of the portfolio
        """
        return self.__market_value

    @property
    def short_positions(self, *tickers):
        """
        Returns all short positions to the user
        """
        pass

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

