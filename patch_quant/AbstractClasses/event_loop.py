from abc import ABC, abstractmethod  # module providing infrastructure for abstract base class


class eventLoop(ABC):
    """
    Abstract base class that provides an interface for initiating the event loop
    """

    @abstractmethod
    def __init__(self, loop_func, settings_func):
        """
        This init should implement the storing of the two functions that are the traders portion of the event loop
        :param loop_func: Function to be called on every loop
        :param settings_func: Function that is called once for the user to create settings.
        """
        raise NotImplementedError("Error: Implementation of the constructor is required")

    @abstractmethod
    def manage_settings(self):
        """
        This function will implement the calling of the settings function, and the handling of those settings afterwards
        """
        raise NotImplementedError("Error: You must implement the __settings function")

    @abstractmethod
    def loop(self):
        """
        This function should begin and then manage the event loop
        """
        raise NotImplementedError("Error: You must implement the __loop function ")
