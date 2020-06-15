import datetime
import os
import queue
from Events.MarketEvent import MarketEvent
from Events.Stock import Stock
from polygon import RESTClient
from DataHandlerABC import DataHandler


class Alpaca(DataHandler):
    """
    Retrieves equities data from Alpaca with the help of Polygon API

    BarSize: 1 day
    """
    def __init__(self, tickers: list[str], begin_date: str, end_date: str, bar_size: int):
        """
        Dates must be given in the ISO 8601 Format specification YYYY-MM-DD
        :param tickers: list containing all stocks to be traded
        :param begin_date: Date upon which trading will initiate
        :param end_date: Date upon which trading will end
        :param bar_size: minute, hour, day, week etc...
        """
        #self.api_key = os.environ['APCA_API_KEY_ID'] # API key to access polygon data (set as environoment variable )
        self.tickers: list[str] = tickers
        self.ticker_data: dict = dict() # dictionary of ticker symbols with their corresponding data
        self.begin_date: str = begin_date
        self.end_date: str = end_date
        self.look_back: int = datetime.strptime(begin_date) - datetime.strptime(end_date)
        self.market_events = queue.Queue( maxsize = self.look_back )  # Queue of market_events to be processed by strategy
        self.bar_size = bar_size

    def build_ticker_queue(self):
        """
        Packages ticker data into MarketEvents put in a queue to then be processed by the strategy
        """
        
        # pulling data from Polygon API
        self.get_ticker_data(self.tickers, self.look_back)

        for i in range(look_back):
            
            # iterate through all bars for each ticker symbol and package them into MarketEvents
            bar_dict = dict()
            for bar in ticker_data.values:
                bar_dict[bar[i]["T"]] = Stock(bar[i])

            self.market_events.put( MarketEvent(bar_dict) )
        
        return self.market_events
   
    """
    TODO 
    Q: What exactly is stock multiplier? 
    Q: Can we manipulate the bar distance? 
    Q: Is the data on holidays and weekends just non-existent (i.e None)?
    Q: 
    """

    def get_ticker_data(self, tickers: List[str], lookback_length:str):
        """
        Utilizes 
        """

        # setting up client 
        client = RESTClient(self.api_key)
       
        # retrieves market data for each ticker in the specified time frame 
        for stock in self.tickers:
            response = client.stocks_equities_aggregates(
                stock, 1, self.bar_size, self.begin_date, self.end_date
            )

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