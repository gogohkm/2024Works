# 가장 거래량이 높은 3개의 종목을 병령처리로 찾는다.

import requests
import pandas as pd
from time import sleep
from concurrent.futures import ThreadPoolExecutor, as_completed


# 업비트 마켓 코드 가져오기
def get_market_codes():
    url = "https://api.upbit.com/v1/market/all"
    try:
        response = requests.get(url)
        response.raise_for_status()  # HTTP 에러 발생 시 예외 처리
        markets = response.json()
        return [market['market'] for market in markets if market['market'].startswith('KRW')]
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Oops: Something Else: {err}")
    return []


# 최근 10분 동안의 캔들 데이터 가져오기 (거래금액으로 평가)
def get_recent_10_min_data(market):
    url = f"https://api.upbit.com/v1/candles/minutes/1"
    params = {
        'market': market,
        'count': 2  # 1분 단위로 2개의 데이터를 가져옴
    }

    while True:
        try:
            response = requests.get(url, params=params)
            if response.status_code == 429:
                print(f"Rate limit exceeded for {market}. Retrying after a short delay...")
                sleep(1)  # 1초 대기 후 다시 시도
                continue
            response.raise_for_status()  # HTTP 에러 발생 시 예외 처리
            return response.json()
        except requests.exceptions.HTTPError as errh:
            print(f"HTTP Error: {errh}")
            break
        except requests.exceptions.ConnectionError as errc:
            print(f"Error Connecting: {errc}")
            break
        except requests.exceptions.Timeout as errt:
            print(f"Timeout Error: {errt}")
            break
        except requests.exceptions.RequestException as err:
            print(f"Oops: Something Else: {err}")
            break
    return []


# 거래금액이 가장 많은 3개의 종목 찾기 (병렬 처리)
def get_top_3_highest_trade_price():
    markets = get_market_codes()
    if not markets:
        print("No market data retrieved.")
        return None

    trade_price_data = []

    # 병렬 처리로 각 마켓의 데이터를 가져옴
    with ThreadPoolExecutor(max_workers=10) as executor:
        # 각 시장에 대해 API 요청을 병렬로 실행
        future_to_market = {executor.submit(get_recent_10_min_data, market): market for market in markets}

        for future in as_completed(future_to_market):
            market = future_to_market[future]
            try:
                candle_data = future.result()
                if not candle_data:
                    continue

                # 10분간의 거래금액 (candle_acc_trade_price)을 합산
                total_trade_price = sum([candle['candle_acc_trade_price'] for candle in candle_data])
                trade_price_data.append({
                    'market': market,
                    'total_trade_price': total_trade_price
                })
            except Exception as exc:
                print(f"Market {market} generated an exception: {exc}")

    # 거래금액 순으로 정렬하여 상위 3개 종목 추출
    if not trade_price_data:  # 데이터가 없는 경우 처리
        print("No trade price data found.")
        return None

    df = pd.DataFrame(trade_price_data)
    top_3 = df.nlargest(3, 'total_trade_price')

    return top_3


# 결과 출력
top_3_markets = get_top_3_highest_trade_price()
if top_3_markets is not None:
    print(top_3_markets)
