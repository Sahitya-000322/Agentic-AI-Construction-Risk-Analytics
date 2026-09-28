"""Violation CSV logger (ported from teammate D-drive ``logger.py``).

Changes vs original: auto-creates the ``logs/`` directory and supports a
configurable path via ``PPE_LOG_PATH`` env var.
"""

from __future__ import annotations

import csv
import os
from datetime import datetime, timezone
from pathlib import Path


def log_path() -> Path:
    return Path(os.environ.get("PPE_LOG_PATH", "logs/violations.csv"))


def save_log(status: str) -> Path:
    """Append one violation row; returns the log file path."""
    path = log_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(timezone.utc).isoformat(), status])
    return path
