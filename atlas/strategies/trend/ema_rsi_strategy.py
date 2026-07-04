from datetime import datetime

from atlas.domain.feature_set import FeatureSet
from atlas.domain.signal import Signal, SignalType
from atlas.strategies.base import Strategy


class EmaRsiTrendStrategy(Strategy):
    """
    Simple trend strategy using EMA alignment and RSI confirmation.
    """

    @property
    def name(self) -> str:
        return "ema_rsi_trend"

    def generate(self, feature_set: FeatureSet) -> Signal:
        ema_fast = feature_set.get("ema_20")
        ema_slow = feature_set.get("ema_50")
        rsi = feature_set.get("rsi_14")

        if ema_fast > ema_slow and rsi > 55:
            signal_type = SignalType.BUY
            reason = "Fast EMA above slow EMA and RSI confirms bullish momentum."
            confidence = 0.70

        elif ema_fast < ema_slow and rsi < 45:
            signal_type = SignalType.SELL
            reason = "Fast EMA below slow EMA and RSI confirms bearish momentum."
            confidence = 0.70

        else:
            signal_type = SignalType.HOLD
            reason = "No strong trend confirmation."
            confidence = 0.50

        return Signal(
            symbol=feature_set.symbol,
            signal_type=signal_type,
            confidence=confidence,
            timeframe=feature_set.timeframe,
            strategy=self.name,
            timestamp=datetime.now(),
            reason=reason,
        )