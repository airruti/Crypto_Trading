import auth_sandbox
import cbpro
import time
import datetime

buyRatio = 0.999
sellRatio = 1.003
timePerCheck = 5

actions = ['buy', 'sell']
cryptos = ['BTC']

class CBPro:
    def __init__(self, coinbase_client):
        self.client = coinbase_client
        
    def viewCash(self):
        balance = self.client.get_account('71f39a56-26a4-46f6-92e2-a534e7200779')
        return balance['balance']
     
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
    richMethods.marketOrder(cryptos[0], action, 1)
    print(f"{action} BTC...")
    print(richMethods.getAcc(cryptos[0]))
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
    
def start():
    print('Waiting for changes...')
    print()
    oldPriceBTC = richMethods.currentPrice(cryptos[0])
    oldPriceBTC = float(oldPriceBTC)
    
    countdown(timePerCheck)
    
    old2PriceBTC = richMethods.currentPrice(cryptos[0])
    old2PriceBTC = float(old2PriceBTC)
    
    print('-------------------------First pass-------------------------')
    print()
    if(old2PriceBTC < (oldPriceBTC*buyRatio)):
        tradeBTC(actions[0])
    if(old2PriceBTC > (oldPriceBTC*sellRatio)):
        tradeBTC(actions[1])
    
    displayInfo()
    print('Waiting for changes...')
    print()
    
    countdown(timePerCheck)
    
    newPriceBTC = richMethods.currentPrice(cryptos[0])
    newPriceBTC = float(newPriceBTC)
    
    print('-------------------------Second pass-------------------------')
    print()
    if(newPriceBTC < ((oldPriceBTC*buyRatio) or (old2PriceBTC*buyRatio))):
        tradeBTC(actions[0])
    if(newPriceBTC > ((oldPriceBTC*sellRatio) or (old2PriceBTC*sellRatio))):
        tradeBTC(actions[1])
        
    displayInfo()
    
if __name__ == "__main__":
    auth_client = cbpro.AuthenticatedClient(auth_sandbox.sandbox_key,
                                            auth_sandbox.sandbox_secret,
                                            auth_sandbox.sandbox_pass,
                                            api_url='https://api-public.sandbox.pro.coinbase.com')

richMethods = CBPro(auth_client)
# print(datetime.datetime.now())
while(True):
    start()