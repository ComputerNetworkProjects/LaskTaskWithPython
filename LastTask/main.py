import asyncio
import websockets
import json

async def receive_binance_data():
    uri = "wss://stream.binance.com:9443/ws/btcusdt@depth5/btcusdt@trade"
    async with websockets.connect(uri) as websocket:
        with open("streamdata-multi.txt", "a") as file:
            while True:
                data = await websocket.recv()
                json_data = json.loads(data)

                orderbook_data = json_data.get("bids") or json_data.get("asks") or json_data.get("p")
                if orderbook_data:
                    file.write(f'btcusdt@{json_data.get("e")},{json.dumps(orderbook_data)}\n')
                else:
                    file.write(f'btcusdt@trade,{json.dumps(json_data)}\n')

async def receive_upbit_data():
    uri = "wss://api.upbit.com/websocket/v1"
    async with websockets.connect(uri) as websocket:
        request_data = [
            {"ticket": "UNIQUE_TICKET"},
            {"type": "orderbook", "codes": ["KRW-BTC"]}
        ]
        await websocket.send(json.dumps(request_data))

        with open("streamdata-multi.txt", "a") as file:
            while True:
                data = await websocket.recv()
                json_data = json.loads(data)

                # 'orderbook_units' 데이터만 추출
                orderbook_units = json_data.get("orderbook_units", [])
                file.write(f'btckrw@orderbook,{json.dumps(orderbook_units)}\n')

async def main():
    # 두 개의 비동기 작업을 동시에 실행
    await asyncio.gather(
        receive_binance_data(),
        receive_upbit_data()
    )

# 프로그램 실행
asyncio.run(main())