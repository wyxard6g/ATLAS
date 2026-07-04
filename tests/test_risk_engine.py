from datetime import datetime

import pytest

from atlas.domain.signal import Signal, SignalType
from atlas.risk.engine import RiskEngine
from atlas.risk.models.minimum_confidence import MinimumConfidenceRiskModel
from atlas.risk.registry import RiskRegistry


def test_minimum_confidence_model_approves_high_confidence_signal():
    signal = Signal(
        symbol="EURUSD",
        signal_type=SignalType.BUY,
        confidence=0.75,
        timeframe="1m",
        strategy="test_strategy",
        timestamp=datetime.now(),
        reason="Test signal",
    )

    model = MinimumConfidenceRiskModel(minimum_confidence=0.60)

    assert model.approve(signal) is True


def test_minimum_confidence_model_rejects_low_confidence_signal():
    signal = Signal(
        symbol="EURUSD",
        signal_type=SignalType.BUY,
        confidence=0.50,
        timeframe="1m",
        strategy="test_strategy",
        timestamp=datetime.now(),
        reason="Test signal",
    )

    model = MinimumConfidenceRiskModel(minimum_confidence=0.60)

    assert model.approve(signal) is False


def test_minimum_confidence_model_rejects_invalid_threshold():
    with pytest.raises(ValueError):
        MinimumConfidenceRiskModel(minimum_confidence=1.5)


def test_risk_engine_evaluates_registered_model():
    signal = Signal(
        symbol="EURUSD",
        signal_type=SignalType.BUY,
        confidence=0.75,
        timeframe="1m",
        strategy="test_strategy",
        timestamp=datetime.now(),
        reason="Test signal",
    )

    registry = RiskRegistry()
    registry.register(MinimumConfidenceRiskModel(minimum_confidence=0.60))

    engine = RiskEngine(registry)

    assert engine.evaluate("minimum_confidence", signal) is True