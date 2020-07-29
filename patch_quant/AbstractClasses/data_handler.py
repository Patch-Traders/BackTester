from abc import ABC, abstractmethod  # module providing infrastructure for abstract base class

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
    def __correct_begin_date(self):
        """
        Retrieves the correct begin date for the specified lookback period
        """
        raise NotImplementedError("Error: Implementation of '__correct_begin_date' is required")

    @abstractmethod
    def __create_truncated_dict(self, offest: int):
        """
        Truncates the full dataset
        :return truncated_data: Dataset that is truncated over the proper time period
        """
        raise NotImplementedError("Error: Implementation of '__create_truncated_dict' is required")

    @abstractmethod
    def __get_full_barset(self):
        """
        Retrieves the full dataset from the Alpaca web api
        """
        raise NotImplementedError("Error: Implementation of '__get_full_barset' is required")

    @abstractmethod
    def get_initial_barset(self):
        """
        Retrieves a dataset of size lookback_length with the data ending at the begin date of the specified period
        """
        raise NotImplementedError("Error: Implementation for 'get_latest_bars' is required")

    @abstractmethod
    def update_barset(self):
        """
        Pushes the latest bar data for each ticker in the given trading period
        """
        raise NotImplementedError("Error: Implementation for 'update_bars' is required")
