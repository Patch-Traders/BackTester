import datetime
import os
from data-handler import DataHandler
from nyse-holidays import _NYSE_HOLIDAYS 

"""
Retrieves equities data from Alpaca with the help of Polygon API

BarSize: 1 day
"""
class Alpaca(DataHandler):

    def __init__(self, tickers: List[str], lookback_length: int):
        self.holidays = _NYSE_HOLIDAYS
        #self.api_key = os.environ['APCA_API_KEY_ID'] # API key set as environment variable
        self.begin_date = self.calculate_begin_date(
            datetime.timedelta(days = lookback_length).days
        )
        self.tickers = tickers # array of tickers
        self.ticker_data = dict() # { key:ticker_name : value:pricing_data }

     """
    Retrieves lastest bar data from specified time period
    """
    def get_ticker_data(self, tickers: List[str], lookback_length:str):

        # setting up client 
        client = RESTClient(self.api_key)
       
        # retrieves market data for each ticker in the specified time frame 
        for stock in self.tickers:
            response = client.stocks_equities_aggregates(stock, 1, self.bar_distance,
                                                         self.begin_date - datetime.timedelta(days=1),
                                                         self.end_date + datetime.timedelta(days=1))
            # ensures data is retrieved
            if response.results is None:
                    raise Exception("Unable to retrieve market data")

            # puts ticker with corresponding pricing over specified period 
            self.ticker_data[stock] = response.results

    """
    Retrieves the latest bar from specified database to add to bar container
    """
    def update_ticker_data(self, ticker_symbol:str):

        # is this possible with REST API or do we need to use WebSockets for constant connection? 
        pass


    """
    Calculates the appropriate start date accounting for weekends and holidays
    """
    def calculate_begin_date(num_days:int):

        # considers weekends and holidays to look back appropriate number of days 
        begin_date = None  
        while num_days > 0:
            if begin_date.isoweekday() == 7:
                begin_date -= datetime.timedelta(days=2)
            elif begin_date.isoweekday() == 6:
                begin_date -= datetime.timedelta(days=1)
            elif begin_date in self.__NYSE_HOLIDAYS:
                begin_date -= datetime.timedelta(days=1)
            else:
                begin_date -= datetime.timedelta(days=1)
                num_days -= 1
        
        return begin_date



if __name__ == "__main__":

    print("Hello World")