import csv
from pandas import read_csv
import os
import pandas as pd

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
        clean_sheets = []
        for balance_sheet in dfs:
            balance_sheet = balance_sheet.rename(columns={balance_sheet.columns[0]:'Timestamp'})
            balance_sheet = balance_sheet.set_index('Timestamp').T
            balance_sheet.index = pd.to_datetime(balance_sheet.index, format='%Y-%m')
            clean_sheets.append(balance_sheet)
        return clean_sheets

    def load_cashflow(self):
        dfs = []
        for ticker in self.tickers:
            print(ticker)
            filename = os.path.join(self.dirname, 'data/{} {}.csv'.format(ticker, "Cash Flow"))
            print(filename)
            dfs.append(read_csv(filename, skiprows=1))
        clean_sheets = []
        for balance_sheet in dfs:
            balance_sheet = balance_sheet.rename(columns={balance_sheet.columns[0]:'Timestamp'})
            balance_sheet = balance_sheet.set_index('Timestamp').T
            balance_sheet.index = pd.to_datetime(balance_sheet.index, format='%Y-%m')
            clean_sheets.append(balance_sheet)
        return clean_sheets

    def load_income_statement(self):
        dfs = []
        for ticker in self.tickers:
            print(ticker)
            filename = os.path.join(self.dirname, 'data/{} {}.csv'.format(ticker, "Income Statement"))
            print(filename)
            dfs.append(read_csv(filename, skiprows=1))
        clean_sheets = []
        for balance_sheet in dfs:
            balance_sheet = balance_sheet.rename(columns={balance_sheet.columns[0]:'Timestamp'})
            balance_sheet = balance_sheet.set_index('Timestamp').T
            balance_sheet.index = pd.to_datetime(balance_sheet.index, format='%Y-%m')
            clean_sheets.append(balance_sheet)
        return clean_sheets
    
    def load_key_ratios(self):
        dfs = []
        for ticker in self.tickers:
            print(ticker)
            filename = os.path.join(self.dirname, 'data/{} {}.csv'.format(ticker, "Key Ratios"))
            print(filename)
            dfs.append(read_csv(filename, skiprows=1))
        clean_sheets = []
        for balance_sheet in dfs:
            balance_sheet = balance_sheet.rename(columns={balance_sheet.columns[0]:'Timestamp'})
            balance_sheet = balance_sheet.set_index('Timestamp').T
            balance_sheet.index = pd.to_datetime(balance_sheet.index, format='%Y-%m')
            clean_sheets.append(balance_sheet)
        return clean_sheets
