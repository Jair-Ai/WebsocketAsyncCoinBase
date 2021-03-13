from datetime import time

import websocket


class Client:

    def __init__(self, production=False, ticker=[], level2=[], user=[], ohlc=[], credentials=None):
        self.url = 'wss://ws-feed-public.sandbox.pro.coinbase.com'
        self.production = production

        self._ticker = ticker
        self._level2 = level2
        self._user = user
        self._ohlc = ohlc
        self._credentials = credentials

        self.updated_time = time.time() + 30

        if self.production:
            self.url = 'wss://ws-feed.pro.coinbase.com'
        self._subscription = self.subscription(self._ticker, self._level2, self._user, self._credentials)
        self.data = self.set_data(self._subscription, self._ohlc, self.production)
        self.messages = []
        self.ws = None
        self.conn_thread = None
        self.terminated = False
        self.error_count = 0
        self.max_errors_allowed = 1000

        self.PRODUCTS = ['BTC-USD', 'LTC-USD', 'ETH-USD', 'ETC-USD', 'LTC-BTC', 'ETH-BTC', 'ETC-BTC', 'BCH-USD',
                         'BCH-BTC', 'ZRX-USD', 'ZRX-BTC']
        self.accepted_message_type = ["error", "ticker", "snapshot", "l2update", "received", "open", "done", "match",
                                      "change", "activate"]
