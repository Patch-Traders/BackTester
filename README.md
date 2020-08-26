# PatchQuant
PatchQuant is a python backtesting library that allows the user to simulate trading 
strategies on all stocks listed on the exchange [Alpaca](https://alpaca.markets/).  

- [Installation](#installation)
- [How to Use](#how-to-use)
- [Team](#team)
- [License](#license)

### Installation
You can install PatchQuant from [PyPi](https://pypi.org):
    
    pip install PatchQuant

### Prerequisites
This package requires the installation of two python packages to enable its functionality: alpaca_trade_api, and plotly. 

Both can be installed with the following commands

    pip install plotly
    pip install alpaca_trade_api
    
### How to Use
Once the package is installed using PatchQuant is quite simple. To import simply use
    
    from PatchQuant.patch_quant import patchQuant as pq

Before writing any code it is critical that the user defines two environment variables:
    
    APCA_API_KEY_ID
    APCA_API_SECRET_KEY
    
These environment variables should be defined as your own Alpaca API keys.

PatchQuant expects the user to implement a class that contains two distinct functions: trade() and define_settings().
The specific requirements of their implementation is detailed below. 

Once backtesting is begun PatchQuant will initially
make a single call to the settings() function. In here the user has the opportunity to 
configure the details of the backtesting.
After that each trading period the trade() 
function will be called and the user will be given the opportunity to execute trades
in that period.

An example class that the user may implement:

    class myTrader():

        def trade(self, lookback_data: dict, day_data:dict):
            """
            Trading function
            :param lookback_data: Data set for each ticker over the lookback period
            :param day_data: Data set for each ticker on the day of trading
            """

        def define_settings(self, settings):
            """
            Settings function
            :param settings: Dictionary that defines the backtestings settings
            :return: The settings dictionary
            """
 
            return settings
            
            
##### define_settings(self, settings):
This function is where all of the backtester settings are defined, each setting is a member of a dictionary that is
passed to the define_settings function. It is imperative that this dictionary is returned by the function for the 
changes to take affect.

Settings can be defined like so:

        settings['LookBack'] = 5
        settings['BeginDate'] = '2019-01-01'
        settings['EndDate'] = '2019-03-30'
        settings['Cash'] = 100000
        settings['BarSize'] = 'day'
        settings['Tickers'] = ['AAPL']
        settings['Slippage'] = 0.02
        
| Setting  | Definition |
|----------| -----------------------------------------------------------------------------|
| LookBack | The time period in days for which the strategy has access to historical data | 
| BeginDate| The first day that trading will be simulated on |
| EnDate | The last day that trading will be simulated on |
| Cash | Cash available to purchase with at the beggining of trading |
| BarSize | Size of the trading period, options are: 'minute', 'hour', or 'day' |
| Tickers | A list containing the stock tickers to be traded |
| Slippage| A number used in slippage calculations |
##### trade(self, lookback_data, day_data):
The trade function is called at the beggining of each trading period and it is where the user has 
the opportunity to execute trades. 

lookback_data is a pandas dataframe containg all of the pricing data for each ticker over the lookback period.
day_data is the data for the current trading period.

The four most important functions to use are:
    
    pq.open_long(ticker, quantity)
    pq.close_long(ticker, quantity)
    pq.open_short(ticker, quantity)
    pq.close_short(ticker, quantity)

These functions allow you to open and close long and short positions on specific symbols.

At anytime the properties cash, order_log, and market_value are available as members of the PathQuant object.

After this class is implemented you can use these functions calls to begin the backtesting

    pq.initialize(myTrader)
    pq.begin()

After the final trading day there are a number of functions available to the user to allow them to visualize the performance of there strategy.

##### pq.candlestick(start_date, end_date, \*tickers):
This function creates a candelstick plot for the specified tickers

##### pq.timeseries(start_date, end_date, \*tickers): 
This function creates a timeseries plot for the specified tickers

##### pq.portfolio_performance(start_date, end_date):
This function creates a plot of the value of the portfolio over the time period

An Example of pq.candlestick():

![alt text](https://imgur.com/BEKlRgh.png)

### Team
This project is being developed and maintained by Hal Owens and Carson Kurtz, two college students with interests 
in technology, finance and statistics

Hal Owens - Purdue University - owens155@purdue.edu 

Carson Kurtz - Williams College - kurtzcarson@gmail.com


### License
Copyright 2020 Patch Traders

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.