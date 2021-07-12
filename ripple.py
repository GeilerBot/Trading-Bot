from config import *
from discord_webhook import DiscordWebhook
from discord_webhook import DiscordEmbed
import json, numpy as np
import websocket
import talib
import strategy
from threading import Thread
import time

url = 'https://discord.com/api/webhooks/853608942809382913/3MLiF2Q3XoDxIigdAFpHdaackaB_8dumAENJTMY6tTbdPCPkKCL4q76JnPEvkZgO3AEO'

webhook4 = DiscordWebhook(url=url, rate_limit_retry=True,
                        content='Is Logged In')
webhook4.execute()

securitynumber = 0
crypto = 'XRP/USDT'
cc = 'xrpusdt'
interval = '1m'

date = time.ctime()

socket = f'wss://stream.binance.com:9443/ws/{cc}@kline_{interval}'

amount = 500000
trade_amount = 5000
stop_loss = 0
pattern = ''

portfolio = 0
investment, real_time_portfolio_value, closes, highs, lows, opens = [], [], [], [], [], []
money_end = amount
prices = []
timer = False


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

def trailingStop(price):
    global stop_loss, timer, portfolio, real_time_portfolio_value, amount
    bitcoin_position = real_time_portfolio_value
    if bitcoin_position <= stop_loss and stop_loss != 0:
        webhook1 = DiscordWebhook(url=url, rate_limit_retry=True)
        embed1 = DiscordEmbed(title='Sell Ripple', description=f'Sold Ripple on trailing-stop', color=0xffb029)
        embed1.set_thumbnail(url='https://media.discordapp.net/attachments/792024444742533121/856214443884937266/ripple.png')
        embed1.add_embed_field(name='Amount:', value=f'${str(bitcoin_position)}', inline=True)
        embed1.add_embed_field(name='Quantity:', value=f'{str(round(portfolio, 2))}', inline=True)
        embed1.add_embed_field(name='Ripple Price:', value=f'${str(round(price))}', inline=True)
        embed1.add_embed_field(name='Portfolio:', value=f'{str(round(real_time_portfolio_value))}/{str(amount)}', inline=True)
        embed1.set_footer(text=f'Sold Ripple at {date}')
        webhook1.add_embed(embed1)
        webhook1.execute()
        sell(bitcoin_position, price)
        print('Selled all the bitcoins!')
        timer = True
        del prices[:]
        prices.append(0)
        real_time_portfolio_value = stop_loss
    else:
        prices.append(bitcoin_position)
        prices.sort()
        print(prices)
        if prices[-1] == bitcoin_position:
            stop_loss = bitcoin_position-5
            print('stop-loss moved')
            print(f'Stop-Loss: {stop_loss}\n')
class Bot(Thread):
    def run(self):
        def on_message(ws, message):
            global portfolio, investment, closes, highs, lows, opens, money_end, real_time_portfolio_value, timer, stop_loss, pattern, securitynumber, crypto, pattern
            json_message = json.loads(message)
            cs = json_message['k']
            candle_closed, close, open1, low, high = cs['x'], cs['c'], cs['o'], cs['l'], cs['h']
            if candle_closed:
                closes.append(float(close))
                highs.append(float(high))
                lows.append(float(low))
                opens.append(float(open1))
                last_price = closes[-1]
                #Strategies
                securitynumber = strategy.strategy(crypto=crypto, security=securitynumber, type=pattern)
                # print(securitynumber)
                # engulfing = talib.CDLENGULFING(np.array(opens), np.array(highs), np.array(lows), np.array(closes))
                # doji = talib.CDLDOJI(np.array(opens), np.array(highs), np.array(lows), np.array(closes))
                # hammer = talib.CDLHAMMER(np.array(opens), np.array(highs), np.array(lows), np.array(closes))
                # if engulfing[-1] >= 0:
                #     securitynumber += 1
                #     pattern = 'Engulfing'
                # elif doji[-1] >= 0:
                #     securitynumber += 1
                #     pattern = 'Doji'
                # elif hammer[-1] >= 0:
                #     securitynumber += 1
                #     pattern = 'Hammer'
                # else:
                #     pass
                if securitynumber == 0:
                    pass
                elif securitynumber > 0 and securitynumber < 3:
                    amt = trade_amount - 2000
                elif securitynumber > 0 and securitynumber < 5:
                    amt = trade_amount -1000
                elif securitynumber > 0:
                    amt = trade_amount
                else:
                    amt = 0
                real_time_portfolio_value = portfolio*last_price + money_end
                webhook5 = DiscordWebhook(url='https://discord.com/api/webhooks/855698858684579860/k8DjBmPGq7bgrfcQgb07vrGxQl6aaAMhOiWVokAXjTitYGWneNt371BvjmhnwQJ6J4TQ', rate_limit_retry=True, content = str(real_time_portfolio_value))
                webhook5.execute()
                date = time.ctime()
                if amt > 0 and amt < money_end:
                    buy(amt, price=last_price)
                    webhook2 = DiscordWebhook(url=url, rate_limit_retry=True)
                    embed2 = DiscordEmbed(title='Bought Ripple', description=f'Bought Ripple on "{pattern}" strategy', color=0xffb029)
                    embed2.set_thumbnail(url='https://media.discordapp.net/attachments/792024444742533121/856214443884937266/ripple.png')
                    embed2.add_embed_field(name='Amount:', value=f'${str(amt)}', inline=True)
                    embed2.add_embed_field(name='Quantity:', value=f'{str(round(amt/last_price, 2))}', inline=True)
                    embed2.add_embed_field(name='Ripple Price:', value=f'${str(round(last_price))}', inline=True)
                    embed2.add_embed_field(name='Portfolio:', value=f'{str(round(real_time_portfolio_value))}/{str(amount)}', inline=True)
                    embed2.set_footer(text=f'Bought Ripple at {date}')
                    webhook2.add_embed(embed2)
                    webhook2.execute()
                    print(f'We have bought ${amt} worth of bitcoin')
                else:
                    print('No Trade!')
                trailingStop(last_price)
                if timer == True:
                    time.sleep(200)
                    timer = False
                    stop_loss = 0
        ws = websocket.WebSocketApp(socket, on_message=on_message)
        ws.run_forever()
