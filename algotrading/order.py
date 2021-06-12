def order_stock(alpaca, symbols, count):
    alpaca.submit_order(
            symbol=symbols[count], 
            qty=1, 
            side='buy', 
            type='trailing_stop', 
            time_in_force='day', 
            trail_percent=0.15, 
        )