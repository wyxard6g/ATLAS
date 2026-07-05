import pytest

from atlas.backtesting.slippage import SlippageModel


def test_buy_slippage():
    model = SlippageModel(0.05)

    assert model.buy_price(100) == 100.05


def test_sell_slippage():
    model = SlippageModel(0.05)

    assert model.sell_price(100) == 99.95


def test_negative_slippage():
    with pytest.raises(ValueError):
        SlippageModel(-1)


def test_invalid_execution_price():
    model = SlippageModel(0.05)

    with pytest.raises(ValueError):
        model.buy_price(0)