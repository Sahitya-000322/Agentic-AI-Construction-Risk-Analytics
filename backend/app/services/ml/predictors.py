"""Tabular predictors wrapping teammate-trained sklearn models.

Every function accepts a plain ``dict`` of raw inputs, reindexes to the
model's expected feature order (via the registry auxiliary artifact when
present), and returns ``{"prediction": ..., "source": "model"}``.
Unknown / missing models raise :class:`ModelNotAvailableError` (mapped to
HTTP 503 by the router) — never a crash.
"""

from __future__ import annotations

from typing import Any

from app.services.ml.registry import ModelNotAvailableError, get_model


def _tabular_predict(model_name: str, row: dict[str, Any]) -> Any:
    import pandas as pd

    model, features = get_model(model_name)
    if isinstance(features, dict) and "features" in features:
        columns: list[str] = list(features["features"])
    elif isinstance(features, (list, tuple)):
        columns = list(features)
    else:
        columns = list(row.keys())
    data = pd.DataFrame([{c: row.get(c, 0) for c in columns}])[columns]
    return model.predict(data)[0]


def predict_safety_risk(
    helmet: int, vest: int, gloves: int, safety_shoes: int, accident: int = 0
) -> dict:
    pred = _tabular_predict(
        "safety_risk",
        {
            "Helmet": int(helmet),
            "Vest": int(vest),
            "Gloves": int(gloves),
            "Safety_Shoes": int(safety_shoes),
            "Accident": int(accident),
        },
    )
    return {"prediction": str(pred), "source": "model"}


def predict_injury(features: dict[str, Any]) -> dict:
    if not features:
        raise ModelNotAvailableError("injury: empty feature dict")
    return {"prediction": str(_tabular_predict("injury", features)), "source": "model"}


def predict_delay(
    workers: float,
    budget: float,
    progress: float,
    weather_rain: int = 0,
    weather_sunny: int = 0,
) -> dict:
    pred = _tabular_predict(
        "delay",
        {
            "Workers": workers,
            "Budget": budget,
            "Progress": progress,
            "Weather_Rain": int(weather_rain),
            "Weather_Sunny": int(weather_sunny),
        },
    )
    label = "Yes" if int(pred) == 1 else "No"
    return {"prediction": label, "raw": int(pred), "source": "model"}


def predict_cost(
    material_cost: float,
    labor_cost: float,
    equipment_cost: float,
    budget: float,
) -> dict:
    pred = _tabular_predict(
        "cost",
        {
            "MaterialCost": material_cost,
            "LaborCost": labor_cost,
            "EquipmentCost": equipment_cost,
            "Budget": budget,
        },
    )
    return {"prediction": str(pred), "source": "model"}


def _generic_predict(model_name: str, features: dict[str, Any]) -> dict:
    if not features:
        raise ModelNotAvailableError(f"{model_name}: empty feature dict")
    return {"prediction": str(_tabular_predict(model_name, features)), "source": "model"}


def predict_schedule(features: dict[str, Any]) -> dict:
    return _generic_predict("schedule", features)


def predict_project_delay(features: dict[str, Any]) -> dict:
    return _generic_predict("project_delay", features)


def predict_resource(features: dict[str, Any]) -> dict:
    return _generic_predict("resource", features)


def predict_compliance(features: dict[str, Any]) -> dict:
    return _generic_predict("compliance", features)


def predict_insurance(features: dict[str, Any]) -> dict:
    return _generic_predict("insurance", features)
