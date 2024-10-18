import requests


# 업비트 API에서 모든 마켓의 종목 정보를 가져오는 함수
def get_markets():
    url = "https://api.upbit.com/v1/market/all"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"API 호출 오류: {response.status_code}")
        return None


# 체결 정보를 가져와서 매수 및 매도 체결량을 분석하는 함수
def get_trade_ticker(market):
    url = f"https://api.upbit.com/v1/trades/ticks?market={market}&count=200"
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"API 호출 오류: {response.status_code}")
        return None


# 체결 강도가 높은 상위 5개 종목을 찾아 출력하는 함수
def find_top_5_by_trade_strength():
    markets = get_markets()
    if not markets:
        return

    market_strengths = []

    # 각 종목의 체결 강도를 계산
    for market in markets:
        if "KRW-" in market['market']:  # KRW 마켓만 대상으로 필터링
            trade_ticker = get_trade_ticker(market['market'])
            if trade_ticker:
                # 체결 데이터를 분석하여 매수 및 매도 강도를 계산
                bid_volume = 0  # 매수 체결량
                ask_volume = 0  # 매도 체결량

                for trade in trade_ticker:
                    if trade['ask_bid'] == 'BID':  # 매수 체결
                        bid_volume += trade['trade_volume']
                    elif trade['ask_bid'] == 'ASK':  # 매도 체결
                        ask_volume += trade['trade_volume']

                if ask_volume > 0:
                    trade_strength = (bid_volume / ask_volume) * 100
                else:
                    trade_strength = 0  # 매도 체결이 없는 경우 강도는 0

                market_strengths.append({
                    'market': market['market'],
                    'trade_strength': trade_strength
                })

    # 체결 강도 기준으로 정렬하고 상위 5개 종목 출력
    market_strengths.sort(key=lambda x: x['trade_strength'], reverse=True)
    top_5 = market_strengths[:5]

    print("체결 강도가 가장 높은 상위 5개 종목:")
    for i, market in enumerate(top_5, start=1):
        print(f"{i}. {market['market']} - 체결 강도: {market['trade_strength']:.2f}%")


if __name__ == "__main__":
    find_top_5_by_trade_strength()
