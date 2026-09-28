"""ML model registry for locally trained models."""

from __future__ import annotations

import logging
import os
import sys
import threading
from pathlib import Path
from typing import Any

import sklearn._loss
import sklearn._loss._loss


logger = logging.getLogger("buildai.ml")


# ============================================================
# PROJECT ROOT
# ============================================================

# C:\Users\Sahitya\Desktop\Agentic Construction
_REPO_ROOT = Path(__file__).resolve().parents[4]


# Existing trained models:
# C:\Users\Sahitya\Desktop\Agentic Construction\models
_DEFAULT_MODEL_DIR = _REPO_ROOT / "models"


def model_dir() -> Path:
    """Return the directory containing the trained model packages."""

    custom = os.environ.get("MODEL_DIR")

    if custom:
        return Path(custom)

    return _DEFAULT_MODEL_DIR


# ============================================================
# MODEL FILE REGISTRY
# ============================================================

# Paths are relative to the project's models/ directory.

MODEL_FILES: dict[str, tuple[str, str | None]] = {

    "safety_risk": (
        "Safety_Agent_Model_v1.0_FINAL/"
        "safety_risk_model/"
        "safety_risk_model.pkl",

        "Safety_Agent_Model_v1.0_FINAL/"
        "safety_risk_model/"
        "safety_risk_features.pkl",
    ),

    "injury": (
        "Safety_Agent_Model_v1.0_FINAL/"
        "injury_prediction_model/"
        "injury_prediction_model.pkl",

        "Safety_Agent_Model_v1.0_FINAL/"
        "injury_prediction_model/"
        "injury_prediction_features.pkl",
    ),

    "delay": (
        "delay_prediction/"
        "delay_prediction_model.joblib",

        "delay_prediction/"
        "delay_feature_info.json",
    ),

    "cost": (
        "cost_prediction/"
        "cost_prediction_model.joblib",

        "cost_prediction/"
        "feature_info.json",
    ),

    "schedule": (
        "schedule_intelligence_model/"
        "schedule_delay_prediction_model.pkl",

        None,
    ),

    "project_delay": (
        "project_delay_intelligence_model/"
        "project_delay_prediction_model.pkl",

        None,
    ),

    "resource": (
        "Resource_Intelligence_Model/"
        "resource_equipment_shortage_model.pkl",

        None,
    ),

    "compliance": (
        "Milestone_3_Compliance_Insurance_Intelligence_v1.0/"
        "Milestone_3_Compliance_Insurance_Intelligence_v1.0/"
        "compliance_intelligence_model/"
        "compliance_intelligence_model.pkl",

        "Milestone_3_Compliance_Insurance_Intelligence_v1.0/"
        "Milestone_3_Compliance_Insurance_Intelligence_v1.0/"
        "compliance_intelligence_model/"
        "compliance_intelligence_features.pkl",
    ),

    "insurance": (
        "Milestone_3_Compliance_Insurance_Intelligence_v1.0/"
        "Milestone_3_Compliance_Insurance_Intelligence_v1.0/"
        "insurance_intelligence_model/"
        "insurance_intelligence_model.pkl",

        "Milestone_3_Compliance_Insurance_Intelligence_v1.0/"
        "Milestone_3_Compliance_Insurance_Intelligence_v1.0/"
        "insurance_intelligence_model/"
        "insurance_intelligence_features.pkl",
    ),
}


# ============================================================
# EXCEPTIONS
# ============================================================

class ModelNotAvailableError(RuntimeError):
    """Raised when a requested trained model is not available."""


# ============================================================
# MODEL CACHE
# ============================================================

_CACHE: dict[str, tuple[Any, Any]] = {}

_LOCK = threading.Lock()


# ============================================================
# PATH RESOLUTION
# ============================================================

def _resolve(path: str | None) -> Path | None:
    """Resolve a model path relative to the model directory."""

    if path is None:
        return None

    return model_dir() / path


# ============================================================
# MODEL AVAILABILITY
# ============================================================

