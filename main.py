import websocket
import json
import matplotlib.pyplot as plt
import numpy as np

# 호가 데이터를 실시간으로 저장할 변수
bids = []
asks = []


# 웹소켓 메시지 핸들러 함수
def on_message(ws, message):
    global bids, asks

    data = json.loads(message)
    orderbook_units = data['orderbook_units']

    # 총 매수호가량 및 총 매도호가량 계산
    total_bid_size = sum([unit['bid_size'] for unit in orderbook_units])
    total_ask_size = sum([unit['ask_size'] for unit in orderbook_units])

    bids.append(total_bid_size)
    asks.append(total_ask_size)

    # 실시간 업데이트를 위해 그래프를 다시 그립니다.
    plt.clf()
    plt.plot(bids[-50:], label='Total Bid Size', color='blue')
    plt.plot(asks[-50:], label='Total Ask Size', color='red')
    plt.xlabel('Time')
    plt.ylabel('Size')
    plt.title('Upbit BTC/KRW Order Book')
    plt.legend()
    plt.pause(0.1)


# 웹소켓 연결 핸들러 함수
def on_open(ws):
    payload = [
        {
            "ticket": "test",
        },
        {
            "type": "orderbook",
            "codes": ["KRW-BTC"]
        }
    ]
    ws.send(json.dumps(payload))


# 웹소켓 에러 핸들러 함수
def on_error(ws, error):
    print(f"Error: {error}")


# 웹소켓 종료 핸들러 함수
def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed")


# 웹소켓 연결 시작 함수
def start_websocket():
    websocket_url = "wss://api.upbit.com/websocket/v1"
    ws = websocket.WebSocketApp(websocket_url, on_message=on_message, on_open=on_open, on_error=on_error,
                                on_close=on_close)
    ws.run_forever()


# matplotlib 인터랙티브 모드 설정
plt.ion()

# 웹소켓 연결 시작
if __name__ == "__main__":
    start_websocket()
