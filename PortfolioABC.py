
from abc import ABC, abstractmethod #module providing infrastructure for abstract base class
from Events.OrderEvent import OrderEvent

"""
Abstract Base Class for Porfolio objects

Functionality: 
"""
class Portfolio: 

    @abstractmethod
    def buy( order_event: OrderEvent ):
        """
        Executes a buy order and changes portfolio holdings.
        During live trading the data in the FillEvent will accurately represent 
        asset price at sell
        """
        raise NotImplementedError("Error: Implementation for 'buy' is required")


    @abstractmethod
    def sell( order_event: OrderEvent ):
        """
        Executes a buy order and changes portfolio holdings
        During live trading the data in the FillEvent will accurately represent 
        asset price at sell
        """
        raise NotImplementedError("Error: Implementation for 'sell' is required")


    @abstractmethod
    def currentHoldings():
        raise NotImplementedError("Error: Implementation for 'sell' is required")


    @abstractmethod
    def marketValue(): 
        raise NotImplementedError("Error: Implementation for 'marketValue' is required")


    @abstractmethod
    def netReturn(): 
        raise NotImplementedError("Error: Implementation for 'marketValue' is required")


    @abstractmethod
    def liquidity(): 
        raise NotImplementedError("Error: Implementation for 'liquidity' is required")

    
    @abstractmethod
    def leverage(): 
        raise NotImplementedError("Error: Implementation for 'leverage' is required")



