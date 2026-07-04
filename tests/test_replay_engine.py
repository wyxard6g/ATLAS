from datetime import datetime, timedelta

import pytest

from atlas.backtesting.replay import ReplayEngine
from atlas.domain.candle import Candle


def test_replay_engine_iterates_all_candles():
    now = datetime.now()

    candles = [
        Candle(now, 100, 105, 95, 101, 1000),
        Candle(now + timedelta(minutes=1), 101, 106, 100, 103, 1100),
        Candle(now + timedelta(minutes=2), 103, 107, 102, 104, 1200),
    ]

    replay = ReplayEngine(candles)

    replayed = list(replay)

    assert len(replayed) == 3
    assert replayed[0].close == 101
    assert replayed[-1].close == 104


def test_replay_engine_rejects_empty_input():
    with pytest.raises(ValueError):
        ReplayEngine([])