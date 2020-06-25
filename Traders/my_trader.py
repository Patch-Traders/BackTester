from AbstractClasses.trader import trader
from Portfolios.my_portfolio import myPortfolio
from EventLoops.backtesting_loop import backTesting

class myTrader(trader):
    def __init__(self, portfolio: myPortfolio):
        self.__global_vars = dict()
        self.__portfolio = portfolio
        self.__counter = 1

    def trade(self, lookback_data: dict, day_data:dict):
        """
        Test trading function
        :param data_set: Data set for each stock
        :param global_vars: dictionary that allows for passing of variables between function calls
        :return:
        """

        if (self.__portfolio.cash >=  day_data['AAPL']['close']):
            self.__portfolio.buy(day_data['AAPL'].name, 'AAPL', 1, day_data['AAPL']['close'])

        # print("Lookback Data: ", lookback_data)
        # print("\nDay_Data: ", day_data)

    def define_settings(self, settings):
        """
        Test function that is given to event loop to define settings
        """
        settings['LookBack'] = 5
        settings['BeginDate'] = '2019-01-01'
        settings['EndDate'] = '2019-01-30'
        settings['Cash'] = 1000
        settings['BarSize'] = 'day'
        settings['Tickers'] = ['AAPL']

        return settings

    def portfolio(self):
        return self.__portfolio


if __name__ == '__main__':
    portfolio = myPortfolio(['AAPL', 'MSFT'], 1000)
    trader = myTrader(portfolio)
    backTesting(trader)
    print(portfolio.order_log)