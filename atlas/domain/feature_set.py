from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass(frozen=True, slots=True)
class FeatureSet:
    """
    Represents computed features for a symbol and timeframe.
    """

    symbol: str
    timeframe: str
    timestamp: datetime
    features: dict[str, Any]
    source: str = "feature_engine"
    metadata: dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        if not self.symbol.strip():
            raise ValueError("Symbol cannot be empty.")

        if not self.timeframe.strip():
            raise ValueError("Timeframe cannot be empty.")

        if not self.features:
            raise ValueError("FeatureSet must contain at least one feature.")

    def get(self, name: str) -> Any:
        return self.features[name]

    @property
    def count(self) -> int:
        return len(self.features)