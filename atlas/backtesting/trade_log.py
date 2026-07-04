from dataclasses import dataclass, field

from atlas.domain.trade import Trade


@dataclass(slots=True)
class TradeLog:
    """
    Stores completed trades from a backtest.
    """

    trades: list[Trade] = field(default_factory=list)

    def add(self, trade: Trade) -> None:
        self.trades.append(trade)

    @property
    def count(self) -> int:
        return len(self.trades)