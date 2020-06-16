from abc import ABC, abstractmethod #module providing infrastructure for abstract base class


class dataHandler(ABC):
    """
    Abstract Base Class to provide a framework for all data collection across all platforms

    Output: Generates a container holding the specified number of bars for a ticker and time frame
    """
    @abstractmethod
    def __init__(self, tickers: list, begin_date: str, end_date: str, bar_size: str, look_back: int):
        """
        Dates must be given in the ISO 8601 Format specification YYYY-MM-DD
        :param tickers: list containing all stocks to be traded
        :param begin_date: Date upon which trading will initiate
        :param end_date: Date upon which trading will end
        :param bar_size: minute, hour, day, week etc...
        :param look_back: lookback period in days
        """
        raise NotImplementedError("Error: Implementation of the constructor is required")

    @abstractmethod
    def get_initial_barset(self):
        """
        When implemented this method should retrieve a dataset of size lookback_length
        with the data ending at the beginDate of that stock
        """
        raise NotImplementedError("Error: Implementation for 'get_latest_bars' is required")

    """
    Retrieves the latest bar from specified database to add to bar container
    """
    @abstractmethod
    def update_barset(self):
        """
        When implemented this method should push the latest bar to the relevant ticker's data structure
        """
        raise NotImplementedError("Error: Implementation for 'update_bars' is required")

