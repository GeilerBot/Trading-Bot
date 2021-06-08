from alpaca_trade_api import Stream, stream
import alpaca_trade_api as tradeapi
from alpaca_trade_api.common import URL


    
async def DataStream(symbol):
    async def bar_callback(b):
        print('bar', b)

    async def trade_callback(t):
        print('trade', t)


    async def quote_callback(q):
            print('quote', q)

    # Initiate Class Instance
    stream = Stream('PK846E5V8HQPZOR052YA',
                    'CeiY5b4wxFwGUClZ3EIAmjFufvhuSISXXbYaXMwg',
                    base_url=URL('https://paper-api.alpaca.markets'),
                    data_feed='sip')  # <- replace to SIP if you have PRO subscription

    # subscribing to event
    trades = stream.subscribe_trades(trade_callback, symbol)
    quotes = stream.subscribe_quotes(quote_callback, symbol)
    bars = stream.subscribe_bars(bar_callback, symbol)
    values = [trades, quotes, bars]
    await stream.run()
    return values