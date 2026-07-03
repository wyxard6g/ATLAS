from atlas.features.base import Feature


class FeatureRegistry:
    """
    Stores all registered features.
    """

    def __init__(self):
        self._features: dict[str, Feature] = {}

    def register(self, feature: Feature) -> None:
        self._features[feature.name] = feature

    def get(self, name: str) -> Feature:
        return self._features[name]

    def all(self) -> list[Feature]:
        return list(self._features.values())