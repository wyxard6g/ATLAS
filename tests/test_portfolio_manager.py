import pytest

from atlas.backtesting.portfolio_manager import PortfolioManager


def test_portfolio_manager_initialization():
    manager = PortfolioManager(starting_cash=100_000)

    assert manager.cash == 100_000
    assert manager.equity == 100_000


def test_portfolio_manager_debits_cash():
    manager = PortfolioManager(starting_cash=100_000)

    manager.debit_cash(10_000)

    assert manager.cash == 90_000
    assert manager.equity == 90_000


def test_portfolio_manager_credits_cash():
    manager = PortfolioManager(starting_cash=100_000)

    manager.credit_cash(5_000)

    assert manager.cash == 105_000
    assert manager.equity == 105_000


def test_portfolio_manager_rejects_invalid_starting_cash():
    with pytest.raises(ValueError):
        PortfolioManager(starting_cash=0)


def test_portfolio_manager_rejects_insufficient_cash():
    manager = PortfolioManager(starting_cash=100_000)

    with pytest.raises(ValueError):
        manager.debit_cash(200_000)