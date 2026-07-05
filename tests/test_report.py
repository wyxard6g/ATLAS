from atlas.backtesting.report import BacktestReport


def test_report_string_contains_metrics():
    report = BacktestReport(
        starting_capital=100000,
        ending_capital=112500,
        total_return=12500,
        total_trades=50,
        winning_trades=32,
        losing_trades=18,
        win_rate=0.64,
        maximum_drawdown=0.031,
        profit_factor=1.84,
        sharpe_ratio=1.56,
    )

    text = str(report)

    assert "ATLAS BACKTEST REPORT" in text
    assert "112,500.00" in text
    assert "50" in text
    assert "64.00%" in text