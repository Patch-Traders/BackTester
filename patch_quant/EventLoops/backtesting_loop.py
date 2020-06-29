from patch_quant.AbstractClasses.event_loop import eventLoop
from patch_quant.DataHandlers.alpaca import Alpaca


class backTesting(eventLoop):
    """
    This class implements the event loop abstract class for backtesting
    """

    def __init__(self, trader):
        """
        Initializes the object with the two functions that will be called within the event loop
        :param loop_func: Function to be called on every loop
        :param settings_func: Function that is called once for the user to create settings.
        """

        self.__trade = trader.trade
        self.__define_settings = trader.define_settings
        self.__default_settings()
        self.alpaca = Alpaca(self.__settings['Tickers'], self.__settings['BeginDate'], self.__settings['EndDate'],
                             self.__settings['BarSize'], self.__settings['LookBack'])
        self.__settings = dict()

    def __default_settings(self):
        """
        This method initializes the settings dictionary to default values
        """
        settings = dict()
        settings['LookBack'] = 25
        settings['BeginDate'] = "2019-01-01"
        settings['EndDate'] = "2019-01-30"
        settings['Cash'] = 1000
        settings['BarSize'] = 'day'
        settings['Tickers'] = ['AAPL', 'MSFT']
        settings['Slippage'] = 0.2
        self.__settings = settings

    def manage_settings(self):
        """
        Calls the settings function passing to it the settings dictionary where the user can set the settings
        """
        self.__settings = self.__define_settings(self.__settings)
        if self.__settings["LookBack"] < 1:
            raise ValueError("LookBack can not be less than 1")
        if self.__settings['Cash'] <= 0:
            raise ValueError("Minimum Cash is 1")
        if self.__settings['BarSize'] not in ['minute', '1Min', '5Min', '15Min', 'day', '1D']:
            raise ValueError("BarSize is not a valid value")
        if not self.__settings['Tickers']:
            raise ValueError("No Stock tickers provided")

    def loop(self):
        """
        Manages the trading execution loop
        """

        data_array = self.alpaca.get_initial_barset()
        while data_array != 0:

            # updates market value for risk management
            self.__portfolio.update_market_value(data_array[1], 'close')

            # trades with look back and daily data
            self.__trade(data_array[0], data_array[1])

            # updates look back and daily data for next iteration
            data_array = self.alpaca.update_barset()
