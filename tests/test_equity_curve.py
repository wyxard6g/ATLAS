from datetime import datetime

import pytest

from atlas.backtesting.equity_curve import EquityCurve


def test_equity_curve_adds_point():
    curve = EquityCurve()

    curve.add(
        timestamp=datetime.now(),
        equity=100_000,
    )

    assert curve.count == 1
    assert curve.latest_equity == 100_000


def test_equity_curve_rejects_negative_equity():
    curve = EquityCurve()

    with pytest.raises(ValueError):
        curve.add(
            timestamp=datetime.now(),
            equity=-1,
        )


def test_equity_curve_rejects_latest_when_empty():
    curve = EquityCurve()

    with pytest.raises(ValueError):
        _ = curve.latest_equity