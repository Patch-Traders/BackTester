from abc import ABC, abstractmethod #module providing infrastructure for abstract base class


class dataHandler(ABC):
    """
    Abstract Base Class to provide a framework for all data collection across all platforms

    Output: Generates a container holding the specified number of bars for a ticker and time frame
    """
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

