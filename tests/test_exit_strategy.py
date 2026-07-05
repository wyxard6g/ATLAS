import pytest

from atlas.domain.position import Position
from atlas.exit_strategies.engine import ExitStrategyEngine
from atlas.exit_strategies.fixed_percent import FixedPercentExitStrategy
from atlas.exit_strategies.registry import ExitStrategyRegistry


def test_fixed_percent_exit_take_profit():
    position = Position(
        symbol="EURUSD",
        quantity=10,
        average_price=100,
    )

    strategy = FixedPercentExitStrategy(
        take_profit_percent=0.10,
        stop_loss_percent=0.05,
    )

    assert strategy.should_exit(position, current_price=110) is True


def test_fixed_percent_exit_stop_loss():
    position = Position(
        symbol="EURUSD",
        quantity=10,
        average_price=100,
    )

    strategy = FixedPercentExitStrategy(
        take_profit_percent=0.10,
        stop_loss_percent=0.05,
    )

    assert strategy.should_exit(position, current_price=95) is True


def test_fixed_percent_exit_hold():
    position = Position(
        symbol="EURUSD",
        quantity=10,
        average_price=100,
    )

    strategy = FixedPercentExitStrategy(
        take_profit_percent=0.10,
        stop_loss_percent=0.05,
    )

    assert strategy.should_exit(position, current_price=103) is False


def test_fixed_percent_exit_rejects_invalid_parameters():
    with pytest.raises(ValueError):
        FixedPercentExitStrategy(
            take_profit_percent=0,
            stop_loss_percent=0.05,
        )


def test_exit_strategy_engine():
    position = Position(
        symbol="EURUSD",
        quantity=10,
        average_price=100,
    )

    registry = ExitStrategyRegistry()
    registry.register(
        FixedPercentExitStrategy(
            take_profit_percent=0.10,
            stop_loss_percent=0.05,
        )
    )

    engine = ExitStrategyEngine(registry)

    assert engine.should_exit(
        strategy_name="fixed_percent",
        position=position,
        current_price=110,
    ) is True