import auth_credentials
import cbpro
import time
from multipledispatch import dispatch

cryptos = {"BTC": 0.0002, "IMX": 3, "DOGE": 50} #cryptos that will be used and how many to buy/sell
wait = 300 #15 minutes

class CBMoney:
    def __init__(self, coinbase_client):
        self.client = coinbase_client

    def myAccounts(self):
        accounts = self.client.get_accounts()
        myAccounts = []
        for account in accounts:
            if float(account['balance']) != 0:
                myAccounts.append(account)
                #print(f"{account['currency']}: {round(float(account['balance']), 5)}")
        return myAccounts
    
    def viewSingleAccount(self, coin: str):
        accounts = self.client.get_accounts()
        account = list(filter(lambda account: account['currency'] == coin.upper(), accounts)) #definitely did not steal this off stackoverflow
        print(f"{account[0]['currency']}: {account[0]['balance']}")
        return account

    #method overloading in python!! who woulda thunk!! 
    @dispatch()
    def currentPrices(self):
        allAccounts = self.myAccounts()
        for account in allAccounts:
            if account['currency'] == "USD":
                print(f"Total USD: {'${:,.2f}'.format(float(account['balance']))}")
            elif account['currency'] in cryptos:
                tick = self.client.get_product_ticker(product_id=f"{account['currency']}-USD")
                print(f"Current Price of {account['currency']}: {tick['bid']}")
    
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

    def limitOrder(self, crypto, action, quantity):
        pass
    
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
    old_prices = []
    new_prices = []

    for crypto in cryptos:
        old_prices.append(float(richMethods.currentPrices(crypto)))
    
    countdown(wait)
    
    i = 0
    for key, value in cryptos.items():
        new_prices.append(float(richMethods.currentPrices(key)))

        if(new_prices[i] < ((old_prices[i]*0.97))):
            richMethods.marketOrder(key, 'buy', value)
        elif(new_prices[i] > ((old_prices[i]*1.05))):
            richMethods.marketOrder(key, 'sell', value)
        
        i += 1
        
    richMethods.currentPrices()
    
if __name__ == "__main__":
    auth_client = cbpro.AuthenticatedClient(auth_credentials.money_key,
                                            auth_credentials.money_secret,
                                            auth_credentials.money_pass)

richMethods = CBMoney(auth_client)
while(True):
    print('Waiting for changes...')
    start()
    print()