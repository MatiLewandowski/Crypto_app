coins={'BTC_USDT':1,'CRO_USDT':0.44,'FTM_USDT':2.28,'SHIB_USDT':0.1}
prices_new={'BTC_USDT':1,'CRO_USDT':0.24,'FTM_USDT':1.28,'SHIB_USDT':0.0017}
prices=[30000,0.24, 1.28, 0.0017]
class CryptoCurrency():

    def __init__(self,name,price, amount=1000000):
        self.name=name
        self.price=price
        self.amount=amount

    def __str__(self):
        return f'{self.name} is worth now {self.price} $'

class Owned_crypto(CryptoCurrency):
    def __init__(self,name,price):
        super().__init__(name,price,amount=0)
    def __str__(self):
        return f'You have {self.amount} of {self.name}'

class Market():

    def __init__(self):
        self.market_crypto=[]
        for coin in coins:
            created_crypto=CryptoCurrency(coin, coins[coin])
            self.market_crypto.append(created_crypto)

    def update_price(self,new_price):
        for item in self.market_crypto:
            item.price=new_price[item.name]

    def sell_coins(self,coin, how_many):
        for item in self.market_crypto:
            if coin==item.name:
                item.amount-=how_many        




class Wallet():
    
    def __init__(self,budget):
        self.owned_coins=[]
        for item in coins:
            created_coin=Owned_crypto(item,coins[item])
            self.owned_coins.append(created_coin)
        self.budget=budget

    def add_coins(self,coin, how_many):
        for item in self.owned_coins:
            if item.name==coin:
                item.amount+=how_many-(how_many*0.004)
                self.budget-=how_many*item.price

        return coin,how_many

    def __str__(self):
        return f'You have {self.budget} $'

Crypto_market=Market()


MyWallet=Wallet(2000)
print(MyWallet)
for item in MyWallet.owned_coins:
    print(item)
name,amount=MyWallet.add_coins('BTC_USDT',1000)
Crypto_market.sell_coins(name,amount)

for item in MyWallet.owned_coins:
    print(item)

for item in Crypto_market.market_crypto:
    if item.name=='BTC_USDT':
        print(item.amount)

print(MyWallet.budget)
