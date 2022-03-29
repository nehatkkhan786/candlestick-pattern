from turtle import clear
import ta
import ccxt
import pandas as pd
from ta.volatility import BollingerBands, AverageTrueRange
import re
import pandas_ta as pta
import talib
from dhooks import Webhook

import schedule
import time



BINANCE_API_KEY = 'RnOw8aNjU3hFgQyCF9umvTlUaOfkQj7cIVBo4PLZg7gonEwrvtIhZcDR1d20SOwn'
BINANCE_SECRET_KEY = 'x7hU7xmYnAee3lYR6KrkhLcwNYOQiB86IcuKqCMng0cuZeZf9Avt0sKo59gmjoAt'

BULLISH_HOOK = Webhook('https://discord.com/api/webhooks/958348993417588746/eX-TqTFdxxWWlOZw7exIALCRc_5OYPLxs9bhZ8n2yS9Eqnz7EasWJMaClKY9PIs7GWJP')
BEARISH_HOOK = Webhook('https://discord.com/api/webhooks/958354220686389249/6P_mGbb-S3i2agQPBMNPG5F2fNVVgarZqi_C-WQKmQ0b6EpNBPqP8U-s5Q6meFKPkNCW')


exchange = ccxt.binance({
    'apiKey': BINANCE_API_KEY,
    'secret': BINANCE_SECRET_KEY
})

markets = exchange.load_markets()

coin_pairs = exchange.symbols
valid_coin_pairs = []
overbought = []
oversold = []
regx = '^.*/USDT'

for coin_pair in coin_pairs:
    if re.match(regx,coin_pair):
        valid_coin_pairs.append(coin_pair)


def get_data(coin, timeframe):
    data = exchange.fetch_ohlcv(coin, timeframe)
    df = pd.DataFrame(data,columns=['timestamp', 'open','high', 'low', 'close', 'volume'] )
    return df

BullishEngulfing = []
BearishEngulfing = []

for coin in valid_coin_pairs:
    data= get_data(coin, '4h')
    engulfing = talib.CDLENGULFING(data['open'], data['high'], data['low'], data['close'])
    last_engulfing = engulfing.iloc[-2]
    if last_engulfing == 100:
        BullishEngulfing.append(coin)
    elif last_engulfing == -100:
        BearishEngulfing.append(coin)

BULLISH_HOOK.send('\n' .join(BullishEngulfing))
BEARISH_HOOK.send('\n' .join(BearishEngulfing))


def analyseCoin():
    BullishEngulfing = []
    BearishEngulfing = []

    for coin in valid_coin_pairs:
        data= get_data(coin, '4h')
        engulfing = talib.CDLENGULFING(data['open'], data['high'], data['low'], data['close'])
        last_engulfing = engulfing.iloc[-2]
        if last_engulfing == 100:
            BullishEngulfing.append(coin)
        elif last_engulfing == -100:
            BearishEngulfing.append(coin)
    BULLISH_HOOK.send('\n' .join(BullishEngulfing))
    BEARISH_HOOK.send('\n' .join(BearishEngulfing))


schedule.every(5).minutes.do(analyseCoin)

while True:
    schedule.run_pending()
    time.sleep(1)