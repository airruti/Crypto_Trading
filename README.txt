Simple trading bot that consumes the Coinbase Pro API in order to automate trades. Setting parameters within the application is pretty self-explanatory.
I haven't decided yet whether I want to specify pairings, or automatically pair to USD. 
The bot waits 450 seconds per every check to update the price and determine whether it will buy or sell.
In order for the bot to function (whether through the Coinbase Sandbox API or an actual account), you must create a Secret, Key, and Passphrase through Coinbase and save it to a file called 'auth_credentials.py'

