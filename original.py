import auth_credentials
import cbpro
import time

BTC = 'BTC-USD'
LINK = 'LINK-USD'
BUY = 'buy'
SELL = 'sell'

cryptos = ['BTC-USD', 'LINK-USD', 'XLM-USD']

class CBMoney:
    def __init__(self, coinbase_client):
        self.client = coinbase_client
        
    def viewAccountBTC(self):
        accounts = self.client.get_account('4e1ee09d-8018-4a2c-8b25-ff76b3df7ee3')
        return accounts
    
    def viewAccountLINK(self):
        accounts = self.client.get_account('a996ba51-de3a-4fcd-aef7-77dfa1c0558d')
        return accounts
    
    def viewAccountXLM(self):
        accounts = self.client.get_account('a996ba51-de3a-4fcd-aef7-77dfa1c0558d')
        return accounts
    
    def currentPriceBTC(self):
        tick = self.client.get_product_ticker(product_id=cryptos[0])
        return tick['bid']
        
    def currentPriceLINK(self):
        tick = self.client.get_product_ticker(product_id=cryptos[1])
        return tick['bid']
        
    def marketOrder(self, crypto, action, quantity):
        trade = self.client.place_market_order(product_id=crypto, side=action, size=quantity)
        return trade
    
    def viewOrder(self, order_id):
        pass
    
def getXLM():
    richMethods.marketOrder(cryptos[0], BUY, 1)
    print()
    print('buying XLM...')
    print(richMethods.viewAccountXLM())
    print()
    
def sellXLM():
    richMethods.marketOrder(cryptos[0], SELL, 1)
    print()
    print('selling XLM...')
    print(richMethods.viewAccountXLM())
    print()
    
def getBTC():
    richMethods.marketOrder(cryptos[0], BUY, 1)
    print()
    print('buying BTC...')
    print(richMethods.viewAccountBTC())
    print()
    
def sellBTC():
    richMethods.marketOrder(cryptos[0], SELL, 1)
    print()
    print('selling BTC...')
    print(richMethods.viewAccountBTC())
    print()
        
def getLINK():
    richMethods.marketOrder(cryptos[1], BUY, 1)
    print()
    print('buying LINK...')
    print(richMethods.viewAccountLINK())
    print()
    
def sellLINK():
    richMethods.marketOrder(cryptos[1], SELL, 1)
    print()
    print('selling LINK...')
    print(richMethods.viewAccountLINK())
    print()
    
def start():
    oldPriceBTC = richMethods.currentPriceBTC()
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
while(True):
    start()
