import pytest
from datetime import datetime

from atlas.domain.feature_set import FeatureSet


def test_feature_set_creation():
    feature_set = FeatureSet(
        symbol="EURUSD",
        timeframe="1m",
        timestamp=datetime.now(),
        features={"sma_3": 102},
    )

    assert feature_set.symbol == "EURUSD"
    assert feature_set.get("sma_3") == 102
    assert feature_set.count == 1


def test_feature_set_rejects_empty_features():
    with pytest.raises(ValueError):
        FeatureSet(
            symbol="EURUSD",
            timeframe="1m",
            timestamp=datetime.now(),
            features={},
        )