import datetime
import os
import queue
from polygon import RESTClient
from data-handler import DataHandler

class Alpaca(DataHandler):
    """
    Retrieves equities data from Alpaca with the help of Polygon API

    BarSize: 1 day
    """

    def __init__(self, tickers: List[str], begin_date: str, end_date: str, bar_length: int):
         """
        Dates must be given in the ISO 8601 Format specification YYYY-MM-DD
        :param: API key to access data from polygon (need to set as an environoment variable)
        :param begin_date: Date upon which trading will initiate
        :param end_date: Date upon which trading will end
        :param tickers: list containing all stocks to be traded
        :param bar_length: minute, hour, day, week etc
        """
        #self.api_key = os.environ['APCA_API_KEY_ID'] 
        self.tickers = tickers 
        self.begin_date = begin_date
        self.end_date = end_date
        self.ticker_data = queue.Queue( maxsize = 
            datetime.strptime(begin_date) - datetime.strptime(end_date) 
            ) # maxSize is the time delta between dates (includes weekends/holidays)
        self.bar_length = bar_length

   
    #TODO ******** --> need to rework logic here again *********

    def get_ticker_data(self, tickers: List[str], lookback_length:str):
        """
        Retrieves lastest bar data from specified time period
        """

        # setting up client 
        client = RESTClient(self.api_key)
       
        # retrieves market data for each ticker in the specified time frame 
        for stock in self.tickers:
            response = client.stocks_equities_aggregates(stock, 1, self.bar_distance,
                                                         self.begin_date - datetime.timedelta(days=1),
                                                         self.end_date + datetime.timedelta(days=1))

            print(response)
            # ensures data is retrieved
            if response.results is None:
                    raise Exception("Unable to retrieve market data")

            # puts ticker with corresponding pricing over specified period 
            self.ticker_data[stock] = response.results

    def update_ticker_data(self, ticker_symbol:str):

        """
        Retrieves the latest bar from specified database to add to bar container.
        Only necesssary when live trading. 
        """
        return -1:
        # is this possible with REST API or do we need to use WebSockets for constant connection? 
        # also need to use asynchonous techniques to pull data while managing


if __name__ == "__main__":

    print("Hello World")
    alpaca = Alpaca()