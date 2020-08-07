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
import math
import numpy as np

def generate_rsi_plot(ticker, stock, interval):
    xtick_freq = math.floor(len(stock)/5)
    positions = stock.index[::xtick_freq]

    fig, axes = plt.subplots(nrows=2, sharex=True)
    axes[0].plot(stock.index, stock['high'], color='red')
    axes[0].set_ylabel('high ($)')
    axes[1].plot(stock.index, stock['rsi_14'], color='blue')
    axes[1].set_ylabel('rsi_14')
    axes[1].set_ylim(0,100)
    plt.xticks(rotation=20)
    axes[1].set_xticks(positions)

    fig.suptitle('RSI vs HIGH for {}, {} interval'.format(ticker, interval))
    filename = '{}_rsi.png'.format(ticker)
    filename = os.path.abspath(filename)
    print(filename)
    plt.savefig(filename, bbox_inches = 'tight')
    return filename

def send_alert_based_on_rsi(cur_rsi, prev_rsi, cached_rsi) -> bool:
    if cur_rsi >= 70:
        if prev_rsi < 70 or abs(cur_rsi - cached_rsi) >= 5:
            return True
    if cur_rsi <= 30:
        if prev_rsi > 30 or abs(cur_rsi - cached_rsi) >= 5:
            return True
    return False


# %%
timeframe = 5
tickers = ['DFN.TO', 'V', 'MA', 'FOOD.TO', 'AMD', 'ALK', 'TSLA', 'OAS', 'PLUG', 'XBC.V', 'QCOM']

port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "financeapp1234@gmail.com"  # Enter your address
receiver_email = ['s.michaelru@gmail.com', 'jamesyellowlee61@gmail.com', 'julialee1164@gmail.com']  # Enter receiver address
password = 'admin1234ABC'

cached_rsi = np.full((len(tickers),), 50)
prev_rsi = np.full((len(tickers),), 50)

def email_for_tickers(date):
    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email

    text = 'Ticker(s):  '
    plots = []
    html = ''
    interval = '30m'

    for i, ticker in enumerate(tickers):
        company = yf.Ticker(ticker)
        try:
            ohlc_df = company.history(period="max", interval=interval, start=(date - timedelta(days=timeframe)))
        except:
            print('Error getting company history: date = {}'.format(date))
            return
        stock = sdf.retype(ohlc_df)
        stock.index = stock.index.strftime('%Y-%m-%d %H:%M:%S')

        cur_rsi = stock['rsi_14'].copy().iloc[-1]
        cur_high = stock['high'].copy().iloc[-1]
        print("{}: current rsi:{:.2f}, previous rsi:{:.2f}, cached rsi:{}".format(ticker, cur_rsi, prev_rsi[i], cached_rsi[i]))
        if send_alert_based_on_rsi(cur_rsi, prev_rsi[i], cached_rsi[i]):
            cached_rsi[i] = cur_rsi
            rsi_plot = generate_rsi_plot(ticker, stock, interval)

            html += 'Ticker:{}\nCurrent RSI:{:.2f}</br>High:{}</br><img src="cid:{}">\n'''.format(ticker, cur_rsi, cur_high, rsi_plot)
            fp = open('{}'.format(rsi_plot), 'rb')
            msgImage = MIMEImage(fp.read())
            fp.close()
            msgImage.add_header('Content-ID', '<{}>'.format(rsi_plot))
            message.attach(msgImage)

        prev_rsi[i] = cur_rsi

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
    date = datetime.datetime.now().date()
    localtime = time.localtime()
    result = time.strftime("%H:%M:%S %p", localtime)
    print(result)
    email_for_tickers(date)
    time.sleep(300)
