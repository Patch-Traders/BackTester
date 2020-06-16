from AbstractClasses.event_loop import eventLoop
from DataHandlers.alpaca import Alpaca

class backTesting(eventLoop):
    """
    This class implements the event loop abstract class for backtesting
    """

    def __init__(self, loop_func, settings_func):
        """
        #TODO how do you type hint functions?
        Initializes the object with the two functions that will be called within the event loop
        :param loop_func: Function to be called on every loop
        :param settings_func: Function that is called once for the user to create settings.
        """
        self.__loop_func = loop_func
        self.__settings_func = settings_func
        self.__global_vars = dict() # This will be passed so that the user can keep values between loop calls
        self.__default_settings()
        self.manage_settings()
        self.alpaca = Alpaca(self.__settings['Tickers'], self.__settings['BeginDate'], self.__settings['EndDate'],
                             self.__settings['BarSize'], self.__settings['LookBack'])
        self.loop()

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
        self.__settings = settings

    def manage_settings(self):
        """
        Calls the settings function passing to it the settings dictionary where the user can set the settings
        """
        self.__settings = self.__settings_func(self.__settings)
        if self.__settings["LookBack"] <= 0:
            raise ValueError("LookBack can not be less than 1")
        if self.__settings['Cash'] <= 0:
            raise ValueError("Minimum Cash is 1")
        if self.__settings['BarSize'] not in ['minute', '1Min', '5Min', '15Min', 'day', '1D']:
            raise ValueError("BarSize is not a valid value")
        if not self.__settings['Tickers']:
            raise ValueError("No Stock tickers provided")

    def loop(self):
        """
        This function should begin and then manage the event loop
        """
        data_set = self.alpaca.get_initial_barset()
        while data_set != 0:
            self.__global_vars = self.__loop_func(data_set, self.__global_vars) #TODO Is there a better way to get update __global_vars?
            if type(self.__global_vars) != dict:
                raise TypeError("The dictionary for global variables is not a dictionary")
            data_set = self.alpaca.update_barset()



