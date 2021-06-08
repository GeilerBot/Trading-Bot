import alpaca_trade_api as tradeapi
from stream import DataStream

#Testing the Account Activity
#****************************
api = tradeapi.REST('PK846E5V8HQPZOR052YA','CeiY5b4wxFwGUClZ3EIAmjFufvhuSISXXbYaXMwg','https://paper-api.alpaca.markets')
account = api.get_account()
print(account.status)
#****************************

class PythonTradingBot(object):
    def __init__(self):
        self.alpaca_url = 'https://paper-api.alpaca.markets'
        self.alpaca = tradeapi.REST('PK846E5V8HQPZOR052YA','CeiY5b4wxFwGUClZ3EIAmjFufvhuSISXXbYaXMwg',self.alpaca_url, api_version='v2')
    def run(self):    
        async def looper(self):
        #On Each Minute
            async def on_minute(conn, channel, bar):
            #Entry
                if bar.close >= bar.open and bar.open - bar.low > 0.1:
                    print('Buying on Doji Candle!')
                    self.alpaca.submit_order("MSFT", 1, 'buy', 'market', 'day')
                #TODO: Take Profit at 1% increase (E.g 170 take profit at 171.7)
            r = await DataStream('TSLA')
            on_minute(r[2])

        
bd = PythonTradingBot()
bd.run()
