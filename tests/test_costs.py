import pytest

from atlas.backtesting.costs import CommissionModel


def test_commission_model_calculates_commission():
    model = CommissionModel(rate=0.001)

    assert model.calculate(10_000) == 10


def test_commission_model_rejects_negative_rate():
    with pytest.raises(ValueError):
        CommissionModel(rate=-0.01)


def test_commission_model_rejects_negative_trade_value():
    model = CommissionModel(rate=0.001)

    with pytest.raises(ValueError):
        model.calculate(-100)