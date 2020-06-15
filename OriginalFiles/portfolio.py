class portfolio:
    """
    This class will track and contain the holdings of the account
    """
    def __init__(self, tickers, cash):
        """
        Initialization
        :param tickers: The list of the stocks that have the *potential* to be purchased aka the ones being tracked
        :param cash: The available purchasing power at the beginning
        """
        self.tickers = tickers
        self.cash = cash
        self.holdings = dict()
        self.transactions = dict()

    def add(self, ticker, price, date, quantity):
        """
        Add the stock to the portfolio
        :param ticker: Stock to add
        :param price: Price of stock
        :param date: Date of transaction
        :param quantity: Quantity of shares to exchange
        """
        if type(quantity) != int:
            raise Exception("Quantity of shares to purchase is not an integer!")
        if self.cash >= (quantity * price):
            self.cash -= (quantity * price)
        else:
            raise Exception("Not enough cash (${:.2f}) to purchase {} shares of {} at {}".format(self.cash, quantity,
                                                                                                ticker, price))
        if ticker not in self.holdings:
            self.holdings[ticker] = 0
        if ticker not in self.transactions:
            self.transactions[ticker] = list()

        self.holdings[ticker] += quantity
        self.transactions[ticker].append((quantity, price, date))

    def sell(self, ticker, price, date, quantity):
        """
        Sells the stock removing the shares from holdings
        :param ticker: Stock to be removed
        :param price: price of sale
        :param date: date of sale
        :param quantity: quantity to sell
        """
        #Raise exceptions if you can not sell that many shares
        if ticker not in self.holdings:
            raise Exception("Not enough shares of {}".format(ticker))
        if self.holdings[ticker] < quantity:
            raise Exception("Not enough shares of {}".format(ticker))

        self.cash += price
        self.holdings[ticker] -= quantity
        self.transactions[ticker].append((quantity, price, date))

