import requests


def get_bitcoin_price():
    url = "https://api.upbit.com/v1/ticker?markets=BTC-KRW"
    response = requests.get(url)
    data = response.json()
    return data[0]['trade_price']

