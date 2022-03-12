import auth_credentials
import cbpro
import time
from multipledispatch import dispatch

cryptos = ['BTC', 'DOGE', 'FET', 'IOTX', 'IMX', 'ETH', 'XLM', 'OGN']
wait = 450

class CBMoney:
    def __init__(self, coinbase_client):
        self.client = coinbase_client

    def viewAccounts(self):
        accounts = self.client.get_accounts()
        myAccounts = []
        for account in accounts:
            if round(float(account['balance']), 4) != 0:
                myAccounts.append(account)
                print(f"{account['currency']}: {round(float(account['balance']), 5)}")
        return myAccounts
    
    def viewSingleAccount(self, coin: str):
        accounts = self.client.get_accounts()
        return list(filter(lambda account: account['currency'] == coin, accounts)) #definitely did not steal this off stackoverflow

    #wooooow method overloading in python!! who woulda thunk!! 
    @dispatch()
    def currentPrices(self):
        allAccounts = self.viewAccounts()
        ticks = []
        for account in allAccounts:
            if account['currency'] == "USD":
                print(f"Total USD: {'${:,.2f}'.format(float(account['balance']))}")
            elif account['currency'] in cryptos:
                ticks = self.client.get_product_ticker(product_id=f"{account['currency']}-USD")
                print(f"Current Price of {account['currency']}: {ticks['bid']}")
    
    @dispatch(str)
    def currentPrices(self, coin):
        tick = self.client.get_product_ticker(product_id=f"{coin}-USD")
        return tick['bid']
        
    def marketOrder(self, crypto, action, quantity): #must be a pair
        self.client.place_market_order(product_id=f"{crypto}-USD", side=action, size=quantity)
        print()
        if action == 'buy':
            print(f"buying {crypto}...")
        else : 
            print(f"selling {crypto}...")
        print(self.viewSingleAccount(crypto))
    
    def viewOrder(self, order_id):
        pass

def countdown(time_sec):
    while time_sec:
        mins, secs = divmod(time_sec, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        time_sec -= 1

def start():
    oldPriceBTC = richMethods.currentPrices("BTC")
    oldPriceBTC = float(oldPriceBTC)
    
    time.sleep(wait)
    
    old2PriceBTC = richMethods.currentPrices("BTC")
    old2PriceBTC = float(old2PriceBTC)
    
    time.sleep(wait)
    
    newPriceBTC = richMethods.currentPrices("BTC")
    newPriceBTC = float(newPriceBTC)
    
    if(newPriceBTC < ((oldPriceBTC*0.99) or (old2PriceBTC*0.99))):
        richMethods.marketOrder("BTC", 'buy', 10)
    elif(newPriceBTC > ((oldPriceBTC*1.02) or (old2PriceBTC*1.02))):
        richMethods.marketOrder("BTC", 'sell', 10)
        
    richMethods.currentPrices()

def displayInfo(currentPriceBTC, currentPriceLINK):
    print(f"Current Bitcoin price: {currentPriceBTC}")
    print(f"Current Chainlink price: {currentPriceLINK}")
    
if __name__ == "__main__":
    auth_client = cbpro.AuthenticatedClient(auth_credentials.money_key,
                                            auth_credentials.money_secret,
                                            auth_credentials.money_pass)

richMethods = CBMoney(auth_client)
print('Waiting for changes...')
# while(True):
#     start()

richMethods.viewAccounts()