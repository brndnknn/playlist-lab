import logging
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

LOG_DIR = Path(__file__).parent / "logs"
LOG_FILE = LOG_DIR / "rate_limit_tests.log"


def pytest_configure(config):
    LOG_DIR.mkdir(exist_ok=True)

    handler = logging.FileHandler(LOG_FILE, mode="w")
    handler.setLevel(logging.INFO)
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    )

    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    if root_logger.level > logging.INFO:
        root_logger.setLevel(logging.INFO)

    config._rate_limit_log_handler = handler


def pytest_unconfigure(config):
    handler = getattr(config, "_rate_limit_log_handler", None)
    if not handler:
        return
    root_logger = logging.getLogger()
    root_logger.removeHandler(handler)
    handler.close()
