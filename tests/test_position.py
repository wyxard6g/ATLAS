import pytest

from atlas.domain.position import Position


def test_position_creation():
    position = Position(
        symbol="EURUSD",
        quantity=1000,
        average_price=1.1050,
        unrealized_pnl=25.0,
    )

    assert position.symbol == "EURUSD"
    assert position.quantity == 1000


def test_zero_quantity_invalid():
    with pytest.raises(ValueError):
        Position(
            symbol="EURUSD",
            quantity=0,
            average_price=1.1050,
        )


def test_invalid_average_price():
    with pytest.raises(ValueError):
        Position(
            symbol="EURUSD",
            quantity=1000,
            average_price=0,
        )