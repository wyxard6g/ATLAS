from atlas.domain.position import Position
from atlas.domain.signal import Signal


class PositionManager:
    """
    Manages virtual positions during backtesting.
    """

    def __init__(self):
        self._positions: dict[str, Position] = {}

    @property
    def count(self) -> int:
        return len(self._positions)

    def has_position(self, symbol: str) -> bool:
        return symbol in self._positions

    def get(self, symbol: str) -> Position | None:
        return self._positions.get(symbol)

    def open(
        self,
        signal: Signal,
        quantity: float,
        entry_price: float,
    ) -> Position:
        if self.has_position(signal.symbol):
            raise ValueError(
                f"Position already exists for {signal.symbol}."
            )

        position = Position(
            symbol=signal.symbol,
            quantity=quantity,
            average_price=entry_price,
        )

        self._positions[signal.symbol] = position

        return position

    def close(self, symbol: str) -> Position:
        if not self.has_position(symbol):
            raise ValueError(
                f"No position exists for {symbol}."
            )

        return self._positions.pop(symbol)