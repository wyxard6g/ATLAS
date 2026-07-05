from datetime import datetime
from zoneinfo import ZoneInfo

from atlas.market.sessions import AssetClass, MarketSession


def test_crypto_market_always_open():
    session = MarketSession(asset_class=AssetClass.CRYPTO)

    saturday = datetime(2026, 7, 4, 12, 0, tzinfo=ZoneInfo("UTC"))

    assert session.is_market_open(saturday) is True


def test_stock_market_closed_on_weekend():
    session = MarketSession(
        asset_class=AssetClass.STOCK,
        timezone="America/New_York",
    )

    saturday = datetime(
        2026,
        7,
        4,
        12,
        0,
        tzinfo=ZoneInfo("America/New_York"),
    )

    assert session.is_market_open(saturday) is False


def test_stock_market_open_during_regular_hours():
    session = MarketSession(
        asset_class=AssetClass.STOCK,
        timezone="America/New_York",
    )

    monday = datetime(
        2026,
        7,
        6,
        10,
        0,
        tzinfo=ZoneInfo("America/New_York"),
    )

    assert session.is_market_open(monday) is True


def test_forex_closed_on_saturday():
    session = MarketSession(asset_class=AssetClass.FOREX)

    saturday = datetime(2026, 7, 4, 12, 0, tzinfo=ZoneInfo("UTC"))

    assert session.is_market_open(saturday) is False