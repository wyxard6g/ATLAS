import pytest

from atlas.backtesting.spread import SpreadModel


def test_buy_price():
    spread = SpreadModel(0.2)

    assert spread.buy_price(100) == 100.1


def test_sell_price():
    spread = SpreadModel(0.2)

    assert spread.sell_price(100) == 99.9


def test_negative_spread():
    with pytest.raises(ValueError):
        SpreadModel(-1)


def test_invalid_market_price():
    spread = SpreadModel(0.2)

    with pytest.raises(ValueError):
        spread.buy_price(0)