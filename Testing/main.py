from EventLoops.backtesting_loop import backTesting


def trade(data_set, global_vars):
    """
    Test trading function
    :param data_set: Data set for each stock
    :param global_vars: dictionary that allows for passing of variables between function calls
    :return:
    """
    print(data_set['AAPL']['open'])
    return global_vars


def define_settings(settings):
    """
    Test function that is given to event loop to define settings
    """
    settings['LookBack'] = 50
    settings['BeginDate'] = "2018-01-01"
    settings['EndDate'] = "2019-01-30"
    settings['Cash'] = 10000
    settings['BarSize'] = 'day'
    settings['Tickers'] = ['AAPL', 'MSFT']
    return settings


backTesting(trade, define_settings)


'''
from DataHandlers.alpaca import Alpaca

test = Alpaca(['AAPL'], '2019-01-01', '2019-05-01', 'day', 10)
a = test.get_initial_barset()
print("ehllo")

print(a['AAPL']['open'])
'''
