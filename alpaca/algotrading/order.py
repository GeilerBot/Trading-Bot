def order_stock(alpaca, symbols, count, buy_type):
    alpaca.submit_order(
            symbol=symbols[count], 
            qty=1, 
            side=buy_type, 
            type='trailing_stop', 
            time_in_force='day', 
            trail_percent=0.15, 
        )