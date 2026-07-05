from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class EquityPoint:
    """
    One point in a backtest equity curve.
    """

    timestamp: datetime
    equity: float


@dataclass(slots=True)
class EquityCurve:
    """
    Tracks portfolio equity over time.
    """

    points: list[EquityPoint] = field(default_factory=list)

    def add(self, timestamp: datetime, equity: float) -> None:
        if equity < 0:
            raise ValueError("Equity cannot be negative.")

        self.points.append(
            EquityPoint(
                timestamp=timestamp,
                equity=equity,
            )
        )

    @property
    def count(self) -> int:
        return len(self.points)

    @property
    def latest_equity(self) -> float:
        if not self.points:
            raise ValueError("Equity curve is empty.")

        return self.points[-1].equity