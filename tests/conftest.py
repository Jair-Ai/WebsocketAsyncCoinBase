import asyncio
from pytest import fixture


@fixture(scope='function')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()
