import pytest
from datetime import datetime

from atlas.domain.tick import Tick


def test_tick_creation():
    tick = Tick(
        symbol="EURUSD",
        price=1.2345,
        volume=100,
        timestamp=datetime.now(),
    )

    assert tick.price == 1.2345


def test_invalid_price():
    with pytest.raises(ValueError):
        Tick(
            symbol="EURUSD",
            price=0,
            volume=100,
            timestamp=datetime.now(),
        )


def test_negative_volume():
    with pytest.raises(ValueError):
        Tick(
            symbol="EURUSD",
            price=1.2,
            volume=-10,
            timestamp=datetime.now(),
        )