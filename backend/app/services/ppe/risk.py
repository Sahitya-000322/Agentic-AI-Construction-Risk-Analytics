"""PPE safety risk prediction."""

from __future__ import annotations

import logging

logger = logging.getLogger("buildai.ppe")


def predict_safety_risk(
    helmet: bool,
    vest: bool,
    gloves: bool,
    safety_shoes: bool,
    accident: bool = False,
) -> dict:
    """
    Return PPE safety risk.

    Rules:
    - All PPE available -> Low
    - 1 or 2 PPE missing -> Medium
    - 3 or 4 PPE missing -> High
    - Accident -> High
    """

    helmet = bool(helmet)
    vest = bool(vest)
    gloves = bool(gloves)
    safety_shoes = bool(safety_shoes)
    accident = bool(accident)

    missing = 0

    if not helmet:
        missing += 1

    if not vest:
        missing += 1

    if not gloves:
        missing += 1

    if not safety_shoes:
        missing += 1

    # Accident always means High Risk
    if accident:
        return {
            "risk": "High",
            "source": "safety rule",
        }

    # 3 or 4 PPE items missing = High Risk
    if missing >= 3:
        return {
            "risk": "High",
            "source": "safety rule",
        }

    # 1 or 2 PPE items missing = Medium Risk
    if missing >= 1:
        return {
            "risk": "Medium",
            "source": "safety rule",
        }

    # All PPE available = Low Risk
    return {
        "risk": "Low",
        "source": "safety rule",
    }