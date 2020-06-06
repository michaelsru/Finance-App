import yfinance as yf
from pandas import DataFrame as df

from pandas_datareader import data as pdr

msft = yf.Ticker("MSFT")

print(msft.balance_sheet)

df_cashflow = df(msft.cashflow)
