import auth_sandbox
import cbpro
import time
import datetime

"""import requests
from base64 import b64decode, b64encode
import hmac
import json

url = "https://api.exchange.coinbase.com/accounts"
method = 'GET'
requestPath = '/accounts'
body = ''
cb_access_timestamp = str(time.time())
message = cb_access_timestamp + method + requestPath + body
key = b64decode(auth_credentials.money_secret)
signature = hmac.new(key, message.encode(), digestmod='sha256')
cb_access_sign = b64encode(signature.digest())

headers = {
    "Accept": "application/json",
    "CB-ACCESS-KEY": auth_credentials.money_key,
    "CB-ACCESS-PASSPHRASE": auth_credentials.money_pass,
    "CB-ACCESS-TIMESTAMP": cb_access_timestamp,
    "CB-ACCESS-SIGN": cb_access_sign
    }

response = requests.request("GET", url, headers=headers)

accounts = response.json()"""

balanceLimit = 50
buyRatio = 0.996
sellRatio = 1.008
timePerCheck = 5 #modify depending on how +-volatile the day is. 

actions = ['buy', 'sell']
cryptos = ['BTC', 'LINK']

class CBMoney:
    def __init__(self, coinbase_client):
        self.client = coinbase_client
        
    def viewCash(self):
        usd = self.client.get_account('71f39a56-26a4-46f6-92e2-a534e7200779')
        return usd['balance']
    
    def getAcc(self, crypto):
        accounts = self.client.get_accounts()
        return list(filter(lambda account: account['currency'] == crypto, accounts))
    
    def currentPrice(self, crypto):
        tick = self.client.get_product_ticker(product_id=f"{crypto}-USD")
        return tick['bid']
        
    def marketOrder(self, crypto, action, quantity):
        trade = self.client.place_market_order(product_id=f"{crypto}-USD", side=action, size=quantity)
        return trade
    
def tradeBTC(action):
    richMethods.marketOrder(cryptos[0], action, .001)
    print(f"{action} BTC, current time: {datetime.datetime.now()}")
    print(richMethods.getAcc(cryptos[0]))
    print()
    
def tradeLINK(action):
    richMethods.marketOrder(cryptos[1], action, .2)
    print(f"{action} LINK, current time: {datetime.datetime.now()}")
    print(richMethods.getAcc(cryptos[1]))
    print()
    
def tradeXLM(action):
    richMethods.marketOrder(cryptos[2], action, 15)
    print()
    print(f"{action} XLM, current time: {datetime.datetime.now()}")
    print(richMethods.getAcc(cryptos[2]))
    print()
    
def tradeADA(action):
    richMethods.marketOrder(cryptos[3], action, 2)
    print(f"{action} ADA, current time: {datetime.datetime.now()}")
    print(richMethods.getAcc(cryptos[3]))
    print()
    
def tradeAMP(action):
    richMethods.marketOrder(cryptos[4], action, 105)
    print()
    print(f"{action} AMP, current time: {datetime.datetime.now()}")
    print(richMethods.getAcc(cryptos[4]))
    print()
    