def model_available(name: str) -> bool:
    """Return True when the model file and required feature file exist."""

    entry = MODEL_FILES.get(name)

    if entry is None:
        return False

    model_path = _resolve(entry[0])

    if model_path is None or not model_path.is_file():
        return False

    # Check feature file if the model requires one
    if entry[1] is not None:

        feature_path = _resolve(entry[1])

        if feature_path is None or not feature_path.is_file():
            return False

    return True


# ============================================================
# REGISTERED MODELS
# ============================================================

def registered_models() -> list[dict[str, Any]]:
    """Return availability information for all registered models."""

    result = []

    for name, (model_file, features_file) in MODEL_FILES.items():

        result.append(
            {
                "name": name,
                "available": model_available(name),
                "model_file": model_file,
                "features_file": features_file,
                "loaded": name in _CACHE,
            }
        )

    return result


# ============================================================
# LOAD MODEL
# ============================================================

def get_model(name: str) -> tuple[Any, Any]:
    """Load and cache a trained model and optional feature metadata."""

    # --------------------------------------------------------
    # Check whether model is registered
    # --------------------------------------------------------

    if name not in MODEL_FILES:

        raise ModelNotAvailableError(
            f"Unknown model: {name}"
        )

    # --------------------------------------------------------
    # Return cached model if already loaded
    # --------------------------------------------------------

    if name in _CACHE:
        return _CACHE[name]

    # --------------------------------------------------------
    # Get registered paths
    # --------------------------------------------------------

    model_file, features_file = MODEL_FILES[name]

    model_path = _resolve(model_file)

    feature_path = _resolve(features_file)

    # --------------------------------------------------------
    # Check model file
    # --------------------------------------------------------

    if model_path is None or not model_path.is_file():

        raise ModelNotAvailableError(
            f"Model '{name}' not found: {model_path}"
        )

    # --------------------------------------------------------
    # Check feature file
    # --------------------------------------------------------

    if feature_path is not None and not feature_path.is_file():

        raise ModelNotAvailableError(
            f"Feature file for '{name}' not found: {feature_path}"
        )

    # --------------------------------------------------------
    # Load model
    # --------------------------------------------------------

    try:

        import joblib

        # ====================================================
        # SCIKIT-LEARN COMPATIBILITY
        # ====================================================
        #
        # Some of the saved models were created with an older
        # sklearn pickle structure that refers directly to:
        #
        #     _loss
        #
        # Current sklearn uses:
        #
        #     sklearn._loss._loss
        #
        # Map the old module name to the current compiled
        # sklearn loss module so the existing model can be
        # loaded without modifying or retraining it.
        # ====================================================

        sys.modules.setdefault(
            "_loss",
            sklearn._loss._loss
        )

        # ----------------------------------------------------
        # Thread-safe loading
        # ----------------------------------------------------

        with _LOCK:

            if name in _CACHE:
                return _CACHE[name]

            # ------------------------------------------------
            # Load trained model
            # ------------------------------------------------

            model = joblib.load(model_path)

            # ------------------------------------------------
            # Load optional feature metadata
            # ------------------------------------------------

            features = None

            if feature_path is not None:

                # JSON feature metadata
                if feature_path.suffix.lower() == ".json":

                    import json

                    with feature_path.open(
                        "r",
                        encoding="utf-8"
                    ) as f:

                        features = json.load(f)

                # Joblib feature metadata
                else:

                    features = joblib.load(feature_path)

            # ------------------------------------------------
            # Cache loaded model
            # ------------------------------------------------

            _CACHE[name] = (
                model,
                features
            )

            logger.info(
                "Loaded ML model '%s' from %s",
                name,
                model_path,
            )

            return model, features

    # --------------------------------------------------------
    # Handle model loading errors
    # --------------------------------------------------------

    except Exception as exc:

        logger.exception(
            "Failed to load model '%s'",
            name,
        )

        raise ModelNotAvailableError(
            f"Could not load model '{name}': {exc}"
        ) from exc