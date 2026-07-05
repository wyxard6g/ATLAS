from datetime import datetime

from atlas.backtesting.engine import BacktestEngine
from atlas.backtesting.portfolio import Portfolio
from atlas.backtesting.statistics import Statistics
from atlas.backtesting.trade_log import TradeLog
from atlas.domain.trade import Trade, TradeSide


def test_trade_log_adds_trade():
    trade_log = TradeLog()

    trade = Trade(
        symbol="EURUSD",
        side=TradeSide.BUY,
        quantity=1000,
        price=1.1000,
        timestamp=datetime.now(),
        order_id="ORD-001",
    )

    trade_log.add(trade)

    assert trade_log.count == 1


def test_portfolio_initialization():
    portfolio = Portfolio(
        cash=100_000,
        equity=100_000,
    )

    assert portfolio.cash == 100_000
    assert portfolio.equity == 100_000


def test_statistics_total_trades():
    trade_log = TradeLog()

    statistics = Statistics(trade_log)

    assert statistics.total_trades == 0


def test_backtest_engine_report():
    engine = BacktestEngine(starting_cash=100_000)

    report = engine.report()

    assert report.total_trades == 0
    assert report.starting_capital == 100_000