from atlas.backtesting.performance import PerformanceStatistics


def test_total_return():
    stats = PerformanceStatistics([100, -50, 200])

    assert stats.total_return == 250


def test_trade_count():
    stats = PerformanceStatistics([100, -50, 200])

    assert stats.total_trades == 3


def test_winning_trades():
    stats = PerformanceStatistics([100, -50, 200])

    assert stats.winning_trades == 2


def test_losing_trades():
    stats = PerformanceStatistics([100, -50, 200])

    assert stats.losing_trades == 1


def test_win_rate():
    stats = PerformanceStatistics([100, -50, 200])

    assert stats.win_rate == 2 / 3


def test_empty_statistics():
    stats = PerformanceStatistics([])

    assert stats.total_return == 0
    assert stats.total_trades == 0
    assert stats.win_rate == 0