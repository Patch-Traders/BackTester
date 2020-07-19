from patch_quant.patch_quant import patchQuant as pq
# TODO figure out how to properly organize a package
# The way it is right now feels hacky


class myTrader():

    global GLOBAL_VAR

    def trade(self, lookback_data: dict, day_data:dict):
        """
        Test trading function
        :param data_set: Data set for each stock
        :return:
        """
        if pq.portfolio_cash == 100000:
            pq.open_short('AAPL', 58)
            pq.open_long('AAPL', 58)

    def define_settings(self, settings):
        """
        Test function that is given to event loop to define settings
        """
        settings['LookBack'] = 5
        settings['BeginDate'] = '2019-01-01'
        settings['EndDate'] = '2019-03-30'
        settings['Cash'] = 100000
        settings['BarSize'] = 'day'
        settings['Tickers'] = ['AAPL']
        settings['Slippage'] = 0.2

        return settings

if __name__ == '__main__':
    pq.initialize(myTrader)
    pq.begin()
    pq.portfolio_performance('2019-01-01', '2019-03-30')
    print(pq.portfolio_cash)



