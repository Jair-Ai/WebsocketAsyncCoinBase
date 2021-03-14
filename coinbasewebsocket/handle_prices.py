from datetime import datetime as dt
from typing import List, Dict
from collections import deque
import numpy as np

from log_manager import logger

mess_coin = {
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


class PricesHandler:

    def __init__(self, assets: List[str], window: int = 200):
        self._assets = assets
        self.price = {asset: deque(maxlen=window) for asset in assets}
        self.volume = {asset: deque(maxlen=window) for asset in assets}
        self.vwap = {asset: deque(maxlen=window) for asset in assets}

    def vwap_calculation(self) -> np.array:
        numpy_volume = np.array(self.vwap)
        return np.multiply(self.price,
                           numpy_volume).cumsum() / numpy_volume.cumsum()[-1]

    def check_data(self, message: Dict[str, str]):
        try:
            self.price[message['product_id']].append(float(message['price']))
            self.volume[message['product_id']].append(float(message['price']))
            self.vwap[message['product_id']].append(self.vwap_calculation)
        except TypeError as e:
            logger.warning(
                f"{dt.now()} - Error on insert {message['product_id']} prices, ERROR->{e.__class__}"
            )
        else:
            logger.info(
                f"{dt.now()} Vwap {message['product_id']} - {self.vwap[-1]}")
