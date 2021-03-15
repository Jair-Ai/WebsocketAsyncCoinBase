import asyncio
import os
import json
import websockets
from typing import Dict, List, Union, Callable, Any

from log_manager import logger
from handle_prices import PricesHandler
from config import settings

MESSAGE_FOR_COINBASE = Dict[str, Union[str, List[str], List[Union[str, Dict[str, Union[str, List[str]]]]]]]


def build_message():
    init_message = {
        "type":
            settings.TYPE,
        "channels": [
            settings.CHANNEL, {
                "name": "ticker",
                "product_ids": settings.ASSETS.to_list()
            }
        ]
    }

    return init_message


def check_message_from_broker(message: Dict[str, str], func: Callable) -> None:
    if message['type'] != 'ticker':
        logger.info(message)
    else:
        func(message)


async def consumer_handler(websocket: websockets.WebSocketClientProtocol,
                           func: Callable) -> None:
    async for message in websocket:
        check_message_from_broker(json.loads(message), func)


async def async_websocket_connect(
        uri_server: str,
        subscribe_message: MESSAGE_FOR_COINBASE):
    prices_handler = PricesHandler(settings.ASSETS)
    try:
        async with websockets.connect(uri_server) as websocket:
            await websocket.send(json.dumps(subscribe_message))
            await consumer_handler(websocket, prices_handler.check_data)
    except websockets.WebSocketProtocolError as conn_refused:
        logger.error(f'Connection refused reason: {conn_refused.reason}')
    except websockets.ConnectionClosed as conn_close:
        logger.error(f"Connection Closed reason: {conn_close.reason}.")
    except Exception as e:
        logger.error(f"Oops{e.__class__} occurred.")
        raise

loop = asyncio.get_event_loop()
message_to_coinbase = build_message()
loop.run_until_complete(
    asyncio.ensure_future(
        async_websocket_connect(uri_server=settings.URI,
                                subscribe_message=build_message())))
loop.run_forever()
