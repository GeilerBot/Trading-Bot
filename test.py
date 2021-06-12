#This file is only for testing things!
#≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈
import config
import alpaca_trade_api as tradeapi

#Api Keys
secret = config.secret
key = config.key

#Authentication
alpaca_url = 'https://paper-api.alpaca.markets'
alpaca = tradeapi.REST(key, secret, alpaca_url, api_version='v2')
account = alpaca.get_account()
print(account.status)

#Write your code below:
#**********************

#Variables
#≈≈≈≈≈≈≈≈≈


#≈≈≈≈≈≈≈≈≈
#Functions
#≈≈≈≈≈≈≈≈≈


        

#≈≈≈≈≈≈≈≈≈
#Run->Code
#≈≈≈≈≈≈≈≈≈
