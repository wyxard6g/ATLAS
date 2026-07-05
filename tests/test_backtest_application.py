from datetime import datetime, timedelta
from pathlib import Path

import pytest

from atlas.app.backtest_application import BacktestApplication


def test_backtest_application_runs_with_csv(tmp_path: Path):
    csv_file = tmp_path / "candles.csv"

    start = datetime(2026, 1, 1)

    rows = ["timestamp,open,high,low,close,volume"]

    for i in range(60):
        timestamp = start + timedelta(minutes=i)
        price = 100 + i

        rows.append(
            f"{timestamp.isoformat()},{price},{price + 2},{price - 2},{price},1000"
        )

    csv_file.write_text("\n".join(rows))

    app = BacktestApplication(starting_capital=100_000)

    report = app.run(str(csv_file))

    assert report.starting_capital == 100_000
    assert report.total_trades >= 1


def test_backtest_application_rejects_invalid_starting_capital():
    with pytest.raises(ValueError):
        BacktestApplication(starting_capital=0)


def test_backtest_application_validates_missing_file():
    app = BacktestApplication()

    with pytest.raises(FileNotFoundError):
        app.validate_file("missing.csv")


def test_backtest_application_rejects_non_csv_file(tmp_path: Path):
    txt_file = tmp_path / "candles.txt"
    txt_file.write_text("not a csv")

    app = BacktestApplication()

    with pytest.raises(ValueError):
        app.validate_file(str(txt_file))