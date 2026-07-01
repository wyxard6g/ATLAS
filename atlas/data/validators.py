from atlas.domain.candle import Candle


def validate_candles(candles: list[Candle]) -> None:
    """
    Validate a list of Candle objects.
    """

    if not candles:
        raise ValueError("Candles list cannot be empty.")

    timestamps = [candle.timestamp for candle in candles]

    if timestamps != sorted(timestamps):
        raise ValueError("Candles must be sorted by timestamp.")