from pandas.core.frame import DataFrame
from Credentials import api,secret
import requests,json
import hmac
import hashlib
import time
import pandas
import time
import numpy as np


#setup of API
BASE_URL='https://api.crypto.com/v2/'
API_KEY = api
SECRET_KEY = secret

#get a candle stick info - especially closing price
def get_candle_stick(coins, time_frame):
    lista={}

    for coin in coins:
        lista[coin]=[]
        info=requests.get(BASE_URL+f'public/get-candlestick?instrument_name={coin}&timeframe={time_frame}')
        info=info.json()
        for item in info['result']['data']:
            lista[coin].append(item['c'])
    
    return lista

def current_price(price_dictionary):
    prices={}
    for price in price_dictionary:
        prices[price]=price_dictionary[price][-1]
    return prices


def get_account_summary(API_KEY,SECRET_KEY):

    req = {
        "id": 11,
        "method": "private/get-trades",
        'api_key':API_KEY,
        "params": {'start_ts':1641020400000},
        "nonce": int(time.time() * 1000)
        }
    
    param_str = ""

    MAX_LEVEL = 3


    def params_to_str(obj, level):
        if level >= MAX_LEVEL:
            return str(obj)

        return_str = ""
        for key in sorted(obj):
            return_str += key
            if isinstance(obj[key], list):
                for subObj in obj[key]:
                    return_str += params_to_str(subObj, ++level)
            else:
                return_str += str(obj[key])
        return return_str


    if "params" in req:
        param_str = params_to_str(req['params'], 0)

    payload_str = req['method'] + str(req['id']) + req['api_key'] + param_str + str(req['nonce'])

    req['sig'] = hmac.new(
        bytes(str(SECRET_KEY), 'utf-8'),
        msg=bytes(payload_str, 'utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()

    account_summary=requests.post(BASE_URL+req['method'], json=req, headers={'Content-Type':'application/json'})
    account_summary=account_summary.json()
    return account_summary


#calculate RSI to find the 'buy point'
def rsi(df):
    
    df['delta']=delta=df['Closed'].diff()
    df['up']=up=delta.clip(lower=0)
    df['down']=down=-1*delta.clip(upper=0)

    ema_up=up.ewm(com=13,adjust=False).mean()
    ema_down=down.ewm(com=13, adjust=False).mean()

    rs=ema_up/ema_down
    df['RSI']=100-(100/(1+rs))
    latest_rsi_values=(df['RSI'].iloc[-2:])
    return latest_rsi_values

def mvg_avg(df):
    df['ma5']=df['Closed'].rolling(window=5).mean()
    df['ma8']=df['Closed'].rolling(window=8).mean()
    df['ma13']=df['Closed'].rolling(window=13).mean()
    

def calulate_entry_point(rsi_values, coin):
    df=pandas.DataFrame(rsi_values)
    
    df['<30']=np.where(df['RSI']<55, True, False)
    df['raising?']=df['RSI'].is_monotonic
    example=set(df['<30'])
    example2=set(df['raising?'])
    print(df)
    if True in example and len(example2)==1:
        if True in example2:
            print(f'entry point for {coin}')
            return True

def calulcate_sell_point(buy_price, current_price):
    stop_loss=0.98*buy_price # <2% below buy price then sell
    profit_point=1.03*buy_price # >3% above buy price then sell

    if current_price>buy_price:
        difference=current_price-buy_price
        stop_loss+=difference

    if current_price<=stop_loss:
        return True

    if current_price>=profit_point:
        return True


