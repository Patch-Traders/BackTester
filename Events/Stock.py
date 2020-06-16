

class Stock:
    """
    Makes accessing stock data within a given MarketEvent to be more intuitive and accessible
    """

    def __init__(self, stock_data : dict):

        self.name = stock_data["T"]
        self.volume = stock_data["v"]
        self.open = stock_data["o"]
        self.close = stock_data["c"]
        self.high = stock_data["h"]
        self.low = stock_data["l"]
        self.start = stock_data["t"]
        self.bars_passed = stock_data["n"]
    
    @property
    def name():
        return self.name
    
    @property
    def volume():
        return self.volume

    @property
    def open(): 
        return self.open

    @property
    def close(): 
        return self.close
    
    @property
    def high():
        return self.high

    @property
    def low(): 
        return self.low

    @property
    def start():
        return self.start

    @property 
    def bars_passed():
        return self.bars_passed

