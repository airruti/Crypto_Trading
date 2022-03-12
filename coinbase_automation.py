import auth_credentials
import cbpro
import time
from multipledispatch import dispatch

cryptos = ['BTC', 'DOGE', 'FET']
time_to_wait = 0

class CBMoney:
    def __init__(self, coinbase_client):
        self.client = coinbase_client

    def viewAccounts(self):
        accounts = self.client.get_accounts()
        myAccounts = []
        for account in accounts:
            if account['balance'] != '0.0000000000000000':
                myAccounts.append(account)
        return myAccounts
    
    def viewSingleAccount(self, coin: str):
        allAccounts = self.viewAccounts()
        for account in allAccounts:
            if account["currency"] == coin.upper():
                return account
        return f"You do not own any {coin}"

    #wooooow method overloading in python!! who woulda thunk!! 
    @dispatch()
    def currentPrices(self):
        allAccounts = self.viewAccounts()
        ticks = []
        for account in allAccounts:
            if account['currency'] == "USD":
                continue
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
    
def start():
    oldPriceBTC = richMethods.currentPrices("BTC")
    oldPriceLINK = richMethods.currentPriceLINK()
    oldPriceBTC = float(oldPriceBTC)
    oldPriceLINK = float(oldPriceLINK)
    
    time.sleep(450)
    
    old2PriceBTC = richMethods.currentPriceBTC()
    old2PriceLINK = richMethods.currentPriceLINK()
    old2PriceBTC = float(old2PriceBTC)
    old2PriceLINK = float(old2PriceLINK)
    
    time.sleep(450)
    
    newPriceBTC = richMethods.currentPriceBTC()
    newPriceLINK = richMethods.currentPriceLINK()
    newPriceBTC = float(newPriceBTC)
    newPriceLINK = float(newPriceLINK)
    
    if(newPriceBTC < ((oldPriceBTC*0.99) or (old2PriceBTC*0.99))):
        getBTC()
    if(newPriceBTC > ((oldPriceBTC*1.02) or (old2PriceBTC*1.02))):
        sellBTC()
    if(newPriceLINK < ((oldPriceLINK*0.99) or (old2PriceLINK*0.99))):
        getLINK()
    if(newPriceLINK > ((oldPriceLINK*1.02) or (old2PriceLINK*1.02))):
        sellLINK()
        
    displayInfo(newPriceBTC, newPriceLINK)
    print('Waiting for changes...')

def displayInfo(currentPriceBTC, currentPriceLINK):
    print(f"Current Bitcoin price: {currentPriceBTC}")
    print(f"Current Chainlink price: {currentPriceLINK}")
    
if __name__ == "__main__":
    auth_client = cbpro.AuthenticatedClient(auth_credentials.money_key,
                                            auth_credentials.money_secret,
                                            auth_credentials.money_pass)

richMethods = CBMoney(auth_client)
print('Waiting for changes...')

richMethods.currentPrices()
btc = richMethods.currentPrices("BTC")
print(btc)
        