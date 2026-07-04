from atlas.domain.signal import Signal
from atlas.risk.base import RiskModel


class MinimumConfidenceRiskModel(RiskModel):
    """
    Reject signals below a confidence threshold.
    """

    def __init__(self, minimum_confidence: float = 0.60):
        if not 0 <= minimum_confidence <= 1:
            raise ValueError(
                "Minimum confidence must be between 0 and 1."
            )

        self.minimum_confidence = minimum_confidence

    @property
    def name(self) -> str:
        return "minimum_confidence"

    def approve(self, signal: Signal) -> bool:
        return signal.confidence >= self.minimum_confidence