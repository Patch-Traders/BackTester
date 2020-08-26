from abc import ABC, abstractmethod  # module providing infrastructure for abstract base class


class trader(ABC):
    """
    Abstract base class that provides an interface for trading strategies
    The user is free to define global variables that may assist them with their trading strategy. In addition,
    the user is free to design helper methods that can be utilized within the trade function.
    """

    @abstractmethod
    def trade(self, data_set: dict):
        """
        Implements the calling of the settings function, and the handling of those settings afterwards
        """
        raise NotImplementedError("Error: You must implement the trade function")

    @abstractmethod
    def define_settings(self, settings: dict):
        """
        Defines the settings for the trading system
        User must define the lookback period, begin date, end date, cash, bar sieze and tickers within the settings dictionary
        Example:
        settings['BeginDate'] = "2018-01-01"
        settings['EndDate'] = "2019-01-30"
        settings['Cash'] = 10000
        settings['BarSize'] = 'day'
        settings['Tickers'] = ['AAPL', 'MSFT']
        """
        raise NotImplementedError("Error: You must implement the define_settings function")