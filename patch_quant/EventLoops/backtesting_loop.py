from patch_quant.AbstractClasses.event_loop import eventLoop
from patch_quant.DataHandlers.alpaca import Alpaca


class backTesting(eventLoop):
    """
    Wrapped in the PatchQuant wrapper class to loop through the specified trading strategy intialized in the
    Trader class
    """

    def __init__(self, trader):
        """
        Initializes the backtester with the two functions that will be called within the event loop
        :param trader: Trader object created by the user with a unique trading function and settings
        """

        self.__trade = trader.trade
        self.__define_settings = trader.define_settings
        self.__execution_day = None
        self.__portfolio = None
        self.__alpaca = None
        self.__settings = dict()

    def __default_settings(self):
        """
        Initializes the settings dictionary to default values
        """
        self.__settings['LookBack'] = 25
        self.__settings['BeginDate'] = "2019-01-01"
        self.__settings['EndDate'] = "2019-01-30"
        self.__settings['Cash'] = 1000
        self.__settings['BarSize'] = 'day'
        self.__settings['Tickers'] = ['AAPL', 'MSFT']
        self.__settings['Slippage'] = 0.2

    def manage_settings(self):
        """
        Calls the settings function passing to it the settings dictionary where the user can set the settings
        """
        self.__default_settings()
        self.__settings = self.__define_settings(self.__settings)
        if self.__settings["LookBack"] < 1:
            raise ValueError("LookBack can not be less than 1")
        if self.__settings['Cash'] <= 0:
            raise ValueError("Minimum Cash is 1")
        if self.__settings['BarSize'] not in ['minute', '1Min', '5Min', '15Min', 'day', '1D']:
            raise ValueError("BarSize is not a valid value")
        if not self.__settings['Tickers']:
            raise ValueError("No Stock tickers provided")
        self.__alpaca = Alpaca(self.__settings['Tickers'], self.__settings['BeginDate'], self.__settings['EndDate'],
                               self.__settings['BarSize'], self.__settings['LookBack'])

    def loop(self):
        """
        Manages the trading execution loop
        """

        data_array = self.__alpaca.get_initial_barset()
        while data_array != 0:

            # Get execution price pre slippage
            self.__execution_day = data_array[1]

            # updates market value for risk management
            self.__portfolio.update_market_value(data_array[1], 'open')

            # trades with look back and daily data
            self.__trade(data_array[0], data_array[1])

            # updates look back and daily data for next iteration
            data_array = self.__alpaca.update_barset()


    def set_portfolio(self, portfolio):
        """
        Sets a given portfolio for the back testing system
        """
        self.__portfolio = portfolio

    @property
    def full_data_set(self):
        return self.__alpaca.get_full_barset

    @property
    def settings(self):
        return self.__settings

    @property
    def execution_day(self):
        return self.__execution_day


