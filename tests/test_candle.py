import pytest
from datetime import datetime

from atlas.domain.candle import Candle


def test_invalid_high_low():
    with pytest.raises(ValueError):
        Candle(
            timestamp=datetime.now(),
            open=100,
            high=90,
            low=95,
            close=92,
            volume=1000,
        )


def test_negative_volume():
    with pytest.raises(ValueError):
        Candle(
            timestamp=datetime.now(),
            open=100,
            high=105,
            low=95,
            close=102,
            volume=-1,
        )