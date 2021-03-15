import logging
from coinbasewebsocket import __version__
import pytest

from collections import deque
from coinbasewebsocket.prices_handler import PricesHandler
from config import settings
import numpy as np

LOGGER = logging.getLogger(__name__)


def test_version():
    assert __version__ == '0.1.0'


def test_prices_handler_create_deque():
    prices_handler = PricesHandler(settings.ASSETS.to_list())

    assert isinstance(prices_handler.price, dict)
    assert isinstance(prices_handler.volume, dict)
    assert isinstance(prices_handler.vwap, dict)


def test_check_data_insert_values():
    prices_handler = PricesHandler(settings.ASSETS.to_list())

    price_range = np.random.default_rng().uniform(0.03, 0.04, 205)
    volume_range = np.random.default_rng().uniform(0.01, 0.5, 205)

    range_trade = [{
        'type': 'ticker',
        'sequence': 18829080,
        'product_id': 'ETH-BTC',
        'price': str(price_range[tick]),
        'open_24h': '0.03141',
        'volume_24h': '223.95906816',
        'low_24h': '0.03086',
        'high_24h': '0.0318',
        'volume_30d': '546175.37374905',
        'best_bid': '0.03117',
        'best_ask': '0.03119',
        'side': 'buy',
        'time': '2021-03-14T23:16:25.948518Z',
        'trade_id': str(tick),
        'last_size': str(volume_range[tick])
    } for tick in range(1, 205)]

    for trade_message in range_trade:
        prices_handler.check_data(trade_message)

    assert prices_handler.price[range_trade[-1]['product_id']][-1] == float(range_trade[-1]['price'])
    assert prices_handler.price[range_trade[-1]['product_id']][0] == float(range_trade[4]['price'])

    assert prices_handler.volume[range_trade[-1]['product_id']][-1] == float(range_trade[-1]['last_size'])
    assert prices_handler.volume[range_trade[-1]['product_id']][0] == float(range_trade[4]['last_size'])


def test_vwap_five_messages(event_loop):
    prices_handler = PricesHandler(settings.ASSETS.to_list())

    price_range = np.random.default_rng().uniform(0.03, 0.04, 205)
    volume_range = np.random.default_rng().uniform(0.01, 0.5, 205)

    range_trade = [{
        'type': 'ticker',
        'sequence': 18829080,
        'product_id': 'ETH-BTC',
        'price': str(price_range[tick]),
        'open_24h': '0.03141',
        'volume_24h': '223.95906816',
        'low_24h': '0.03086',
        'high_24h': '0.0318',
        'volume_30d': '546175.37374905',
        'best_bid': '0.03117',
        'best_ask': '0.03119',
        'side': 'buy',
        'time': '2021-03-14T23:16:25.948518Z',
        'trade_id': str(tick),
        'last_size': str(volume_range[tick])
    } for tick in range(0, 5)]

    for trade_message in range_trade:
        prices_handler.check_data(trade_message)

    vwap_5 = (np.multiply(price_range[:5], volume_range[:5]).cumsum()) / volume_range[:5].cumsum()

    vwap_from_class = np.array(prices_handler.vwap[range_trade[1]['product_id']])

    np.testing.assert_array_equal(vwap_5, np.array(vwap_from_class[:5]))


def test_check_data_type_error(caplog):
    trade_message = {
        'type': 'ticker',
        'sequence': 18829080,
        'product_id': 'ETH-BTC',
        'price': 'bad_data',
        'open_24h': '0.03141',
        'volume_24h': '223.95906816',
        'low_24h': '0.03086',
        'high_24h': '0.0318',
        'volume_30d': '546175.37374905',
        'best_bid': '0.03117',
        'best_ask': '0.03119',
        'side': 'buy',
        'time': '2021-03-14T23:16:25.948518Z',
        'trade_id': '3',
        'last_size': '0.03'}

    prices_handler = PricesHandler(settings.ASSETS.to_list())
    prices_handler.check_data(trade_message)

    assert "Error on insert ETH-BTC prices, ERROR -> <class 'ValueError'>" in caplog.text


def test_check_data_success(caplog):
    trade_message = {
        'type': 'ticker',
        'sequence': 18829080,
        'product_id': 'ETH-BTC',
        'price': '0.03258',
        'open_24h': '0.03141',
        'volume_24h': '223.95906816',
        'low_24h': '0.03086',
        'high_24h': '0.0318',
        'volume_30d': '546175.37374905',
        'best_bid': '0.03117',
        'best_ask': '0.03119',
        'side': 'buy',
        'time': '2021-03-14T23:16:25.948518Z',
        'trade_id': '3',
        'last_size': '0.03'}

    prices_handler = PricesHandler(settings.ASSETS.to_list())
    prices_handler.check_data(trade_message)

    assert f"Vwap {trade_message['product_id']} - {trade_message['price']}" in caplog.text


def test_duplicated_message(caplog):
    prices_handler = PricesHandler(settings.ASSETS.to_list())

    duplicated_message = [{
        'type': 'ticker',
        'sequence': 18829080,
        'product_id': 'ETH-BTC',
        'price': '0.03258',
        'open_24h': '0.03141',
        'volume_24h': '223.95906816',
        'low_24h': '0.03086',
        'high_24h': '0.0318',
        'volume_30d': '546175.37374905',
        'best_bid': '0.03117',
        'best_ask': '0.03119',
        'side': 'buy',
        'time': '2021-03-14T23:16:25.948518Z',
        'trade_id': '3',
        'last_size': '0.03'}, {
        'type': 'ticker',
        'sequence': 18829080,
        'product_id': 'ETH-BTC',
        'price': '0.03258',
        'open_24h': '0.03141',
        'volume_24h': '223.95906816',
        'low_24h': '0.03086',
        'high_24h': '0.0318',
        'volume_30d': '546175.37374905',
        'best_bid': '0.03117',
        'best_ask': '0.03119',
        'side': 'buy',
        'time': '2021-03-14T23:16:25.948518Z',
        'trade_id': '3',
        'last_size': '0.03'}]

    new_message = {
        'type': 'ticker',
        'sequence': 18829080,
        'product_id': 'ETH-BTC',
        'price': '0.03258',
        'open_24h': '0.03141',
        'volume_24h': '223.95906816',
        'low_24h': '0.03086',
        'high_24h': '0.0318',
        'volume_30d': '546175.37374905',
        'best_bid': '0.03117',
        'best_ask': '0.03119',
        'side': 'buy',
        'time': '2021-03-14T23:16:25.948518Z',
        'trade_id': '4',
        'last_size': '0.03'}

    # adding first message

    prices_handler.check_data(duplicated_message[0])

    # adding duplicated message

    prices_handler.check_data(duplicated_message[1])

    # adding new message

    prices_handler.check_data(new_message)

    assert len(prices_handler.price[new_message['product_id']]) == 2

    assert f"Got duplicated message on {duplicated_message[1]['product_id']}, trade_id = {duplicated_message[1]['trade_id']}" in caplog.text
