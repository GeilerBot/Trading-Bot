import alpaca_trade_api as tradeapi
from stream import consumer_thread
from algotrading.strategies import Strategy
import threading
import asyncio
import time
from alpaca_trade_api import Stream
from alpaca_trade_api.common import URL
import config

secret = config.secret
key = config.key

#Testing the Account Activity
#****************************
alpaca_url = 'https://paper-api.alpaca.markets'
alpaca = tradeapi.REST(key, secret, alpaca_url, api_version='v2')
account = alpaca.get_account()
print(account.status)
#****************************

conn = Stream(
                key,
                secret,
                base_url=URL('https://paper-api.alpaca.markets'),
                data_feed='sip'
            )

current_quote = []
current_trade = []
current_bar = []
symbols = ['TSLA', 'MSFT', 'FB', 'ETSY', 'TWLO', 'AMD', 'ROKU', 'ZIOP', 'BBGI', 'BSET']
loop = asyncio.get_event_loop()

        #On Each Minute
def stream_thread():
    consumer_thread(current_quote, current_trade, current_bar, symbols, loop, conn)

# def on_minute(bar):
             #Entry
             # if market_time.is_open != False:
#                 if bar.close >= bar.open and bar.open - bar.low > 0.1:
#                     print('Buying on Doji Candle!') 
#                     alpaca.submit_order( 
#                         symbol=symbols[0], 
#                         qty=1, 
#                         side='buy', 
#                         type='trailing_stop', 
#                         time_in_force='day', 
#                         limit_price=1000,
#                         trail_percent=1, 
#                         )
#                 else:
#                     print('Nothing to buy')
                 #TODO: Take Profit at 1% increase (E.g 170 take profit at 171.7)

while True: 
            buyingPower = 4 * (float(account.last_equity) - float(account.last_maintenance_margin))
            print(buyingPower)
            market_time = alpaca.get_clock()
            print(market_time)
            if market_time.is_open != False and buyingPower >= 1000:
                threading.Thread(target=stream_thread, args=2).start
                time.sleep(60)
                loop.run_until_complete(conn.stop_ws())
                print(f'The results:\n\n{current_bar[-1]}, \n{current_trade[-1]}, \n{current_quote[-1]}')
                limit_price = current_trade[-1].price*1.04
                # print(limit_price)
                if float(buyingPower) > limit_price:
                    Strategy(current_bar[-1], alpaca, symbols, 0)
            else:
                if market_time.is_open == False:
                    print(f'Market is closed!\n\n{market_time}')
                else:
                    print(f"Your buying-power ran out. There is only {buyingPower}$ left.")
                current_trade.clear
                current_quote.clear
                current_bar.clear
                time.sleep(60)
