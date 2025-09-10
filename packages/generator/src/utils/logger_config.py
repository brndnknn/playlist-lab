"""
Logger configuration for playlistGenAI.

Provides a global logger and a helper to set the log file path per run.
"""

import logging
import sys
from typing import Optional

logger = logging.getLogger("playlistGenAI")
logger.setLevel(logging.DEBUG)

_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Default to console logging; file logging can be configured per run
# if not any(isinstance(h, logging.StreamHandler) for h in logger.handlers):
#     _console = logging.StreamHandler(sys.stdout)
#     _console.setLevel(logging.INFO)
#     _console.setFormatter(_formatter)
#     logger.addHandler(_console)


def set_log_file(path: str, mode: str = "a", level: int = logging.DEBUG) -> None:
    """
    Configure the logger to write to the specified file.

    Existing FileHandlers are removed to avoid duplicate logs.

    Args:
        path: File path for the log output.
        mode: File open mode ('a' to append, 'w' to truncate).
        level: Log level for the file handler.
    """
    # Remove existing file handlers
    for h in list(logger.handlers):
        if isinstance(h, logging.FileHandler):
            logger.removeHandler(h)

    fh = logging.FileHandler(path, mode=mode)
    fh.setLevel(level)
    fh.setFormatter(_formatter)
    logger.addHandler(fh)