def countdown(time_sec):
    while time_sec:
        mins, secs = divmod(time_sec, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        time_sec -= 1
    
def displayInfo():
    for i in range(len(cryptos)):
        print(f"Current {cryptos[i]} price: {richMethods.currentPrice(cryptos[i])}") 
    print()
    print(f"Current USD: {richMethods.viewCash()}")
    print()
    
def buy_sell():
    print('Buy and sell mode')
    print()
    print('Waiting for changes...')
    print()
    oldPriceBTC = richMethods.currentPrice(cryptos[0])
    oldPriceLINK = richMethods.currentPrice(cryptos[1])
    oldPriceBTC = float(oldPriceBTC)
    oldPriceLINK = float(oldPriceLINK)
    
    countdown(timePerCheck)
    
    old2PriceBTC = richMethods.currentPrice(cryptos[0])
    old2PriceLINK = richMethods.currentPrice(cryptos[1])
    old2PriceBTC = float(old2PriceBTC)
    old2PriceLINK = float(old2PriceLINK)
    
    print('-------------------------First pass-------------------------')
    print()
    if(old2PriceBTC < (oldPriceBTC*buyRatio)):
        tradeBTC(actions[0])
    if(old2PriceBTC > (oldPriceBTC*sellRatio)):
        tradeBTC(actions[1])
    if(old2PriceLINK < (oldPriceLINK*buyRatio)):
        tradeLINK(actions[0])
    if(old2PriceLINK > (oldPriceLINK*sellRatio)):
        tradeLINK(actions[1])
        
    displayInfo()
    print('Waiting for changes...')
    print()
    
    countdown(timePerCheck)
    
    newPriceBTC = richMethods.currentPrice(cryptos[0])
    newPriceLINK = richMethods.currentPrice(cryptos[1])
    newPriceBTC = float(newPriceBTC)
    newPriceLINK = float(newPriceLINK)
    
    print('-------------------------Second pass-------------------------')
    print()
    if(newPriceBTC < ((oldPriceBTC*buyRatio) or (old2PriceBTC*buyRatio))):
        tradeBTC(actions[0])
    if(newPriceBTC > ((oldPriceBTC*sellRatio) or (old2PriceBTC*sellRatio))):
        tradeBTC(actions[1])
    if(newPriceLINK < ((oldPriceLINK*buyRatio) or (old2PriceLINK*buyRatio))):
        tradeLINK(actions[0])
    if(newPriceLINK > ((oldPriceLINK*sellRatio) or (old2PriceLINK*sellRatio))):
        tradeLINK(actions[1])
        
    displayInfo()
    print('Waiting for changes...')
    print()
    
    countdown(timePerCheck)
    
    sellSomeBTC = richMethods.currentPrice(cryptos[0])
    sellSomeLINK = richMethods.currentPrice(cryptos[1])
    sellSomeBTC = float(sellSomeBTC)
    sellSomeLINK = float(sellSomeLINK)
    
    print('-------------------------Third pass-------------------------')
    print()
    if(sellSomeBTC > ((oldPriceBTC*sellRatio) or (old2PriceBTC*sellRatio) or (newPriceBTC*sellRatio))):
        tradeBTC(actions[1])
    if(sellSomeLINK > ((oldPriceLINK*sellRatio) or (old2PriceLINK*sellRatio) or (newPriceLINK*sellRatio))):
        tradeLINK(actions[1])
        
    displayInfo()
    
def only_sell():
    print('sell-only mode')
    print()
    print('Waiting for changes...')
    print()
    oldPriceBTC = richMethods.currentPrice(cryptos[0])
    oldPriceLINK = richMethods.currentPrice(cryptos[1])
    oldPriceBTC = float(oldPriceBTC)
    oldPriceLINK = float(oldPriceLINK)
    
    countdown(timePerCheck)
    
    old2PriceBTC = richMethods.currentPrice(cryptos[0])
    old2PriceLINK = richMethods.currentPrice(cryptos[1])
    old2PriceBTC = float(old2PriceBTC)
    old2PriceLINK = float(old2PriceLINK)
    
    print('-------------------------First pass-------------------------')
    print()
    if(old2PriceBTC > (oldPriceBTC*sellRatio)):
        tradeBTC(actions[1])
    if(old2PriceLINK > (oldPriceLINK*sellRatio)):
        tradeLINK(actions[1])
        
    displayInfo()
    print('Waiting for changes...')
    print()
    
    countdown(timePerCheck)
    
    newPriceBTC = richMethods.currentPrice(cryptos[0])
    newPriceLINK = richMethods.currentPrice(cryptos[1])
    newPriceBTC = float(newPriceBTC)
    newPriceLINK = float(newPriceLINK)
    
    print('-------------------------Second pass-------------------------')
    print()
    if(newPriceBTC > ((oldPriceBTC*sellRatio) or (old2PriceBTC*sellRatio))):
        tradeBTC(actions[1])
    if(newPriceLINK > ((oldPriceLINK*sellRatio) or (old2PriceLINK*sellRatio))):
        tradeLINK(actions[1])
        
    displayInfo()
    print('Waiting for changes...')
    print()
        
    countdown(timePerCheck)
    
    sellSomeBTC = richMethods.currentPrice(cryptos[0])
    sellSomeLINK = richMethods.currentPrice(cryptos[1])
    sellSomeBTC = float(sellSomeBTC)
    sellSomeLINK = float(sellSomeLINK)
    
    print('-------------------------Third pass-------------------------')
    print()
    if(sellSomeBTC > ((oldPriceBTC*sellRatio) or (old2PriceBTC*sellRatio) or (newPriceBTC*sellRatio))):
        tradeBTC(actions[1])
    if(sellSomeLINK > ((oldPriceLINK*sellRatio) or (old2PriceLINK*sellRatio) or (newPriceLINK*sellRatio))):
        tradeLINK(actions[1])
        
    displayInfo()
    
def start():
    acc_balance = richMethods.viewCash()
    acc_balance = float(acc_balance)
    if(acc_balance > balanceLimit):
        buy_sell()
        print('===================================================================')
        print()
    else:
        only_sell()
        print('===================================================================')
        print()
    
if __name__ == "__main__":
    auth_client = cbpro.AuthenticatedClient(auth_sandbox.sandbox_key,
                                            auth_sandbox.sandbox_secret,
                                            auth_sandbox.sandbox_pass,
                                            api_url="https://api-public.sandbox.pro.coinbase.com")
richMethods=CBMoney(auth_client)
while(True):
    start()