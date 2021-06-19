from config import *
from discord_webhook import DiscordWebhook
from discord_webhook import DiscordEmbed
import json, numpy as np
import websocket
import talib
from threading import Thread
import time

url = 'https://discord.com/api/webhooks/853694685951295529/luTD_JlSV9uXpnyi-Ft5S877daATTXWzdnpmhJD86Zln-8XPxzRk427CfEbrkNbhOacI'

webhook4 = DiscordWebhook(url=url, rate_limit_retry=True,
                        content='Is Logged In')
webhook4.execute()

cc = 'btcusdt'
interval = '1m'

socket = f'wss://stream.binance.com:9443/ws/{cc}@kline_{interval}'

amount = 500000
trade_amount = 5000
stop_loss = 0

portfolio = 0
investment, real_time_portfolio_value, closes, highs, lows, opens = [], [], [], [], [], []
money_end = amount
prices = [amount]
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
    global stop_loss, timer, real_time_portfolio_value
    bitcoin_position = real_time_portfolio_value
    if bitcoin_position <= stop_loss and stop_loss != 0:
        sell(bitcoin_position, price)
        print('Selled all the bitcoins!')
        timer = True
    else:
        prices.append(bitcoin_position)
        prices.sort()
        print(prices)
        if prices[-1] == bitcoin_position:
            stop_loss = bitcoin_position*0.995
            print('stop-loss moved')
            print(f'Stop-Loss: {stop_loss}\n')

