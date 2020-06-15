from abc import ABC, abstractmethod #module providing infrastructure for abstract base class




class DataHandler(ABC):
    """
    Abstract Base Class to provide a framework for all data collection across all platforms

    Output: Generates a container holding the specified number of bars for a ticker and time frame
    """
    @abstractmethod
    def get_latest_bars(self, ticker_symbol:str, lookback_length:str):
        """
        Abstract class method that will be defined as a method that returns the last N bars from the ticker symbol
        :param ticker_symbol: stock for which the bars are retrieved
        :param lookback_length: period over which to retrieve data
        """
        raise NotImplementedError("Error: Implementation for 'get_latest_bars' is required")

    """
    Retrieves the latest bar from specified database to add to bar container
    """
    @abstractmethod
    def update_bars(self, ticker_symbol:str):
        """
        When implemented this method should push the latest bar to the relevant ticker's data structure
        :param ticker_symbol: Stock for which new bars are added
        """
        raise NotImplementedError("Error: Implementation for 'update_bars' is required")

