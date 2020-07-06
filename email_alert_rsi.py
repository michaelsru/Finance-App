# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.5.0
#   kernelspec:
#     display_name: finance-app
#     language: python
#     name: finance-app
# ---

# %%
import yfinance as yf
from pandas import DataFrame as df
from pandas_datareader import data as pdr
import pandas as pd
import datetime
from datetime import timedelta
from stockstats import StockDataFrame as sdf
import matplotlib.pyplot as plt

import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

def generate_rsi_plot(ticker):
    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('Date')
    ax1.set_ylabel('rsi_14 ($)', color=color)
    ax1.plot(stock.index, stock['rsi_14'], color=color)
    ax1.tick_params(axis='y', labelcolor=color)
    plt.ylim(0,100)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('High', color=color)  # we already handled the x-label with ax1
    ax2.plot(stock.index, stock['high'], color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.title('RSI vs HIGH for {}'.format(ticker))
    # plt.show()
    filename = 'graphs/{}_rsi.png'.format(ticker)
    plt.savefig(filename)
    return filename



# %%
timeframe = 6
# tickers = ['DFN.TO', 'V']
tickers = ['DFN.TO', 'V', 'MA', 'FOOD.TO', 'AMD', 'ALK', 'AC', 'OAS', 'PD', 'PLUG', 'XBC.V']
today = datetime.datetime.now().date()

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "financeapp1234@gmail.com"  # Enter your address
receiver_email = "s.michaelru@gmail.com"  # Enter receiver address
# password = input("Type your password and press enter: ")
password = 'admin1234ABC'
# email_msg = ''

message = MIMEMultipart("alternative")
message["Subject"] = "multipart test"
message["From"] = sender_email
message["To"] = receiver_email

text = 'Ticker(s):  '
plots = []
html = ''

for ticker in tickers:
    company = yf.Ticker(ticker)

    # msft_ohlc_df = msft.history(period="max", interval='1d', start='2019-10-02', end='2020-01-01')
    ohlc_df = company.history(period="max", interval='60m', start=(today - timedelta(days=timeframe)))
    ohlc_df.index = pd.to_datetime(ohlc_df.index, format='%Y-%M-%d')
    
    stock = sdf.retype(ohlc_df)
    cur_rsi = stock['rsi_14'].iloc[-1]
#     cur_rsi=80
    
    if cur_rsi > 70 or cur_rsi < 30:
        
        rsi_plot = generate_rsi_plot(ticker)
        
        html += """\
Ticker:{}</br>
Current RSI = {:.2f}</br>
<img src="cid:{}"><br>
""".format(ticker, cur_rsi, rsi_plot)
        
        fp = open('{}'.format(rsi_plot), 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID', '<{}>'.format(rsi_plot))
        message.attach(msgImage)

        # Define the image's ID as referenced above
#         msgImage.add_header('Content-ID', '<image1>')

# html += '</body></html>'
msgText = MIMEText(html, 'html')  
print(msgText)
message.attach(msgText)   # Added, and edited the previous line
# print(message)
with smtplib.SMTP_SSL(smtp_server, port) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())

# %%
