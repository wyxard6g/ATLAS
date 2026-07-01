"""
ATLAS Custom Exceptions
"""


class AtlasError(Exception):
    """Base exception for all ATLAS errors."""
    pass


class ConfigurationError(AtlasError):
    """Raised when configuration is invalid."""
    pass


class BrokerConnectionError(AtlasError):
    """Raised when the broker cannot be reached."""
    pass


class MarketDataError(AtlasError):
    """Raised when market data cannot be retrieved."""
    pass


class RiskLimitExceededError(AtlasError):
    """Raised when a trade violates risk rules."""
    pass


class OrderRejectedError(AtlasError):
    """Raised when an order is rejected."""
    pass


class StrategyValidationError(AtlasError):
    """Raised when a strategy fails validation."""
    pass