"""PPE alert + alarm helpers (ported from teammate D-drive).

Changes vs original:
- :func:`play_alarm` is cross-platform (Windows ``winsound`` / Linux ``aplay`` /
  macOS ``afplay``) with graceful log-only fallback.
- Controlled by ``PPE_ALARM_ENABLED`` env var (default ``false`` on servers).
- Violation state-machine helper for "alert once per continuous violation".
"""

from __future__ import annotations

import logging
import os
import platform
import subprocess

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("buildai.ppe")


def check_ppe(worker: dict, risk: str = "Unknown") -> str:
    """Build a human-readable PPE status message for one worker."""
    from app.services.ppe.detector import missing_ppe

    missing = missing_ppe(worker)
    if not missing:
        message = "Worker is Safe"
    else:
        message = "PPE Missing: " + ", ".join(missing)
    return f"{message} | Safety Risk: {risk}"


def play_alarm(status: str, sound_file: str | None = None) -> bool:
    """Play PPE violation alarm on Windows."""

    if "Missing" not in status and "VIOLATION" not in status:
        return False

    if os.environ.get("PPE_ALARM_ENABLED", "false").lower() not in (
        "1",
        "true",
        "yes",
        "on",
    ):
        logger.warning("PPE alarm is disabled")
        return False

    # Always resolve the default sound relative to the backend folder
    if sound_file:
        sound = sound_file
    else:
        backend_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../../..")
        )
        sound = os.path.join(
            backend_dir,
            "sounds",
            "mixkit-emergency-alert-alarm-1007.wav",
        )

    try:
        if not os.path.exists(sound):
            logger.error("PPE alarm sound file not found: %s", sound)
            return False

        logger.warning("PLAYING PPE ALARM: %s", sound)

        if platform.system() == "Windows":
            import winsound

            winsound.PlaySound(
                sound,
                winsound.SND_FILENAME | winsound.SND_ASYNC,
            )
            return True

        elif platform.system() == "Darwin":
            subprocess.run(["afplay", sound], check=False, timeout=10)
            return True

        else:
            subprocess.run(["aplay", sound], check=False, timeout=10)
            return True

    except Exception as e:
        logger.exception("PPE alarm playback failed: %s", e)
        return False


class ViolationTracker:
    """Alert-once-per-continuous-violation state machine.

    Mirrors the logic from teammate ``video_monitor.py`` but reusable and
    testable without OpenCV.
    """

    def __init__(self) -> None:
        self.violation_active = False

    def update(self, has_violation: bool) -> str:
        """Return 'started' | 'ongoing' | 'cleared' | 'clear'."""
        if has_violation and not self.violation_active:
            self.violation_active = True
            return "started"
        if has_violation:
            return "ongoing"
        if self.violation_active:
            self.violation_active = False
            return "cleared"
        return "clear"
