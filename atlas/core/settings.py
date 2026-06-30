"""
ATLAS Configuration Settings

This module stores all global settings used by the application.
"""

from dataclasses import dataclass


@dataclass
class Settings:
    """
    Global configuration for ATLAS.
    """

    app_name: str = "ATLAS"

    version: str = "0.1.0"

    environment: str = "development"

    broker: str = "Interactive Brokers"

    paper_trading: bool = True

    max_risk_per_trade: float = 0.005  # 0.5%


settings = Settings()