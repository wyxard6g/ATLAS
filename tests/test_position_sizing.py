import pytest

from atlas.risk.position_sizing import PositionSizingEngine


def test_position_sizing_calculates_quantity():
    engine = PositionSizingEngine(risk_per_trade=0.01)

    quantity = engine.calculate_size(
        account_equity=100_000,
        entry_price=100,
        stop_loss_price=95,
    )

    assert quantity == 200


def test_position_sizing_rejects_invalid_risk():
    with pytest.raises(ValueError):
        PositionSizingEngine(risk_per_trade=0)


def test_position_sizing_rejects_zero_stop_distance():
    engine = PositionSizingEngine(risk_per_trade=0.01)

    with pytest.raises(ValueError):
        engine.calculate_size(
            account_equity=100_000,
            entry_price=100,
            stop_loss_price=100,
        )