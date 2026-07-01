"""
ATLAS Configuration System (Production Grade)
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central configuration for ATLAS.

    Automatically loads values from .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Core identity
    app_name: str = "ATLAS"
    version: str = "0.1.0"
    environment: str = "development"

    # Trading configuration
    broker: str = "Interactive Brokers"
    paper_trading: bool = True
    max_risk_per_trade: float = 0.005


# Single global settings instance
settings = Settings()