import asyncio
import json
import logging
import traceback

import websockets
from typing import Dict

from log_manager import logger

uri = 'wss://ws-feed-public.sandbox.pro.coinbase.com'

subscribe_message = {
    "type": "subscribe",
    "product_ids": [
        "BTC-USD",
        "ETH-USD",
        "ETH-BTC"
    ],
    "channels": [
        "match",
        {
            "name": "ticker",
            "product_ids": [
                "BTC-USD",
                "ETH-USD",
                "ETH-BTC"
            ]
        }
    ]
}


async def consumer_handler(websocket: websockets.WebSocketClientProtocol):
    async for message in websocket:
        log_message(json.loads(message))


async def consume(uri: str):
    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(message=json.dumps(subscribe_message))
            await consumer_handler(websocket)
    except ConnectionRefusedError as refused:
        logger.error(refused)
    except ConnectionError as con_err:
        logger.error(con_err)
    except Exception as e:
        logger.error(f"Oops{e.__class__} occurred.")
        raise

def log_message(message: Dict[str, str]) -> None:
    if message['type'] != 'ticker':
        logger.info(message)
    else:
        logger.error(message)


def vwap_calculation():
    ...


def disconnect():
    ...


def on_close():
    ...


def on_open():
    ...


def on_error():
    ...


def on_message():
    ...


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume(uri=uri))
    loop.run_forever()
