from atlas.risk.base import RiskModel


class RiskRegistry:
    """
    Stores available risk models.
    """

    def __init__(self):
        self._models: dict[str, RiskModel] = {}

    def register(self, model: RiskModel):
        self._models[model.name] = model

    def get(self, name: str) -> RiskModel:
        return self._models[name]