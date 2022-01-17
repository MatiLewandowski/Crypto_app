from Crypto_bot_app import get_candle_stick, current_price, rsi, calulate_entry_point, calulcate_sell_point
from Objective_Crypto_Market import CryptoCurrency, Owned_crypto, Market, Wallet
import pandas,time

#Settings to edit - change coins/timeframe to be followed by this algorithm
coins=['BTC_USDT','CRO_USDT','FTM_USDT','SHIB_USDT']
time_frame='5m'
buy_amount=1000


#initialize market (including only listed coins)
Crypto_market=Market()

#initialize wallet with 2000$
MyWallet=Wallet(2000)

rsi_dict={}

while True:
    lista=get_candle_stick(coins,time_frame)
    prices=current_price(lista)
    print(prices)
    
    for item in coins:
        df=pandas.DataFrame({'Closed':lista[item]})
        rsi_values=rsi(df)
        
        rsi_dict[item]=[rsi_values.iloc[-1]]
        if calulate_entry_point(rsi_values,item):
            MyWallet.add_coins(item,buy_amount)
            Crypto_market.sell_coins(item,buy_amount)
            bought_price=item.price

        if calulcate_sell_point(bought_price,item.price):
            pass
    rsi_df=pandas.DataFrame(rsi_dict)   
    print(rsi_df)

    time.sleep(20)
