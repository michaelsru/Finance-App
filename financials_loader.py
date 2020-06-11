import csv
from pandas import read_csv
import os

class FinancialsLoader:
    def __init__(self, tickers):
        self.tickers = tickers
        self.dirname = os.path.dirname(__file__)

    def load_balance_sheet(self):
        dfs = []
        for ticker in self.tickers:
            print(ticker)
            filename = os.path.join(self.dirname, 'data/{} {}.csv'.format(ticker, "Balance Sheet"))
            print(filename)
            dfs.append(read_csv(filename, skiprows=1))
        return dfs

    def load_cashflow(self):
        dfs = []
        for ticker in self.tickers:
            print(ticker)
            filename = os.path.join(self.dirname, 'data/{} {}.csv'.format(ticker, "Cash Flow"))
            print(filename)
            dfs.append(read_csv(filename, skiprows=1))
        return dfs

    def load_income_statement(self):
        dfs = []
        for ticker in self.tickers:
            print(ticker)
            filename = os.path.join(self.dirname, 'data/{} {}.csv'.format(ticker, "Income Statement"))
            print(filename)
            dfs.append(read_csv(filename, skiprows=1))
        return dfs
    
    def load_key_ratios(self):
        dfs = []
        for ticker in self.tickers:
            print(ticker)
            filename = os.path.join(self.dirname, 'data/{} {}.csv'.format(ticker, "Key Ratios"))
            print(filename)
            dfs.append(read_csv(filename, skiprows=1))
        return dfs
