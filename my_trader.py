import patch_quant


class myTrader(trader):
    def __init__(self, portfolio: myPortfolio):
        self.__global_vars = dict()
        self.__portfolio = portfolio
        self.__counter = 1

    def trade(self, lookback_data: dict, day_data:dict):
        """
        Test trading function
        :param data_set: Data set for each stock
        :return:
        """

        # basic trading strategy for testing
        if (self.__portfolio.cash >=  day_data['AAPL']['close']):
            self.__portfolio.buy(day_data['AAPL'].name, 'AAPL', 1, day_data['AAPL']['close'])

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

    # initialization for running the trader
    portfolio = myPortfolio(['AAPL'], 1000)
    trader = myTrader(portfolio)
    backTesting(trader)

    print('Order Log: \n', portfolio.order_log)