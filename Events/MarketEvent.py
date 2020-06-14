"""
Data is pulled from Polygon through the RESTful API and packaged into MarketEvents

MarketEvents represent data for a given bar period (e.g day, minute, hour, etc... ) and are 
partitioned by ticker names

A MarketEvent is just a dictionary with keys of the ticker symbols. Each symbol is mapped to a 
stock object that represents data for the specified bar period

The MarketEvents are packaged into a stack or queue (depending on how they are received) by the DataHandler
and then returned back to the Strategy for processing. 
 """

 class MarketEvent():

    def __init__(self, stock_dict):
        self.tickers = stock_dict
    

    def get(self, ticker: str):
        return self.tickers[ticker]

    