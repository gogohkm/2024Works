# 특정종목에 대해 거래량을 구하고 이를 출력하는 코드

import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


# 업비트 API URL 설정 (종목별 시세 정보 - 최근 거래량)
def get_market_ticker(market="KRW-BTC"):
    url = f"https://api.upbit.com/v1/candles/minutes/1?market={market}&count=200"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code}")
        return None


# 거래량 변동 계산 및 그래프 그리기
def calculate_and_plot_volume_change(market="KRW-BTC"):
    data = get_market_ticker(market)

    if data:
        # 최근 200분 간의 거래량 데이터
        volumes = [item['candle_acc_trade_volume'] for item in data]
        times = [item['candle_date_time_kst'] for item in data]

        # DataFrame으로 변환
        df = pd.DataFrame({
            'time': times,
            'volume': volumes
        })

        # 거래량 변동 계산 (이전 거래량 대비 변화율)
        df['volume_change'] = df['volume'].pct_change() * 100  # 퍼센트 변동
        df['time'] = pd.to_datetime(df['time'])

        # DataFrame 출력
        print(df.head())

        # 거래량 변동 그래프 그리기
        plt.figure(figsize=(10, 6))
        plt.plot(df['time'], df['volume_change'], label='Volume Change (%)', color='b')
        plt.xlabel('Time')
        plt.ylabel('Volume Change (%)')
        plt.title(f'{market} Volume Change Over Time')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()

        return df
    else:
        print("No data returned")


# 실행
df = calculate_and_plot_volume_change("KRW-BTC")  # 비트코인(KRW-BTC) 종목의 거래량 변동 및 그래프
