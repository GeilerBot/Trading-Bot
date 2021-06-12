from . import order_stock

def StrategyBuy(bar, alpaca, symbols, count, bar2):
    if bar.close >= bar.open and bar.open - bar.low > 0.1:
        print('Buying on Doji Candle!')
        order_stock(alpaca, symbols, count)
    elif bar.close >= bar.open and bar.open - bar.low > 0.7 :
        print('Buying on Hammer Candle!')
        order_stock(alpaca, symbols, count)
    elif bar.close >= bar.open and bar.open - bar.low > 0.1:
        print('Buying on Shooting-Star!')
        order_stock(alpaca, symbols, count)
    elif bar.close >= bar.open and bar.open - bar.low > 0.1:
        print('Buying on Bulish-Engulfing!')
        order_stock(alpaca, symbols, count)
    elif bar.close >= bar.open and bar.open - bar.low > 0.1:
        print('Buying on Bearish-Engulfing Candle!')
        order_stock(alpaca, symbols, count)
    elif bar.close >= bar.open and bar.open - bar.low > 0.1:
        print('Buying on Bulish-Harami Candle!')
        order_stock(alpaca, symbols, count)
    if bar.close >= bar.open and bar.open - bar.low > 0.1:
        print('Buying on Bearish-Harami Candle!')
        order_stock(alpaca, symbols, count)
    elif bar.close >= bar.open and bar.open - bar.low > 0.1:
        print('Buying on Hanging-Man Candle!')
        order_stock(alpaca, symbols, count)
    elif bar.close >= bar.open and bar.open - bar.low > 0.1:
        print('Buying on Dark-Cloud-Cover Candle!')
        order_stock(alpaca, symbols, count)
    else:
        print('Nothing to buy!')

def StrategySell(bar, alpaca, symbols, count):
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


