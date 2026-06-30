from atlas.core.logger import logger
from atlas.core.settings import settings

logger.info("ATLAS has started successfully.")

logger.info(f"Application: {settings.app_name}")

logger.info(f"Version: {settings.version}")

logger.info(f"Broker: {settings.broker}")

logger.info(f"Paper Trading: {settings.paper_trading}")