from datetime import datetime, timedelta

from atlas.domain.candle import Candle
from atlas.domain.market_data import MarketData
from atlas.features.context import FeatureContext


def test_feature_context_from_market_data():
    now = datetime.now()

    candles = [
        Candle(now, 100, 105, 95, 102, 1000),
        Candle(now + timedelta(minutes=1), 102, 106, 101, 104, 1200),
    ]

    market_data = MarketData(
        symbol="EURUSD",
        timeframe="1m",
        source="test",
        candles=candles,
    )

    context = FeatureContext.from_market_data(market_data)

    assert context.symbol == "EURUSD"
    assert context.timeframe == "1m"
    assert context.count == 2
    assert context.closes == [102, 104]
    assert context.volumes == [1000, 1200]