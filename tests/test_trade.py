import pytest
from datetime import datetime

from atlas.domain.trade import Trade, TradeSide


def test_trade_creation():
    trade = Trade(
        symbol="EURUSD",
        side=TradeSide.BUY,
        quantity=1000,
        price=1.1050,
        timestamp=datetime.now(),
        order_id="ORD-001",
    )

    assert trade.symbol == "EURUSD"
    assert trade.price == 1.1050


def test_invalid_trade_quantity():
    with pytest.raises(ValueError):
        Trade(
            symbol="EURUSD",
            side=TradeSide.BUY,
            quantity=0,
            price=1.1050,
            timestamp=datetime.now(),
            order_id="ORD-001",
        )


def test_invalid_trade_price():
    with pytest.raises(ValueError):
        Trade(
            symbol="EURUSD",
            side=TradeSide.BUY,
            quantity=1000,
            price=0,
            timestamp=datetime.now(),
            order_id="ORD-001",
        )