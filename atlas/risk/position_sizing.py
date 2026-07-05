class PositionSizingEngine:
    """
    Calculates position size based on account risk and stop-loss distance.
    """

    def __init__(self, risk_per_trade: float):
        if risk_per_trade <= 0:
            raise ValueError("Risk per trade must be greater than 0.")

        if risk_per_trade > 1:
            raise ValueError("Risk per trade cannot exceed 100%.")

        self.risk_per_trade = risk_per_trade

    def calculate_size(
        self,
        account_equity: float,
        entry_price: float,
        stop_loss_price: float,
    ) -> float:
        if account_equity <= 0:
            raise ValueError("Account equity must be greater than 0.")

        if entry_price <= 0:
            raise ValueError("Entry price must be greater than 0.")

        if stop_loss_price <= 0:
            raise ValueError("Stop loss price must be greater than 0.")

        risk_amount = account_equity * self.risk_per_trade
        risk_per_unit = abs(entry_price - stop_loss_price)

        if risk_per_unit <= 0:
            raise ValueError("Risk per unit must be greater than 0.")

        return risk_amount / risk_per_unit