from atlas.domain.position import Position
from atlas.exit_strategies.base import ExitStrategy


class FixedPercentExitStrategy(ExitStrategy):
    """
    Exits when price reaches fixed take-profit or stop-loss percentages.
    """

    def __init__(
        self,
        take_profit_percent: float,
        stop_loss_percent: float,
    ):
        if take_profit_percent <= 0:
            raise ValueError("Take profit percent must be greater than 0.")

        if stop_loss_percent <= 0:
            raise ValueError("Stop loss percent must be greater than 0.")

        self.take_profit_percent = take_profit_percent
        self.stop_loss_percent = stop_loss_percent

    @property
    def name(self) -> str:
        return "fixed_percent"

    def should_exit(
        self,
        position: Position,
        current_price: float,
    ) -> bool:
        take_profit_price = position.average_price * (
            1 + self.take_profit_percent
        )

        stop_loss_price = position.average_price * (
            1 - self.stop_loss_percent
        )

        tolerance = 1e-9

        return (
            current_price >= take_profit_price - tolerance
            or current_price <= stop_loss_price + tolerance
        )