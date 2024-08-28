from logging import DEBUG, INFO
from os import getenv

import structlog


def set_up_custom_logging() -> None:
    """Setup custom logging for the application."""
    level = INFO
    if getenv("DEBUG", "false").lower() == "true":
        level = DEBUG
    structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(level))
    structlog.configure()



