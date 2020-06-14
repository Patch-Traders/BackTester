from abc import ABC, abstractmethod #module providing infrastructure for abstract base class


"""
Abstract Base Class to provide a framework for all data collection across all platforms

Output: Generates a container holding the specified number of bars for a ticker and time frame
"""
class DataHandler(ABC):


    @abstractmethod
    def build_ticker_queue(): 
        """
        Creates a Queue of MarketEvents to be processed by the Strategy
        """        
        pass
   
    @abstractmethod
    def get_ticker_data(self, ticker_symbol:str, lookback_length:str):
         """
        Retrieves lastest bar data from specified time period
        """
        pass

    @abstractmethod
    def update_ticker_data(self, ticker_symbol:str):
        """
        Retrieves the latest bar from specified database to add to bar container
        """
        pass

    