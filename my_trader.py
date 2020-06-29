from patch_quant.patch_quant import pq
# TODO figure out how to properly organize a package
# The way it is right now feels hacky


class myTrader():
    def trade(self, lookback_data: dict, day_data:dict):
        """
        Test trading function
        :param data_set: Data set for each stock
        :return:
        """
        # basic trading strategy for testing
        print(lookback_data)

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
        settings['Slippage'] = 0.2

        return settings



if __name__ == '__main__':
    pq.begin(myTrader)
