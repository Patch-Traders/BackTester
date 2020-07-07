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
        self.__execution_day = 0
        self.__portfolio = None
        self.__alpaca = None
        self.__settings = dict()

    def __default_settings(self):
        """
        This method initializes the settings dictionary to default values
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
            self.__portfolio.update_market_value(data_array[1], 'close')

            # trades with look back and daily data
            self.__trade(data_array[0], data_array[1])

            # updates look back and daily data for next iteration
            data_array = self.__alpaca.update_barset()

    def set_portfolio(self, portfolio):
        self.__portfolio = portfolio

    @property
    def settings(self):
        return self.__settings

    @property
    def execution_day(self):
        return self.__execution_day


