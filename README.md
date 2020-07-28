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


### How to Use
Once the package is installed using PatchQuant is quite simple. To import simply add 
    
    import PatchQuant as pq
to your file

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

lookback_data is a pandas dataframe containg all of the pricing data for each ticker over the lookback period
day_data is the data for the current trading period

The four most important functions to use are:
    
    pq.open_long(ticker, quantity)
    pq.close_long(ticker, quantity)
    pq.open_short(ticker, quantity)
    pq.close_short(ticker, quantity)


After this class is implemented you can use these functions calls to begin the backtesting

    pq.initialize(myTrader)
    pq.begin()


### Team
This project is being developed and maintained by Hal Owens and Carson Kurtz, two college students with interests 
in technology, finance and statistics

Hal Owens - Purdue University - owens155@purdue.edu 

Carson Kurtz - Williams College - kurtzcarson@gmail.com


### License
