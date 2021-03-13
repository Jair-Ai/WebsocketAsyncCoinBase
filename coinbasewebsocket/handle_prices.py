from typing import List
from collections import deque


class handle_prices():

    def __init__(self, assets: List[str], window: int = 200):
        self._assets = assets
        self.data = {asset: deque(maxlen=200) for asset in assets}

    def vwap(self):
        ...

    def organize_data(self, new_data):
        check_data = {}

    def check_data(self, message):
        self.data[message['product_id']].append(message['price'])


