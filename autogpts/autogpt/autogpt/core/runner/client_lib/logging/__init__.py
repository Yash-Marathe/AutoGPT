import logging
import sys

from .config import BelowLevelFilter, FancyConsoleFormatter, configure_logging as configure_root_logger
from .helpers import dump_prompt


def get_client_logger():
    """
    Configures logging before doing anything else and returns a logger for the
    autogpt_client_application.
    """
    client_logger = logging.getLogger("autogpt_client_application")
    client_logger.setLevel(logging.DEBUG)

    # Create a console handler with a formatter and a filter
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FancyConsoleFormatter())
    console_handler.addFilter(BelowLevelFilter())

    # Add the console handler to the logger

