import pytest
from datetime import datetime

from atlas.domain.order import Order, OrderSide, OrderType


def test_market_order_creation():
    order = Order(
        symbol="EURUSD",
        side=OrderSide.BUY,
        order_type=OrderType.MARKET,
        quantity=1000,
        timestamp=datetime.now(),
    )

    assert order.side == OrderSide.BUY
    assert order.quantity == 1000


def test_invalid_quantity():
    with pytest.raises(ValueError):
        Order(
            symbol="EURUSD",
            side=OrderSide.BUY,
            order_type=OrderType.MARKET,
            quantity=0,
            timestamp=datetime.now(),
        )


def test_limit_order_requires_limit_price():
    with pytest.raises(ValueError):
        Order(
            symbol="EURUSD",
            side=OrderSide.BUY,
            order_type=OrderType.LIMIT,
            quantity=1000,
            timestamp=datetime.now(),
        )


def test_stop_order_requires_stop_price():
    with pytest.raises(ValueError):
        Order(
            symbol="EURUSD",
            side=OrderSide.SELL,
            order_type=OrderType.STOP,
            quantity=1000,
            timestamp=datetime.now(),
        )