from AbstractClasses.trader import trader
from Portfolios.my_portfolio import myPortfolio
from EventLoops.backtesting_loop import backTesting

class myTrader(trader):
    def __init__(self, portfolio: myPortfolio):
        self.__global_vars = dict()
        self.__portfolio = portfolio
        self.__counter = 1

    def trade(self, data_set: dict):
        """
        Test trading function
        :param data_set: Data set for each stock
        :param global_vars: dictionary that allows for passing of variables between function calls
        :return:
        """
        price = data_set["AAPL"].iloc[-1]['open']
        if self.__counter == 1:
            self.__portfolio.buy("fake_date", "AAPL", 1, price)
            self.__counter += 1
        # print("Daily Data :", data_set["AAPL"].iloc[-1])
        print(price)
        print(self.__portfolio.current_holdings)
        print("Market Value: ", self.__portfolio.market_value)
        print("Net Return: ", self.__portfolio.net_return())

    def define_settings(self, settings):
        """
        Test function that is given to event loop to define settings
        """
        settings['LookBack'] = 10
        settings['BeginDate'] = '2019-01-01'
        settings['EndDate'] = '2019-01-30'
        settings['Cash'] = 1000
        settings['BarSize'] = 'day'
        settings['Tickers'] = ['AAPL', 'MSFT']

        return settings

    def portfolio(self):
        return self.__portfolio


if __name__ == '__main__':
    portfolio = myPortfolio(['AAPL', 'MSFT'], 1000)
    trader = myTrader(portfolio)
    backTesting(trader)