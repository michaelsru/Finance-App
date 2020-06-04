import csv
from pandas import read_csv
import os

class FinancialsLoader:
    def __init__(self, ticker):
        self.ticker = ticker
        self.dirname = os.path.dirname(__file__)

    def load_balance_sheet(self):
        filename = os.path.join(self.dirname, 'data/{} {}.csv'.format(self.ticker, "Balance Sheet"))
        return read_csv(filename)


    def load_cashflow(self):
        filename = os.path.join(self.dirname, 'data/{} {}.csv'.format(self.ticker, "Cash Flow"))
        print(filename)
        return read_csv(filename)

    def load_income_statement(self):
        filename = os.path.join(self.dirname, 'data/{} {}.csv'.format(self.ticker, "Income Statement"))
        return read_csv(filename)

    def load_key_ratios(self):
        filename = os.path.join(self.dirname, 'data/{} {}.csv'.format(self.ticker, "Key Ratios"))
        return read_csv(filename)
