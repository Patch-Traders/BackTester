from abc import ABC, abstractmethod #module providing infrastructure for abstract base class


"""
Abstract Base Class to provide a framework for all data collection across all platforms

Output: Generates a container holding the specified number of bars for a ticker and time frame
"""
class DataHandler(ABC):

    """
    Retrieves lastest bar data from specified time period
    """
    @abstractmethod
    def get_latest_bars(self, ticker_symbol:str, lookback_length:str):
        pass

    """
    Retrieves the latest bar from specified database to add to bar container
    """
    @abstractmethod
    def update_bars(self, ticker_symbol:str):
        pass

    