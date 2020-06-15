import os
from polygon import RESTClient
import datetime
from portfolio import portfolio

"""
    Current Idea for flow of trades and information
    -instantiate object with settings
    -call beginTrading
    -begin trading calls the user defined trading function every day passing in the requested data
    -User makes calls to trade function
    -function attempts to execute specified trade at the current time instance
    -if succesfully executed the system returns some data 
"""


class backTest:
    """
    This class provides a structured way for accessing data and executing trades
    """
    __NYSE_HOLIDAYS = list(map(datetime.date.fromisoformat, ['2012-01-02', '2012-01-16', '2012-02-20', '2012-04-06',
                                                             '2012-05-28', '2012-07-04', '2012-09-03', '2012-11-22',
                                                             '2012-12-25', '2013-01-01', '2013-01-21', '2013-02-18',
                                                             '2013-03-29', '2013-05-27', '2013-07-04', '2013-09-02',
                                                             '2013-11-28', '2013-12-25', '2014-01-01', '2014-01-20',
                                                             '2014-02-17', '2014-04-18', '2014-05-26', '2014-07-04',
                                                             '2014-09-01', '2014-11-27', '2014-12-25', '2015-01-01',
                                                             '2015-01-19', '2015-02-16', '2015-04-03', '2015-05-25',
                                                             '2015-07-03', '2015-09-07', '2015-11-26', '2015-12-25',
                                                             '2016-01-01', '2016-01-18', '2016-02-15', '2016-03-25',
                                                             '2016-05-30', '2016-07-04', '2016-09-05', '2016-11-24',
                                                             '2016-12-26', '2017-01-02', '2017-01-16', '2017-02-20',
                                                             '2017-04-14', '2017-05-29', '2017-07-04', '2017-09-04',
                                                             '2017-11-23', '2017-12-25', '2018-01-01', '2018-01-15',
                                                             '2018-02-19', '2018-03-30', '2018-05-28', '2018-07-04',
                                                             '2018-09-03', '2018-11-22', '2018-12-25', '2019-01-01',
                                                             '2019-01-21', '2019-02-18', '2019-04-19', '2019-05-27',
                                                             '2019-07-04', '2019-11-02', '2019-11-28', '2019-12-25',
                                                             '2020-01-01', '2020-01-20', '2020-02-17', '2020-04-10',
                                                             '2020-05-25', '2020-07-03', '2020-11-26', '2020-12-25',
                                                             '2021-01-01', '2021-01-18', '2021-02-15', '2021-04-02',
                                                             '2021-05-31', '2021-07-05', '2021-09-06', '2021-11-25',
                                                             '2021-12-24']))

    def __init__(self, begin_date, end_date, look_back, cash, tickers, trading_func, bar_distance='day', slippage=0.02):
        """
        Dates must be given in the ISO 8601 Format specification YYYY-MM-DD
        :param begin_date: Date upon which trading will initiate
        :param end_date: Date upon which trading will end
        :param look_back: Period in days which the system will have access to at any given time
        :param cash: Amount of liquid cash the account starts with
        :param tickers: list containing all stocks to be traded
        :param trading_func function that is called on each trading period
        :param bar_distance: minute, hour, day, week etc
        :param slippage: frictional trade coefficient meant to simulate slippage
        """
        self.api_key = os.environ['APCA_API_KEY_ID']
        self.begin_date = datetime.date.fromisoformat(begin_date)
        self.end_date = datetime.date.fromisoformat(end_date)
        self.look_back = datetime.timedelta(days=look_back)
        self.initial_cash = cash
        self.portfolio = portfolio(tickers, cash)
        self.trading_func = trading_func
        self.bar_distance = bar_distance
        self.slippage = slippage
        self.date_offset = 0
        self.asset = dict()

    #TODO Need to more thouroughly verify that this works
    def __correct_begin_date(self):
        """
        This function gives us the date we need to begin our data collection from by accounting for weekends and nyse
        holidays
        """
        temp_lookback = self.look_back.days #When Extending for other timeframes this function will likely require overhaul
        while temp_lookback > 0:
            if self.begin_date.isoweekday() == 7:
                self.begin_date -= datetime.timedelta(days=2)
            elif self.begin_date.isoweekday() == 6:
                self.begin_date -= datetime.timedelta(days=1)
            elif self.begin_date in self.__NYSE_HOLIDAYS:
                self.begin_date -= datetime.timedelta(days=1)
            else:
                self.begin_date -= datetime.timedelta(days=1)
                temp_lookback -= 1

    def __calc_pl(self):
        """
        Calculate and display the results of the trading
        """
        net_value = self.portfolio.cash
        for ticker in self.portfolio.tickers:
            data = self.asset[ticker][self.look_back.days + self.date_offset] #Subtract one because we incremented offset an extra time
            price = data['c']
            quantity = self.portfolio.holdings[ticker]
            net_value += price * quantity
        print("Portfolio Value {:.2f}".format(net_value))
        print("Initial Investment {:.2f}".format(self.initial_cash))
        print("Net Profit {:.2f}".format(net_value-self.initial_cash))
        print("Percent return {:.2f}%".format(100 * ((net_value/self.initial_cash) - 1)))

    def trade(self):
        """
        This function when called begins the cycle of trading. Note that the data the system has access
        to will be the beginDate - lookback, but the first trade will be initiated as if it was done during beginDate
        The Eventual goal for this will be to implement some controls over it in tkinter
        :return:
        """
        client = RESTClient(self.api_key)
        tickers = self.portfolio.tickers
        self.__correct_begin_date()
        for stock in tickers:
            response = client.stocks_equities_aggregates(stock, 1, self.bar_distance,
                                                         self.begin_date - datetime.timedelta(days=1),
                                                         self.end_date + datetime.timedelta(days=1))
            if response.results is None: #Make sure that data is actually gotten
                    raise Exception("Unable to retrieve market data")
            self.asset[stock] = response.results

        while self.date_offset + self.look_back.days < len(self.asset[tickers[0]]) - 1: #TODO Is every stock going to have the exact same amount of days?
            truncated_data = dict()
            for stock in tickers:
                truncated_data[stock] = self.asset[stock][self.date_offset:self.look_back.days + self.date_offset] #Creates the set of data that only includes the current lookback period
            self.trading_func(truncated_data)
            self.date_offset += 1
        self.__calc_pl()

    def sell(self, ticker, quantity):
        """
        Sells the asset at the open price of the next trading period
        :param ticker: Asset to be sold
        :param quantity: Quantity of asset to sell
        """
        data = self.asset[ticker][self.look_back.days + self.date_offset]
        price = data['o']
        date = datetime.datetime.utcfromtimestamp(data['t']/1000)
        self.portfolio.sell(ticker, price, date, quantity)

    def buy(self, ticker, quantity):
        """
        Buys the asset at the open price of the next trading period
        :param ticker: Asset to be purchased
        :param quantity: Quantity to purchase
        """
        data = self.asset[ticker][self.look_back.days + self.date_offset]
        price = data['o']
        date = datetime.datetime.utcfromtimestamp(data['t']/1000)
        self.portfolio.add(ticker, price, date, quantity)
