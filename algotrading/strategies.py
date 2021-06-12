from .order import order_stock

def Strategy(bar, alpaca, symbols, count):
    if bar.close >= bar.open and bar.open - bar.low > 0.1:
        print('Buying on Doji Candle!')
        order_stock(alpaca, symbols, count)
    elif bar.close >= bar.open and bar.open - bar.low > 0.1:
        print('Buying on Doji Candle!')
        order_stock(alpaca, symbols, count)
    elif bar.close >= bar.open and bar.open - bar.low > 0.1:
        print('Buying on Doji Candle!')
        order_stock(alpaca, symbols, count)
    elif bar.close >= bar.open and bar.open - bar.low > 0.1:
        print('Buying on Doji Candle!')
        order_stock(alpaca, symbols, count)
    elif bar.close >= bar.open and bar.open - bar.low > 0.1:
        print('Buying on Doji Candle!')
        order_stock(alpaca, symbols, count)
    elif bar.close >= bar.open and bar.open - bar.low > 0.1:
        print('Buying on Doji Candle!')
        order_stock(alpaca, symbols, count)
    if bar.close >= bar.open and bar.open - bar.low > 0.1:
        print('Buying on Doji Candle!')
        order_stock(alpaca, symbols, count)
    elif bar.close >= bar.open and bar.open - bar.low > 0.1:
        print('Buying on Doji Candle!')
        order_stock(alpaca, symbols, count)
    elif bar.close >= bar.open and bar.open - bar.low > 0.1:
        print('Buying on Doji Candle!')
        order_stock(alpaca, symbols, count)
    elif bar.close >= bar.open and bar.open - bar.low > 0.1:
        print('Buying on Doji Candle!')
        order_stock(alpaca, symbols, count)
    else:
        print('Nothing to buy!')
