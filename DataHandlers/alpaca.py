import datetime
import os
import alpaca_trade_api as tradeapi
from data_handler import dataHandler
import numpy as np
from nyse_holidays import NYSE_HOLIDAYS


class Alpaca(dataHandler):
    """"
    Retrieves equities data from Alpaca with the help of Polygon API

    BarSize: 1 day
    """
    def __init__(self, tickers: list, begin_date: str, end_date: str, bar_size: str, look_back: int):
        """
        Dates must be given in the ISO 8601 Format specification YYYY-MM-DD
        :param tickers: list containing all stocks to be traded
        :param begin_date: Date upon which trading will initiate
        :param end_date: Date upon which trading will end
        :param bar_size: minute, hour, day, week etc...
        :param look_back: lookback period in days
        """
        self.__api = tradeapi.REST(key_id=os.environ['APCA_API_KEY_ID'], secret_key=os.environ['APCA_API_SECRET_KEY'],
                                   api_version='v2')
        self.__tickers = tickers
        self.__begin_date = datetime.date.fromisoformat(begin_date)
        self.__end_date = datetime.date.fromisoformat(end_date)
        self.__bar_size = bar_size
        self.__look_back = look_back
        self.__barset_offset = 0  #Tracks the amount of times update date is being called
        self.__full_barset = dict()

    def __correct_begin_date(self):
        """
        Because we want to be able to have a static lookback period we are uncertain of the actual first date we need
        to request data for as there are holidays and weekends in unpredictable quantities that create breaks in the
        dataset if not accounted for we would not be able to gurantee that a lookback period sized dataset is created
        """
        temp_look_back = self.__look_back
        while temp_look_back > 0:
            if self.__begin_date.isoweekday() == 7:
                self.__begin_date -= datetime.timedelta(days=2)
            elif self.__begin_date.isoweekday() == 6:
                self.__begin_date -= datetime.timedelta(days=1)
            elif self.__begin_date in NYSE_HOLIDAYS:
                self.__begin_date -= datetime.timedelta(days=1)
            else:
                self.__begin_date -= datetime.timedelta(days=1)
                temp_look_back -= 1

    def __create_truncated_dict(self, offset):
        """
        Truncates the full dataset
        :return truncated_data: Dataset that is truncated over the proper time period
        """
        truncated_data = dict()
        for ticker in self.__full_barset:
            truncated_data[ticker] = self.__full_barset[ticker][offset:self.__look_back + offset]
        return truncated_data

    def __get_full_barset(self):
        """
        Grabs the full dataset from the alpaca web api
        #TODO Need to deal with the data size limit imposed by api.polygon.historic_agg_v2
        currently only 3000 data points can be retrieved
        """
        for ticker in self.__tickers:
            self.__full_barset[ticker] = self.__api.polygon.historic_agg_v2(ticker, 1, self.__bar_size, _from=self.__begin_date.isoformat(), to=self.__end_date.isoformat()).df

    def get_initial_barset(self):
        """
        Retrieves the initial barset for ticker_symbol from alpaca
        :param ticker_symbol: symbol from which data is retrieved
        :param look_back_length: the size of the dataset and the period of time it spans
        :return The initial dateset that goes up to the day before begin_date
        """
        self.__correct_begin_date()
        self.__get_full_barset()
        return self.__create_truncated_dict(0)

    def update_barset(self):
        """
        Creates a new barset to simulate the acquistion of data from a real exchange
        :return: An np frame dataset that contains the data for the proper timeframe
        #TODO make sure that we do not step outside of the datset
        """
        self.barset_offset += 1
        return self.__create_truncated_dict(self.__barset_offset)
