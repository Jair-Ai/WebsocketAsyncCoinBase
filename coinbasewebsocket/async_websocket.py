import asyncio
import json
import websockets
from typing import Dict, List, Union, Callable, Any

from log_manager import logger
from handle_prices import PricesHandler
from config import settings
uri = 'wss://ws-feed-public.sandbox.pro.coinbase.com'


async def consumer_handler(websocket: websockets.WebSocketClientProtocol, func: Callable):
    async for message in websocket:
        check_message_from_broker(json.loads(message), func)


async def consume(uri_server: str, subscribe_message: Dict[str, List[str, Dict[str, Union[str, List[str]]]]], func: Callable):
    try:
        async with websockets.connect(uri_server) as websocket:
            await websocket.send(message=json.dumps(subscribe_message))
            while True:
                message_str = await asyncio.wait_for(websocket.recv(), WAIT_TIMEOUT)
                await consumer_handler(websocket, func)
    except websockets.WebSocketProtocolError as refused:
        logger.error(refused)
    except websockets.ConnectionClosed as con_err:
        logger.error(con_err)
    except Exception as e:
        logger.error(f"Oops{e.__class__} occurred.")
        raise


def check_message_from_broker(message: Dict[str, str], func: Callable) -> None:
    if message['type'] != 'ticker':
        logger.info(message)
    else:
        func(message)


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
    prices_handler = PricesHandler()
    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(consume())]
    loop.run_until_complete(consume(uri=uri))
    loop.run_forever()
