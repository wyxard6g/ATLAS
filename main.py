from atlas.core.logger import logger
from atlas.core.exceptions import RiskLimitExceededError

logger.info("ATLAS starting...")

try:
    raise RiskLimitExceededError("Risk exceeds maximum allowed.")

except RiskLimitExceededError as error:
    logger.error(error)