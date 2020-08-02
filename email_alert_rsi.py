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
import os

def generate_rsi_plot(ticker, stock):
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
    filename = '{}_rsi.png'.format(ticker)
    filename = os.path.abspath(filename)
    print(filename)
    plt.savefig(filename)
    return filename

def send_alert_based_on_rsi(cur_rsi, prev_rsi) -> bool:
    if abs(cur_rsi - prev_rsi) < 10:
        return False
    if cur_rsi > 70:
        return True
    if cur_rsi < 30:
        return True
    if abs(cur_rsi-prev_rsi) > 10:
        return True



# %%
import numpy as np

timeframe = 7
tickers = ['DFN.TO', 'V', 'MA', 'FOOD.TO', 'AMD', 'ALK', 'TSLA', 'OAS', 'PLUG', 'XBC.V']
today = datetime.datetime.now().date()

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "financeapp1234@gmail.com"  # Enter your address
receiver_email = ['s.michaelru@gmail.com', 'jamesyellowlee61@gmail.com', 'julialee1164@gmail.com']  # Enter receiver address
# password = input("Type your password and press enter: ")
password = 'admin1234ABC'

prev_rsi_array = np.zeros((len(tickers),), dtype=int)

def email_for_tickers():
    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email

    text = 'Ticker(s):  '
    plots = []
    html = ''

    for i, ticker in enumerate(tickers):
        company = yf.Ticker(ticker)
        ohlc_df = company.history(period="max", interval='5m', start=(today - timedelta(days=timeframe)))
        ohlc_df.index = pd.to_datetime(ohlc_df.index, format='%Y-%M-%d')

        stock = sdf.retype(ohlc_df)
        cur_rsi = stock['rsi_14'].iloc[-1]
        cur_high = stock['high'].iloc[-1]

        if send_alert_based_on_rsi(cur_rsi, prev_rsi_array[i]):
            prev_rsi_array[i] = cur_rsi
            rsi_plot = generate_rsi_plot(ticker, stock)

            html += 'Ticker:{}\nCurrent RSI:{:.2f}</br>High:{}</br><img src="cid:{}">\n'''.format(ticker, cur_rsi, cur_high, rsi_plot)

            fp = open('{}'.format(rsi_plot), 'rb')
            msgImage = MIMEImage(fp.read())
            fp.close()
            msgImage.add_header('Content-ID', '<{}>'.format(rsi_plot))
            message.attach(msgImage)

    if html == '':
        return

    msgText = MIMEText(html, 'html')
    print(msgText)
    message.attach(msgText)

    with smtplib.SMTP_SSL(smtp_server, port) as server:
        server.login(sender_email, password)
        for rec in receiver_email:
            message["To"] = rec
            print(rec)
            server.sendmail(sender_email, rec, message.as_string())


# %%
import time

while True:
    localtime = time.localtime()
    result = time.strftime("%H:%M:%S %p", localtime)
    email_for_tickers()
    time.sleep(300)
