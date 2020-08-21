import datetime
import alpaca_trade_api as tradeapi
from patch_quant.AbstractClasses.data_handler import dataHandler
from patch_quant.Resources.nyse_holidays import NYSE_HOLIDAYS


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
        #TODO Add in catches for dates outside of proper range
        """
        self.__api = tradeapi.REST()
        self.__tickers = tickers
        self.__begin_date = datetime.date.fromisoformat(begin_date)
        self.__end_date = datetime.date.fromisoformat(end_date)
        self.__bar_size = bar_size
        self.__look_back = look_back
        self.__barset_offset = 0  # Tracks the amount of times update date is being called
        self.__full_barset = self.__get_full_barset()

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

    def __create_truncated_dict(self, offset: int):
        """
        Truncates the full dataset
        :return truncated_data: Dataset that is truncated over the proper time period
        """
        lookback_data = dict()
        days_data = dict()
        for ticker in self.__full_barset:
            lookback_data[ticker] = self.__full_barset[ticker][offset:self.__look_back + offset]
            days_data[ticker] = self.__full_barset[ticker].iloc[self.__look_back + offset - 1]
        return [lookback_data, days_data]

    def __get_full_barset(self):
        """
        Grabs the full dataset from the alpaca web api
        # TODO Need to deal with the data size limit imposed by api.polygon.historic_agg_v2
        # TODO investigate the exclusive nature of the alpaaca API end date
        currently only 3000 data points can be retrieved
        """
        full_bar_set = dict()
        for ticker in self.__tickers:
            full_bar_set[ticker] = self.__api.polygon.historic_agg_v2(ticker, 1, self.__bar_size,
                                                                            _from=self.__begin_date.isoformat(),
                                                                            to=self.__end_date.isoformat()).df

        return full_bar_set

    def get_initial_barset(self):
        """
        Retrieves the initial barset for ticker_symbol from alpaca
        :param ticker_symbol: symbol from which data is retrieved
        :param look_back_length: the size of the dataset and the period of time it spans
        :return The initial dateset that goes up to the day before begin_date
        """
        self.__correct_begin_date()
        return self.__create_truncated_dict(0)

    def update_barset(self):
        """
        Creates a new barset to simulate the acquistion of data from a real exchange
        :return: A pandas Dataframe that contains the data for the proper timeframe
        """
        # TODO Make this work for time periods that arent a day
        # Either scale lookback if the user will always provide lookback in terms of days
        # Or make lookback be in the unit of barsize which would require no change
        # TODO Does a distinction need to be made when a new day appears for barsizes < day
        # Only continue dripfeeding data if there is data to feed
        if self.__barset_offset + self.__look_back < len(self.__full_barset[self.__tickers[0]]):
            self.__barset_offset += 1
            return self.__create_truncated_dict(self.__barset_offset)
        else:
            # This is the signal for the event loop to know that the trading period has ended
            return 0

    @property
    def get_full_barset(self):
        return self.__full_barset

