from coinbasewebsocket import __version__
import pytest

from collections import deque
from coinbasewebsocket.handle_prices import PricesHandler
from config import settings
import numpy as np


def test_version():
    assert __version__ == '0.1.0'


def test_prices_handler_create_deque():
    prices_handler = PricesHandler(settings.ASSETS.to_list())

    assert isinstance(prices_handler.price, deque)
    assert isinstance(prices_handler.volume, deque)
    assert isinstance(prices_handler.vwap, deque)


def test_check_data():
    prices_handler = PricesHandler(settings.ASSETS.to_list())

    price_range = np.random.default_rng().uniform(0.03, 0.04, 205)
    volume_range = np.random.default_rng().uniform(0.01, 0.5, 205)

    range_trade = [{'type': 'ticker', 'sequence': 18829080, 'product_id': 'ETH-BTC', 'price': str(price_range[tick]),
                    'open_24h': '0.03141', 'volume_24h': '223.95906816', 'low_24h': '0.03086', 'high_24h': '0.0318',
                    'volume_30d': '546175.37374905', 'best_bid': '0.03117', 'best_ask': '0.03119', 'side': 'buy',
                    'time': '2021-03-14T23:16:25.948518Z', 'trade_id': tick, 'last_size': str(volume_range[tick])} for tick in
                   range(1, 205)]

    for trade_message in range_trade:
        prices_handler.check_data(trade_message)

    # TODO: CHECK TEST FIRST AND LAST ITEM ON EACH DEQUE


def test_check_data_typeerror():
    ...



def test_vwap(event_loop):
    prices_handler = PricesHandler(settings.ASSETS.to_list())

    price_range = np.random.default_rng().uniform(0.03, 0.04, 100)
    volume_range = np.random.default_rng().uniform(0.01, 0.5, 100)


