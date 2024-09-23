import requests
import time
import matplotlib.pyplot as plt
from collections import deque
import matplotlib.font_manager as fm

# 한글 폰트를 '굴림'으로 설정하는 함수
def set_korean_font():
    plt.rc('font', family='Gulim')  # 굴림체를 설정


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


# 총 매도호가와 총 매수호가를 계산하는 함수
def calculate_order_totals(orderbook):
    total_ask = sum([order['ask_size'] for order in orderbook['orderbook_units']])
    total_bid = sum([order['bid_size'] for order in orderbook['orderbook_units']])
    return total_ask, total_bid


# 실시간으로 "총매도호가 - 총매수호가" 값을 그래프로 표시하는 함수
def plot_real_time_diff():
    # 데이터를 저장할 덱(Deque) 생성
    diff_history = deque(maxlen=50)  # 최근 50개의 데이터만 저장

    plt.ion()  # 인터랙티브 모드 켜기
    fig, ax = plt.subplots()

    set_korean_font()  # 한글 폰트 설정

    while True:
        orderbook = get_orderbook("KRW-BTC")
        if orderbook:
            total_ask, total_bid = calculate_order_totals(orderbook)
            diff = total_ask - total_bid  # 총매도호가 - 총매수호가
            diff_history.append(diff)

            # 그래프 업데이트
            ax.clear()
            ax.plot(diff_history, label='총매도호가 - 총매수호가')
            ax.set_xlabel('시간')
            ax.set_ylabel('호가 차이')
            ax.set_title('총매도호가 - 총매수호가 실시간 그래프')
            ax.legend()

            plt.pause(1)  # 1초 대기 후 업데이트


if __name__ == "__main__":
    plot_real_time_diff()
