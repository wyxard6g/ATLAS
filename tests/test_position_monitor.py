from datetime import datetime

from atlas.backtesting.exit_engine import ExitEngine
from atlas.backtesting.portfolio_manager import PortfolioManager
from atlas.backtesting.position_manager import PositionManager
from atlas.backtesting.position_monitor import PositionMonitor
from atlas.domain.signal import Signal, SignalType
from atlas.exit_strategies.engine import ExitStrategyEngine
from atlas.exit_strategies.fixed_percent import FixedPercentExitStrategy
from atlas.exit_strategies.registry import ExitStrategyRegistry


def make_signal():
    return Signal(
        symbol="EURUSD",
        signal_type=SignalType.BUY,
        confidence=0.9,
        timeframe="1m",
        strategy="test",
        timestamp=datetime.now(),
        reason="unit test",
    )


def test_position_monitor_closes_position_at_take_profit():
    portfolio = PortfolioManager(100_000)
    positions = PositionManager()

    positions.open(
        signal=make_signal(),
        quantity=10,
        entry_price=100,
    )

    registry = ExitStrategyRegistry()
    registry.register(
        FixedPercentExitStrategy(
            take_profit_percent=0.10,
            stop_loss_percent=0.05,
        )
    )

    exit_strategy_engine = ExitStrategyEngine(registry)

    exit_engine = ExitEngine(
        portfolio_manager=portfolio,
        position_manager=positions,
    )

    monitor = PositionMonitor(
        position_manager=positions,
        exit_strategy_engine=exit_strategy_engine,
        exit_engine=exit_engine,
        exit_strategy_name="fixed_percent",
    )

    pnl = monitor.check_exit(
        symbol="EURUSD",
        current_price=110,
    )

    assert pnl == 100
    assert positions.count == 0
    assert portfolio.cash == 101_100


def test_position_monitor_holds_when_exit_not_triggered():
    portfolio = PortfolioManager(100_000)
    positions = PositionManager()

    positions.open(
        signal=make_signal(),
        quantity=10,
        entry_price=100,
    )

    registry = ExitStrategyRegistry()
    registry.register(
        FixedPercentExitStrategy(
            take_profit_percent=0.10,
            stop_loss_percent=0.05,
        )
    )

    exit_strategy_engine = ExitStrategyEngine(registry)

    exit_engine = ExitEngine(
        portfolio_manager=portfolio,
        position_manager=positions,
    )

    monitor = PositionMonitor(
        position_manager=positions,
        exit_strategy_engine=exit_strategy_engine,
        exit_engine=exit_engine,
        exit_strategy_name="fixed_percent",
    )

    pnl = monitor.check_exit(
        symbol="EURUSD",
        current_price=103,
    )

    assert pnl is None
    assert positions.count == 1
    assert portfolio.cash == 100_000


def test_position_monitor_returns_none_when_no_position():
    portfolio = PortfolioManager(100_000)
    positions = PositionManager()

    registry = ExitStrategyRegistry()
    registry.register(
        FixedPercentExitStrategy(
            take_profit_percent=0.10,
            stop_loss_percent=0.05,
        )
    )

    exit_strategy_engine = ExitStrategyEngine(registry)

    exit_engine = ExitEngine(
        portfolio_manager=portfolio,
        position_manager=positions,
    )

    monitor = PositionMonitor(
        position_manager=positions,
        exit_strategy_engine=exit_strategy_engine,
        exit_engine=exit_engine,
        exit_strategy_name="fixed_percent",
    )

    pnl = monitor.check_exit(
        symbol="EURUSD",
        current_price=110,
    )

    assert pnl is None