class Bot(Thread):
    def run(self):
        def on_message(ws, message):
            global portfolio, investment, closes, highs, lows, opens, money_end, real_time_portfolio_value, timer
            json_message = json.loads(message)
            cs = json_message['k']
            candle_closed, close, open1, low, high = cs['x'], cs['c'], cs['o'], cs['l'], cs['h']
            if candle_closed:
                closes.append(float(close))
                highs.append(float(high))
                lows.append(float(low))
                opens.append(float(open1))
                last_price = closes[-1]
                print(f'\nCLoses: {closes}')
                # if core_to_trade == True and counter == 0:
                #     buy(core_trade_amount, price = last_price)
                #     webhook = DiscordWebhook(url='https://discord.com/api/webhooks/853694685951295529/luTD_JlSV9uXpnyi-Ft5S877daATTXWzdnpmhJD86Zln-8XPxzRk427CfEbrkNbhOacI', rate_limit_retry=True)
                #     embed = DiscordEmbed(title='Bought DogeCoin', description=f'Bought $ price worth of DogeCoin', color=0xffb029)
                #     embed.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/en/d/d0/Dogecoin_Logo.png')
                #     embed.add_embed_field(name='Price:', value='$ price', inline=True)
                #     embed.add_embed_field(name='Quantity:', value='quantity', inline=True)
                #     embed.add_embed_field(name='DogeCoin Price:', value='$ price', inline=True)
                #     embed.set_footer(text='Bought DogeCoin at this time')
                #     webhook.add_embed(embed=embed)
                #     webhook.execute()
                #     print(f'Core Investment: We bought ${core_trade_amount} worth of bitcoin')
                #     core_quantity += core_trade_amount/last_price
                #     core_to_trade = False
                # elif core_trade_amount == True and counter != 0:
                #     second_amount = money_end * 0.8
                #     buy(second_amount, price = last_price)
                #     webhook1 = DiscordWebhook(url='https://discord.com/api/webhooks/853694685951295529/luTD_JlSV9uXpnyi-Ft5S877daATTXWzdnpmhJD86Zln-8XPxzRk427CfEbrkNbhOacI', rate_limit_retry=True)
                #     embed1 = DiscordEmbed(title='Bought DogeCoin', description='Bought $price worth of DogeCoin', color=0xffb029)
                #     embed1.set_thumbnail(url='https://upload.wikimedia.org/wikipedia/en/d/d0/Dogecoin_Logo.png')
                #     embed1.add_embed_field(name='Price:', value='$ price', inline=True)
                #     embed1.add_embed_field(name='Quantity:', value='quantity', inline=True)
                #     embed1.add_embed_field(name='DogeCoin Price:', value='$ price', inline=True)
                #     embed1.set_footer(text='Bought DogeCoin at this time')
                #     webhook1.add_embed(embed1)
                #     webhook1.execute()
                #     print(f'Core Investment: We bought ${second_amount} worth of bitcoin')
                #     core_quantity += core_trade_amount/last_price
                #     core_to_trade = False
                #Strategies
                engulfing = talib.CDLENGULFING(np.array(opens), np.array(highs), np.array(lows), np.array(closes))
                doji = talib.CDLDOJI(np.array(opens), np.array(highs), np.array(lows), np.array(closes))
                hammer = talib.CDLHAMMER(np.array(opens), np.array(highs), np.array(lows), np.array(closes))
                shooting_star = talib.CDLSHOOTINGSTAR(np.array(opens), np.array(highs), np.array(lows), np.array(closes))
                harami = talib.CDLHARAMI(np.array(opens), np.array(highs), np.array(lows), np.array(closes))
                kicking = talib.CDLKICKING(np.array(opens), np.array(highs), np.array(lows), np.array(closes))
                if engulfing[-1] != 0:
                    last_eng = engulfing[-1]
                    print(f'Engulfing: {last_eng}')
                elif doji[-1] != 0:
                    last_eng = doji[-1]
                    print(f'Doji: {last_eng}')
                elif hammer[-1] != 0:
                    last_eng = hammer[-1]
                    print(f'Hammer: {last_eng}')
                elif shooting_star[-1] != 0:
                    last_eng = shooting_star[-1]
                    print(f'Shooting-Star: {last_eng}')
                elif harami[-1] != 0:
                    last_eng = harami[-1]
                    print(f'Harami: {last_eng}')
                elif kicking[-1] != 0:
                    last_eng = kicking[-1]
                    print(f'Kicking: {last_eng}')
                else:
                    last_eng = 0
                    pass
                amt = last_eng*trade_amount/100
                port_value = portfolio*last_price
                trade_amt = amt - port_value
                if last_eng == 0:
                    trade_amt = 0
                real_time_portfolio_value = portfolio*last_price + money_end
                webhook5 = DiscordWebhook(url='https://discord.com/api/webhooks/855698858684579860/k8DjBmPGq7bgrfcQgb07vrGxQl6aaAMhOiWVokAXjTitYGWneNt371BvjmhnwQJ6J4TQ', rate_limit_retry=True, content = str(real_time_portfolio_value))
                webhook5.execute()
                if trade_amt > 0 and trade_amt < money_end:
                    buy(trade_amt, price=last_price)
                    webhook2 = DiscordWebhook(url=url, rate_limit_retry=True)
                    embed2 = DiscordEmbed(title='Bought BitCoin', description='Bought BitCoin this much', color=0xffb029)
                    embed2.set_thumbnail(url='https://images-na.ssl-images-amazon.com/images/I/51O6ByIc8OL._AC_SX466_.jpg')
                    embed2.add_embed_field(name='Price:', value='price', inline=True)
                    embed2.add_embed_field(name='Quantity:', value='price', inline=True)
                    embed2.add_embed_field(name='BitCoin Price:', value='price', inline=True)
                    embed2.set_footer(text='Bought Bitcoin at this time')
                    webhook2.add_embed(embed2)
                    webhook2.execute()
                    # print(f'We have bought ${trade_amt} worth of bitcoin')
                else:
                    if portfolio != 0 and trade_amt != 0:
                        sell(-trade_amt, price=last_price)
                        webhook3 = DiscordWebhook(url=url, rate_limit_retry=True, content = 'Hello')
                        embed3 = DiscordEmbed(title='Sell BitCoin', description='Sold BitCoin this much', color=0xffb029)
                        embed3.set_thumbnail(url='https://images-na.ssl-images-amazon.com/images/I/51O6ByIc8OL._AC_SX466_.jpg')
                        embed3.add_embed_field(name='Profit:', value='profit', inline=True)
                        embed3.add_embed_field(name='Quantity:', value='price', inline=True)
                        embed3.add_embed_field(name='BitCoin Price:', value='price', inline=True)
                        embed3.set_footer(text='Sold Bitcoin at this time')
                        webhook3.add_embed(embed3)
                        webhook3.execute()
                        # print(f'We sold ${-trade_amt} worth of bitcoin')
                    else:
                        print('No Trade!')
                trailingStop(last_price)
                if timer == True:
                    time.sleep(200)
                    timer = False
        ws = websocket.WebSocketApp(socket, on_message=on_message)
        ws.run_forever()
