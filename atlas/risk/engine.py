from atlas.domain.signal import Signal
from atlas.risk.registry import RiskRegistry


class RiskEngine:
    """
    Executes risk validation.
    """

    def __init__(self, registry: RiskRegistry):
        self._registry = registry

    def evaluate(
        self,
        model_name: str,
        signal: Signal,
    ) -> bool:
        model = self._registry.get(model_name)

        return model.approve(signal)