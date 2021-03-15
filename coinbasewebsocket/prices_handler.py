from datetime import datetime as dt
from typing import List, Dict
from collections import deque
import numpy as np

from coinbasewebsocket.log_manager import logger


class PricesHandler:

    def __init__(self, assets: List[str], window: int = 200):
        self._assets = assets
        self.price = {asset: deque(maxlen=window) for asset in assets}
        self.volume = {asset: deque(maxlen=window) for asset in assets}
        self.vwap = {asset: deque(maxlen=window) for asset in assets}

    def vwap_calculation(self, asset: str) -> float:
        numpy_volume = np.array(self.volume[asset])
        return ((np.multiply(self.price[asset],
                             numpy_volume).cumsum()) / numpy_volume.cumsum())[-1]

    def check_data(self, message: Dict[str, str]) -> None:
        # TODO: Before that check if the trade id is not the same as the last one.
        try:
            self.price[message['product_id']].append(float(message['price']))
            self.volume[message['product_id']].append(
                float(message['last_size']))

            self.vwap[message['product_id']].append(self.vwap_calculation(message['product_id']))
        except ValueError as e:
            logger.warning(
                f"Error on insert {message['product_id']} prices, ERROR -> {e.__class__}"
            )
        else:
            logger.info(
                f"Vwap {message['product_id']} - {self.vwap[message['product_id']][-1]}")
