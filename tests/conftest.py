import asyncio
from pytest import fixture
from config import settings


@fixture(scope='function')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@fixture(scope='function')
def send_async_message():
    assets = settings.ASSETS
    wellcome_message = ''
