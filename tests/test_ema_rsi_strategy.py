from datetime import datetime

from atlas.domain.feature_set import FeatureSet
from atlas.domain.signal import SignalType
from atlas.strategies.trend.ema_rsi_strategy import EmaRsiTrendStrategy


def test_ema_rsi_strategy_generates_buy_signal():
    feature_set = FeatureSet(
        symbol="EURUSD",
        timeframe="1m",
        timestamp=datetime.now(),
        features={
            "ema_20": 105,
            "ema_50": 100,
            "rsi_14": 60,
        },
    )

    strategy = EmaRsiTrendStrategy()
    signal = strategy.generate(feature_set)

    assert signal.signal_type == SignalType.BUY


def test_ema_rsi_strategy_generates_sell_signal():
    feature_set = FeatureSet(
        symbol="EURUSD",
        timeframe="1m",
        timestamp=datetime.now(),
        features={
            "ema_20": 95,
            "ema_50": 100,
            "rsi_14": 40,
        },
    )

    strategy = EmaRsiTrendStrategy()
    signal = strategy.generate(feature_set)

    assert signal.signal_type == SignalType.SELL


def test_ema_rsi_strategy_generates_hold_signal():
    feature_set = FeatureSet(
        symbol="EURUSD",
        timeframe="1m",
        timestamp=datetime.now(),
        features={
            "ema_20": 101,
            "ema_50": 100,
            "rsi_14": 50,
        },
    )

    strategy = EmaRsiTrendStrategy()
    signal = strategy.generate(feature_set)

    assert signal.signal_type == SignalType.HOLD