from stream import DataStream
from alpaca_trade_api import Stream, stream
import alpaca_trade_api as tradeapi
from alpaca_trade_api.common import URL
import threading
import asyncio
import time

bar = []
quote = []
trade = []

def consumer_thread():
    try:
        # make sure we have an event loop, if not create a new one
        loop = asyncio.get_event_loop()
        loop.set_debug(True)
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

    async def bar_callback(b):
                print('bar', b)
                bar.append(b)

    async def trade_callback(t):
                print('trade', t)
                trade.append(t)


    async def quote_callback(q):
                    print('quote', q)
                    quote.append(q)

    # Initiate Class Instance
    global conn
    conn = Stream(
                'PK846E5V8HQPZOR052YA',
                'CeiY5b4wxFwGUClZ3EIAmjFufvhuSISXXbYaXMwg',
                base_url=URL('https://paper-api.alpaca.markets'),
                data_feed='sip'
            )

                # subscribing to event
    conn.subscribe_trades(trade_callback, 'TSLA')
    conn.subscribe_quotes(quote_callback, 'TSLA')
    conn.subscribe_bars(bar_callback, 'TSLA')
    conn.run()

loop = asyncio.get_event_loop()

while 1:
        threading.Thread(target=consumer_thread).start()
        time.sleep(60)
        loop.run_until_complete(conn.stop_ws())
        values = [trade, quote, bar]
        print(f'\n\n\n\n\n\n\nThe results:\n\n{values}')
        time.sleep(20)
        values.clear