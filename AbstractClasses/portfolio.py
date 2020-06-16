from abc import ABC, abstractmethod #module providing infrastructure for abstract base class
from Events.OrderEvent import OrderEvent


class portfolio:
    """
    Abstract Base Class for Porfolio objects

    Functionality:
    """
    @abstractmethod
    def buy(self, order_event: OrderEvent):
        """
        Executes a buy order and changes portfolio holdings.
        During live trading the data in the FillEvent will accurately represent 
        asset price at sell
        :param order_event: Event object that contains order information
        """
        raise NotImplementedError("Error: Implementation for 'buy' is required")


    @abstractmethod
    def sell(self, order_event: OrderEvent):
        """
        Executes a sell order and changes portfolio holdings
        During live trading the data in the FillEvent will accurately represent 
        asset price at sell
        :param order_event: Event object that contains order information
        """
        raise NotImplementedError("Error: Implementation for 'sell' is required")


    @abstractmethod
    def current_holdings(self):
        """
        Should return current holdings
        """
        raise NotImplementedError("Error: Implementation for 'sell' is required")


    @abstractmethod
    def market_value(self):
        """
        Should return marketValue
        """
        raise NotImplementedError("Error: Implementation for 'marketValue' is required")


    @abstractmethod
    def net_return(self):
        """
        Should calculate and return net Return
        """
        raise NotImplementedError("Error: Implementation for 'marketValue' is required")


    @abstractmethod
    def liquidity(self):
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



