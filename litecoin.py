from config import *
from discord_webhook import DiscordWebhook
from discord_webhook import DiscordEmbed
import json, numpy as np
import websocket
from binance.client import Client
import talib
from threading import Thread
import time

url = 'https://discord.com/api/webhooks/853323785838395392/nuAmX--T2jC42B9k3caiQTToRssB0J4mne5deBsyjCF6RrHJqJZH_LIZ1Im70ieBqA_B'

client = Client(key,secret)
webhook4 = DiscordWebhook(url=url, rate_limit_retry=True,
                        content='Is Logged In')
webhook4.execute()
print('logged in')

cc = 'ltcusdt'
interval = '1m'

socket = f'wss://stream.binance.com:9443/ws/{cc}@kline_{interval}'

amount = 500000
core_trade_amount = 0.8*amount
trade_amount = 0.2*amount
stop_loss = core_trade_amount*0.99
core_to_trade = True
counter = 0

portfolio = 0
investment, real_time_portfolio_value, closes, highs, lows, opens = [], [], [], [], [], []
money_end = amount
prices = [core_trade_amount]


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
    global portfolio, core_trade_amount, stop_loss, core_to_trade, prices, counter
    bitcoin_position = portfolio*price
    if bitcoin_position <= stop_loss:
        sell(bitcoin_position, price)
        print('Selled all the litecoins!')
        core_to_trade = True
        counter += 1
    else:
        prices.append(bitcoin_position)
        prices.sort()
        print(prices)
        if prices[-1] == bitcoin_position:
            stop_loss = bitcoin_position*0.99
            print('stop-loss moved')
            print(stop_loss)


class Bot(Thread):
    def run(self):
        def on_message(ws, message):
            global portfolio, investment, closes, highs, lows, opens, money_end, core_to_trade, real_time_portfolio_value
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
                if core_to_trade == True and counter == 0:
                    buy(core_trade_amount, price = last_price)
                    webhook = DiscordWebhook(url='https://discord.com/api/webhooks/853694685951295529/luTD_JlSV9uXpnyi-Ft5S877daATTXWzdnpmhJD86Zln-8XPxzRk427CfEbrkNbhOacI', rate_limit_retry=True, content = 'Hello')
                    embed = DiscordEmbed(title='Bought LiteCoin', description='Bought LiteCoin this much', color=0xffb029)
                    embed.set_thumbnail(url='https://banner2.cleanpng.com/20180525/wal/kisspng-litecoin-cryptocurrency-bitcoin-logo-cryptocurrency-5b081f1979b524.5871818715272589054985.jpg')
                    embed.add_embed_field(name='Price:', value='price', inline=True)
                    embed.add_embed_field(name='Quantity:', value='price', inline=True)
                    embed.add_embed_field(name='LiteCoin Price:', value='price', inline=True)
                    embed.set_footer(text='Bought LiteCoin at this time')
                    webhook.add_embed(embed)
                    webhook.execute()
                    print(f'Core Investment: We bought ${core_trade_amount} worth of litecoin')
                    core_quantity = 0
                    core_quantity += core_trade_amount/last_price
                    core_to_trade = False
                elif core_trade_amount == True and counter != 0:
                    second_amount = money_end * 0.8
                    buy(second_amount, price = last_price)
                    webhook1 = DiscordWebhook(url='https://discord.com/api/webhooks/853694685951295529/luTD_JlSV9uXpnyi-Ft5S877daATTXWzdnpmhJD86Zln-8XPxzRk427CfEbrkNbhOacI', rate_limit_retry=True, content = 'Hello')
                    embed1 = DiscordEmbed(title='Bought LiteCoin', description='Bought LiteCoin this much', color=0xffb029)
                    embed1.set_thumbnail(url='https://banner2.cleanpng.com/20180525/wal/kisspng-litecoin-cryptocurrency-bitcoin-logo-cryptocurrency-5b081f1979b524.5871818715272589054985.jpg')
                    embed1.add_embed_field(name='Price:', value='price', inline=True)
                    embed1.add_embed_field(name='Quantity:', value='price', inline=True)
                    embed1.add_embed_field(name='LiteCoin Price:', value='price', inline=True)
                    embed1.set_footer(text='Bought LiteCoin at this time')
                    webhook1.add_embed(embed1)
                    webhook1.execute()
                    print(f'Core Investment: We bought ${second_amount} worth of litecoins')
                    core_quantity = 0
                    core_quantity += core_trade_amount/last_price
                    core_to_trade = False
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
                port_value = (portfolio - core_quantity)*last_price
                trade_amt = amt - port_value
                if last_eng == 0:
                    trade_amt = 0
                else:
                    trade_amt = trade_amt
                
                RT_portfolio_value = money_end + portfolio*last_price
                print(f'The Last Steategie value is "{last_eng}" and recommended exposure is "${trade_amt}"')
                print(f'Realt-Time Portfolio Value: ${RT_portfolio_value}')
                if trade_amt > 0:
                    buy(trade_amt, price=last_price)
                    if trade_amt == 0:
                        pass
                    else:
                        webhook2 = DiscordWebhook(url='https://discord.com/api/webhooks/853694685951295529/luTD_JlSV9uXpnyi-Ft5S877daATTXWzdnpmhJD86Zln-8XPxzRk427CfEbrkNbhOacI', rate_limit_retry=True, content = 'Hello')
                        embed2 = DiscordEmbed(title='Bought LiteCoin', description='Bought LiteCoin this much', color=0xffb029)
                        embed2.set_thumbnail(url='https://banner2.cleanpng.com/20180525/wal/kisspng-litecoin-cryptocurrency-bitcoin-logo-cryptocurrency-5b081f1979b524.5871818715272589054985.jpg')
                        embed2.add_embed_field(name='Price:', value='price', inline=True)
                        embed2.add_embed_field(name='Quantity:', value='price', inline=True)
                        embed2.add_embed_field(name='LiteCoin Price:', value='price', inline=True)
                        embed2.set_footer(text='Bought LiteCoin at this time')
                        webhook2.add_embed(embed)
                        webhook2.execute()
                        print(f'We have bought ${trade_amt} worth of litecoins')

                else:
                    sell(-trade_amt, price=last_price)
                    if trade_amt == 0:
                        pass
                    else:
                        webhook3 = DiscordWebhook(url='https://discord.com/api/webhooks/853694685951295529/luTD_JlSV9uXpnyi-Ft5S877daATTXWzdnpmhJD86Zln-8XPxzRk427CfEbrkNbhOacI', rate_limit_retry=True, content = 'Hello')
                        embed3 = DiscordEmbed(title='Sell LiteCoin', description='Sold LiteCoin this much', color=0xffb029)
                        embed3.set_thumbnail(url='https://banner2.cleanpng.com/20180525/wal/kisspng-litecoin-cryptocurrency-bitcoin-logo-cryptocurrency-5b081f1979b524.5871818715272589054985.jpg')
                        embed3.add_embed_field(name='Profit:', value='profit', inline=True)
                        embed3.add_embed_field(name='Quantity:', value='price', inline=True)
                        embed3.add_embed_field(name='LiteCoin Price:', value='price', inline=True)
                        embed3.set_footer(text='Sold LiteCoin at this time')
                        webhook3.add_embed(embed)
                        webhook3.execute()
                    print(f'We sold ${-trade_amt} worth of litecoin')
                
                trailingStop(last_price)

        ws = websocket.WebSocketApp(socket, on_message=on_message)
        ws.run_forever()