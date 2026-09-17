import os
import sys
import logging
from typing import Optional
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Configurable defaults
DEFAULT_START_DATE = "2026-09-07"
DEFAULT_TIMEZONE_OFFSET = timedelta(hours=5, minutes=30)  # Asia/Kolkata (IST)

def setup_logger(name: str = "automation") -> logging.Logger:
    """Configures and returns a clean stdout logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s", "%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

logger = setup_logger()

def get_repo_root() -> Path:
    """Finds the root repository folder."""
    return Path(__file__).resolve().parent.parent.parent

def get_ist_now() -> datetime:
    """Returns the current date and time in IST (Asia/Kolkata)."""
    ist = timezone(DEFAULT_TIMEZONE_OFFSET, name="IST")
    return datetime.now(ist)

def get_current_day(start_date_str: Optional[str] = None, target_date_str: Optional[str] = None) -> int:
    """
    Calculates current day index (1-based) based on start_date and target_date (or today in IST).
    Formula: (target_date - start_date).days + 1
    """
    if not start_date_str:
        start_date_str = os.getenv("START_DATE", DEFAULT_START_DATE)
    
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()

    if target_date_str:
        target_date = datetime.strptime(target_date_str, "%Y-%m-%d").date()
    else:
        target_date = get_ist_now().date()

    day_diff = (target_date - start_date).days + 1
    return day_diff
