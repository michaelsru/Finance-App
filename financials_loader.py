import csv
import pandas as pd
import os

class FinancialsLoader:
    def __init__(self, ticker):
        self.ticker = ticker
        self.balance_sheet = None
        self.cashflow = None
        self.income_statement = None
        self.key_ratios = None
        self.dirname = os.path.dirname(__file__)

    def load_balance_sheet(self):
        filename = os.path.join(self.dirname, 'data/{} {}.csv'.format(self.ticker, "Balance Sheet"))
        self.balance_sheet = pd.read_csv(filename)

    def load_cashflow(self):
        filename = os.path.join(self.dirname, 'data/{} {}.csv'.format(self.ticker, "Cash Flow"))
        print(filename)
        self.cashflow = pd.read_csv(filename)

    def load_income_statement(self):
        filename = os.path.join(self.dirname, 'data/{} {}.csv'.format(self.ticker, "Income Statement"))
        self.income_statement = pd.read_csv(filename)

    def load_key_ratios(self):
        filename = os.path.join(self.dirname, 'data/{} {}.csv'.format(self.ticker, "Key Ratios"))
        self.key_ratios = pd.read_csv(filename)
