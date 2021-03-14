import asyncio
import json
import websockets
from typing import Dict, List, Union, Callable, Any

from log_manager import logger
from handle_prices import PricesHandler
from config import settings


def build_message():
    return {
        "type": settings.TYPE,
        "product_ids": [
            settings.ASSETS
        ],
        "channels": [
            settings.CHANNELS,
            {
                "name": "ticker",
                "product_ids": [
                    settings.ASSETS
                ]
            }
        ]
    }


async def consumer_handler(websocket: websockets.WebSocketClientProtocol, func: Callable):
    async for message in websocket:
        check_message_from_broker(json.loads(message), func)


async def async_websocket_connect(uri_server: str,
                                  subscribe_message: Dict[str, List[str, Dict[str, Union[str, List[str]]]]],
                                  func: Callable):
    try:
        async with websockets.connect(uri_server) as websocket:
            await websocket.send(message=json.dumps(subscribe_message))
            while True:
                message_str = await asyncio.wait_for(websocket.recv(), settings.WAIT_TIMEOUT)
                await consumer_handler(websocket, func)
    except websockets.WebSocketProtocolError as refused:
        logger.error(refused)
    except websockets.ConnectionClosed as conn_close:
        logger.error(f"Connection Closed reason: {conn_close.reason}.")
    except Exception as e:
        logger.error(f"Oops{e.__class__} occurred.")
        raise


def check_message_from_broker(message: Dict[str, str], func: Callable) -> None:
    if message['type'] != 'ticker':
        logger.info(message)
    else:
        func(message)


prices_handler = PricesHandler(settings.ASSETS)
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.ensure_future(async_websocket_connect(uri_server=settings.URI, subscribe_message=build_message())))
loop.run_forever()
