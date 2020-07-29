from patch_quant.patch_quant import patchQuant as pq
# TODO figure out how to properly organize a package


class myTrader():

    def trade(self, lookback_data: dict, bar_data:dict):
        """
        Trading function
        :param lookback_data: Data set for each ticker over the lookback period
        :param bar_data: Data from most recent bar period
        :return:
        """

        if pq.cash > 99000:
            pq.open_short('AAPL', 10)
        else:
            pq.close_short('AAPL', 1)

        print(pq.cash)

    def define_settings(self, settings):
        """
        Settings function
        :param settings: Dictionary that defines the backtestings settings
        """
        settings['LookBack'] = 5
        settings['BeginDate'] = '2019-01-01'
        settings['EndDate'] = '2019-03-30'
        settings['Cash'] = 100000
        settings['BarSize'] = 'day'
        settings['Tickers'] = ['AAPL']
        settings['Slippage'] = 0.02

        return settings

if __name__ == '__main__':

    pq.initialize(myTrader)
    pq.begin()
    print(pq.order_log)
    pq.candlestick('2019-01-01', '2019-03-30', 'AAPL')
    # pq.portfolio_performance('2019-01-01', '2019-03-30')




