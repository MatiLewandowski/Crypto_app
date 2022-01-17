coins={'BTC_USDT':1,'CRO_USDT':0.44,'FTM_USDT':2.28,'SHIB_USDT':0.1}
prices_new={'BTC_USDT':20,'CRO_USDT':0.24,'FTM_USDT':1.28,'SHIB_USDT':0.0017}
prices_new1={'BTC_USDT':25,'CRO_USDT':0.34,'FTM_USDT':1.88,'SHIB_USDT':0.0067}


#crypto coin class object for cryptomarket
class CryptoCurrency():

    def __init__(self,name,price, amount=1000000):
        self.name=name
        self.price=price
        self.amount=amount

    def __str__(self):
        return f'{self.name} is worth now {self.price} $'


#crypto coin object (taken from original) with changed amount for client 'wallet' purpose
class Owned_crypto(CryptoCurrency):
    def __init__(self,name,price):
        super().__init__(name,price,amount=0)
    def __str__(self):
        return f'You have {self.amount} of {self.name}'


#Market object representing the crypto market with coins
class Market():

    def __init__(self):
        self.market_crypto=[]
        for coin in coins:
            created_crypto=CryptoCurrency(coin, coins[coin])
            self.market_crypto.append(created_crypto)

    def sell_coins(self,coin, how_many):
        for item in self.market_crypto:
            if coin==item.name:
                item.amount-=how_many

    def buy_coins(self,coin,how_many):
        for item in self.market_crypto:
            if coin==item.name:
                item.amount+=how_many

    def update_price(self,new_price):
        for item in self.market_crypto:
            item.price=new_price[item.name]
        return self.market_crypto


#Wallet class object representing client wallet with amount of coins
class Wallet():
    
    def __init__(self,budget):
        self.owned_coins=[]
        self.budget=budget

    def add_coins(self,coin, how_many):
        created_coin=Owned_crypto(coin,coins[coin])
        self.owned_coins.append(created_coin)
        for item in self.owned_coins:
            if item.name==coin:
                item.amount+=how_many-(how_many*0.004) #0.4% transaction fee
                self.budget-=how_many*item.price

        return coin,how_many

    def sell_coins(self,coin,how_many):
        for item in self.owned_coins:
            if item.name==coin:
                if how_many<=item.amount:
                    item.amount-=how_many
                else:
                    how_many=item.amount
                    item.amount=0
                self.budget+=(0.996*how_many)*item.price #0.4% transaction fee
            if item.amount==0:
                self.owned_coins.remove(item)
        return coin, how_many

    def update_price(self,coins):
        for item in self.owned_coins:
            for i in coins:
                if item.name==i.name:
                    item.price=i.price

    def __str__(self):
        return f'You have {self.budget} $'



#Testing some functionality as: buying & selling coins between market and user wallet

for item in Crypto_market.market_crypto:
    print(item.price)

name,amount=MyWallet.add_coins('BTC_USDT',1000)
Crypto_market.sell_coins(name,amount)

MyWallet.update_price(Crypto_market.update_price(prices_new))

for item in Crypto_market.market_crypto:
    print(item.price)

MyWallet.update_price(Crypto_market.update_price(prices_new1))


for item in MyWallet.owned_coins:
    print(item.price)

