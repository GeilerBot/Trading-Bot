from config import *
from discord_webhook import DiscordWebhook
import json, numpy as np
import websocket
from binance.client import Client
import requests
import talib

url = 'https://discord.com/api/webhooks/853323785838395392/nuAmX--T2jC42B9k3caiQTToRssB0J4mne5deBsyjCF6RrHJqJZH_LIZ1Im70ieBqA_B'

client = Client(key,secret)
webhook4 = DiscordWebhook(url=url, rate_limit_retry=True,
                         content='Is Logged In')
webhook4.execute()
print('logged in')

cc = 'btcusdt'
interval = '1m'

socket = f'wss://stream.binance.com:9443/ws/{cc}@kline_{interval}'

amount = 1000
core_trade_amount = 0.8*amount
trade_amount = 0.2*amount
core_to_trade = True

portfolio = 0
investment, real_time_portfolio_value, closes, highs, lows, opens = [], [], [], [], [], []
money_end = amount

def buy(allocated_money, price):
    global portfolio, money_end
    quantity = allocated_money/price
    money_end -= quantity*price
    portfolio += quantity
    if investment == []:
        investment.append(allocated_money)
    else:
        investment.append(allocated_money)
        investment[-1] += investment[-2]

def sell(allocated_money, price):
    global portfolio, money_end
    quantity = allocated_money/price
    money_end += quantity*price
    portfolio -= quantity
    investment.append(-allocated_money)
    investment[-1] += investment[-2]

def on_message(ws, message):
    global portfolio, investment, closes, highs, lows, opens, money_end, core_to_trade, core_quantity, real_time_portfolio_value
    json_message = json.loads(message)
    cs = json_message['k']
    candle_closed, close, open1, low, high = cs['x'], cs['c'], cs['o'], cs['l'], cs['h']

    if candle_closed:
        closes.append(float(close))
        highs.append(float(high))
        lows.append(float(low))
        opens.append(float(open1))
        last_price = closes[-1]
        print(f'CLoses: {closes}')
        if core_to_trade:
            buy(core_trade_amount, price = last_price)
            webhook = DiscordWebhook(url=url, rate_limit_retry=True,
                         content=f'Core Investment: We bought ${core_trade_amount} worth of bitcoin')
            webhook.execute()
            print(f'Core Investment: We bought ${core_trade_amount} worth of bitcoin')
            core_quantity = 0
            core_quantity += core_trade_amount/last_price
            core_to_trade = False
        
        engulfing = talib.CDLENGULFING(np.array(opens), np.array(highs), np.array(lows), np.array(closes))
        last_eng = engulfing[-1]
        amt = last_eng*trade_amount/100
        port_value = (portfolio - core_quantity)*last_price
        trade_amt = amt - port_value
        if last_eng == 0:
            trade_amt = 0
        else:
            trade_amt = trade_amt
        
        RT_portfolio_value = money_end + portfolio*last_price
        print(f'The Last Engulfing value is "{last_eng}" and recommended exposure is "${trade_amt}"')
        if RT_portfolio_value > 1000:    
            webhook7 = DiscordWebhook(url=url, rate_limit_retry=True,
                            content=f'Realt-Time Portfolio Value: ${RT_portfolio_value}')
            webhook7.execute()
        else:
            pass
        print(f'Realt-Time Portfolio Value: ${RT_portfolio_value}')
        if trade_amt >= 0:
            buy(trade_amt, price=last_price)
            if trade_amt == 0:
                pass
            else:
                webhook1 = DiscordWebhook(url=url, rate_limit_retry=True,
                            content=f'We have bought ${trade_amt} worth of bitcoin')
                webhook1.execute()
            print(f'We have bought ${trade_amt} worth of bitcoin')

        else:
            sell(-trade_amt, price=last_price)
            webhook2 = DiscordWebhook(url=url, rate_limit_retry=True,
                         content=f'We have sold ${-trade_amt} worth of bitcoin')
            webhook2.execute()
            print(f'We sold ${-trade_amt} worth of bitcoin')

ws = websocket.WebSocketApp(socket, on_message=on_message)
ws.run_forever()

