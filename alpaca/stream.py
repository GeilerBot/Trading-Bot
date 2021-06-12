import asyncio

def consumer_thread(current_quote, current_trade, current_bar, symbols, loop, conn):
        try:
            # make sure we have an event loop, if not create a new one
            loop = asyncio.get_event_loop()
            loop.set_debug(True)
        except RuntimeError:
            asyncio.set_event_loop(asyncio.new_event_loop())

        async def bar_callback(b):
                print('bar', b)
                current_bar.append(b)

        async def trade_callback(t):
                # print('trade', t)
                current_trade.append(t)

        async def quote_callback(q):
                # print('quote', q)
                current_quote.append(q)
      
        async def trade_updates_callback(tu):
                print('trade_updates', tu)

        # subscribing to event
        conn.subscribe_trades(trade_callback, symbols[0])
        conn.subscribe_quotes(quote_callback, symbols[0])
        conn.subscribe_bars(bar_callback, symbols[0])
        conn.subscribe_trade_updates(trade_updates_callback)
        conn.run()

