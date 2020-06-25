from abc import ABC, abstractmethod #module providing infrastructure for abstract base class


class portfolio(ABC):
    """
    Abstract Base Class for Portfolio objects
    """

    @abstractmethod
    def __init__(self, tickers:list, cash: int):
        """
        :param cash: initial amount of tradeable cash
        """
        raise NotImplementedError("Error: Implementation of the constructor is required")

    @abstractmethod
    def buy(self, date:str, ticker: str, quantity: int, price:int) -> None:
        """
        Executes a buy order and changes portfolio holdings.
        :param ticker: ticker symbol
        :param quantity: quantity to be traded
        """
        raise NotImplementedError("Error: Implementation for 'buy' is required")


    @abstractmethod
    def sell(self, date:str, ticker: str, quantity: int, price:int) -> None:
        """
        Executes a sell order and changes portfolio holdings
        :param ticker: ticker symbol
        :param quantity: quantity to be traded
        """
        raise NotImplementedError("Error: Implementation for 'sell' is required")


    @abstractmethod
    def current_holdings(self) -> dict:
        """
        Should return current holdings
        """
        raise NotImplementedError("Error: Implementation for 'sell' is required")


    @abstractmethod
    def market_value(self) -> int:
        """
        Should return marketValue
        """
        raise NotImplementedError("Error: Implementation for 'marketValue' is required")

    @abstractmethod
    def update_market_value(self, daily_data:dict) -> None:
        """
        Updates the market value of the portfolio
        """
        pass

    @abstractmethod
    def net_return(self) -> int:
        """
        Should calculate and return net Return
        """
        raise NotImplementedError("Error: Implementation for 'marketValue' is required")


    @abstractmethod
    def cash(self) -> int:
        """
        Should return liquidity
        """
        raise NotImplementedError("Error: Implementation for 'liquidity' is required")


    @abstractmethod
    def leverage(self):
        """
        Should return leverage
        """
        raise NotImplementedError("Error: Implementation for 'leverage' is required")
