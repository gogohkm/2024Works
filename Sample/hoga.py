# 총 매수호가와 총 매도호가를 표시

import asyncio
import websockets
import json


async def get_total_bid_ask(ticker):
    uri = "wss://api.upbit.com/websocket/v1"

    # 구독 데이터 작성 (orderbook 구독)
    subscribe_data = [
        {"ticket": "test"},
        {
            "type": "orderbook",
            "codes": [f"KRW-{ticker}"],  # KRW 마켓의 특정 티커 입력
            "isOnlyRealtime": True
        }
    ]

    async with websockets.connect(uri) as websocket:
        # 구독 메시지 전송
        await websocket.send(json.dumps(subscribe_data))

        while True:
            # 서버로부터 메시지 수신
            response = await websocket.recv()
            data = json.loads(response)

            # 주문서 데이터 추출
            if data['type'] == 'orderbook':
                orderbook_units = data.get('orderbook_units', [])

                # 매수 호가와 매도 호가 계산
                total_bid_volume = sum([unit['bid_size'] for unit in orderbook_units])  # 총 매수 잔량
                total_ask_volume = sum([unit['ask_size'] for unit in orderbook_units])  # 총 매도 잔량

                print(f"총 매수 호가: {total_bid_volume}, 총 매도 호가: {total_ask_volume}")

            await asyncio.sleep(1)  # 1초 간격으로 수신


# 실행 코드
ticker = "BTC"  # 원하는 코인 티커를 입력하세요 (예: BTC, ETH)
asyncio.run(get_total_bid_ask(ticker))
