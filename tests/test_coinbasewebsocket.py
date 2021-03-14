from coinbasewebsocket import __version__
import pytest

def test_version():
    assert __version__ == '0.1.0'

def test_vwap(event_loop):



