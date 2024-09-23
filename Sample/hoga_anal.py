# 업비트에서 매도누적수량- 매수누적수량을 계산하고 3차 다항식으로 근사하는 예제

import requests
import time
import matplotlib.pyplot as plt
import numpy as np
from collections import deque
import matplotlib.font_manager as fm


# 한글 폰트를 '굴림'으로 설정하는 함수
def set_korean_font():
    plt.rc('font', family='Gulim')  # 굴림체 설정


# 업비트 API에서 호가 정보를 가져오는 함수
def get_orderbook(market="KRW-BTC"):
    url = f"https://api.upbit.com/v1/orderbook?markets={market}"
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()[0]
    else:
        print("API 호출 오류:", response.status_code)
        return None


# 매도 누적수량과 매수 누적수량을 계산하는 함수
def calculate_accumulated_order_totals(orderbook):
    # 매도 누적수량 = 모든 매도 호가의 수량 합계
    total_ask_size = sum([order['ask_size'] for order in orderbook['orderbook_units']])

    # 매수 누적수량 = 모든 매수 호가의 수량 합계
    total_bid_size = sum([order['bid_size'] for order in orderbook['orderbook_units']])

    return total_ask_size, total_bid_size


# 3차 다항식을 사용하여 근사하는 함수
def fit_cubic_polynomial(x, y):
    # x 값과 y 값으로 3차 다항식의 계수를 계산
    coefficients = np.polyfit(x, y, 3)
    # 계산된 계수로부터 3차 다항식을 생성
    cubic_polynomial = np.poly1d(coefficients)
    return cubic_polynomial


# 실시간으로 "매도 누적수량 - 매수 누적수량" 값을 그래프로 표시하고, 3차 근사함수를 추가하는 함수
def plot_real_time_diff():
    # 데이터를 저장할 덱(Deque) 생성
    diff_history = deque(maxlen=50)  # 최근 50개의 데이터만 저장
    time_history = deque(maxlen=50)  # x 축의 시간 데이터 저장

    plt.ion()  # 인터랙티브 모드 켜기
    fig, ax = plt.subplots()

    set_korean_font()  # 굴림체 설정

    time_counter = 0  # 시간 카운터 (x 축 값)

    while True:
        orderbook = get_orderbook("KRW-BTC")
        if orderbook:
            total_ask_size, total_bid_size = calculate_accumulated_order_totals(orderbook)
            diff = total_ask_size - total_bid_size  # 매도 누적수량 - 매수 누적수량
            diff_history.append(diff)
            time_history.append(time_counter)

            # 그래프 업데이트
            ax.clear()
            ax.plot(time_history, diff_history, label='매도 누적수량 - 매수 누적수량', color='blue')

            # 데이터가 최소 4개 이상일 때 3차 함수 근사
            if len(time_history) >= 4:
                cubic_polynomial = fit_cubic_polynomial(list(time_history), list(diff_history))
                fitted_values = cubic_polynomial(time_history)

                # 3차 함수 그래프 추가
                ax.plot(time_history, fitted_values, label='3차 함수 근사', color='red', linestyle='--')

            ax.set_xlabel('시간')
            ax.set_ylabel('수량 차이')
            ax.set_title('매도 누적수량 - 매수 누적수량 실시간 그래프')
            ax.legend()

            plt.pause(1)  # 1초 대기 후 업데이트
            time_counter += 1  # 시간 업데이트


if __name__ == "__main__":
    plot_real_time_diff()
