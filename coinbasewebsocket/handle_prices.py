from datetime import datetime as dt
from typing import List, Dict
from collections import deque
import numpy as np

from log_manager import logger

class PricesHandler:

    def __init__(self, assets: List[str], window: int = 200):
        self._assets = assets
        self.price = {asset: deque(maxlen=200) for asset in assets}
        self.volume = {asset: deque(maxlen=200) for asset in assets}
        self.vwap = {asset: deque(maxlen=200) for asset in assets}

    def vwap_calculation(self) -> np.array:
        numpy_volume = np.array(self.vwap)
        return ((np.array(self.price)*numpy_volume).cumsum()/numpy_volume.cumsum())[-1]

    def check_data(self, message: Dict[str, str]):
        try:
            self.price[message['product_id']].append(float(message['price']))
            self.volume[message['product_id']].append(float(message['price']))
            self.vwap[message['vwap']].append(self.vwap_calculation)
        except TypeError as e:
            logger.warning(f"{dt.now()} - Error on insert {message['product_id']} prices, check connection or restart")
        else:
            logger.info(f"{dt.now()} Vwap {message['product_id']} - {self.vwap[-1]}")





