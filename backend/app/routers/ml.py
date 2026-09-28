from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.dependencies import get_current_user
from app.models.user import User
from app.services.ml import predictors
from app.services.ml.registry import ModelNotAvailableError, registered_models

router = APIRouter(prefix="/api/ml", tags=["ml"])


def _or_503(fn, *args, **kwargs):
    try:
        return fn(*args, **kwargs)
    except ModelNotAvailableError as e:
        raise HTTPException(status_code=503, detail=str(e))


class SafetyRiskIn(BaseModel):
    helmet: int = Field(0, ge=0, le=1)
    vest: int = Field(0, ge=0, le=1)
    gloves: int = Field(0, ge=0, le=1)
    safety_shoes: int = Field(0, ge=0, le=1)
    accident: int = Field(0, ge=0, le=1)


class DelayIn(BaseModel):
    workers: float
    budget: float
    progress: float
    weather_rain: int = Field(0, ge=0, le=1)
    weather_sunny: int = Field(0, ge=0, le=1)


class CostIn(BaseModel):
    material_cost: float = Field(..., alias="MaterialCost")
    labor_cost: float = Field(..., alias="LaborCost")
    equipment_cost: float = Field(..., alias="EquipmentCost")
    budget: float = Field(..., alias="Budget")

    model_config = {"populate_by_name": True}


class FeaturesIn(BaseModel):
    features: dict = Field(default_factory=dict)


@router.get("/models")
def list_models(_: User = Depends(get_current_user)):
    return {"models": registered_models()}


@router.post("/predict/safety-risk")
def ml_safety_risk(payload: SafetyRiskIn, _: User = Depends(get_current_user)):
    return _or_503(predictors.predict_safety_risk, **payload.model_dump())


@router.post("/predict/injury")
def ml_injury(payload: FeaturesIn, _: User = Depends(get_current_user)):
    return _or_503(predictors.predict_injury, payload.features)


@router.post("/predict/delay")
def ml_delay(payload: DelayIn, _: User = Depends(get_current_user)):
    return _or_503(predictors.predict_delay, **payload.model_dump())


@router.post("/predict/cost")
def ml_cost(payload: CostIn, _: User = Depends(get_current_user)):
    return _or_503(
        predictors.predict_cost,
        material_cost=payload.material_cost,
        labor_cost=payload.labor_cost,
        equipment_cost=payload.equipment_cost,
        budget=payload.budget,
    )


@router.post("/predict/schedule")
def ml_schedule(payload: FeaturesIn, _: User = Depends(get_current_user)):
    return _or_503(predictors.predict_schedule, payload.features)


@router.post("/predict/project-delay")
def ml_project_delay(payload: FeaturesIn, _: User = Depends(get_current_user)):
    return _or_503(predictors.predict_project_delay, payload.features)


@router.post("/predict/resource")
def ml_resource(payload: FeaturesIn, _: User = Depends(get_current_user)):
    return _or_503(predictors.predict_resource, payload.features)


@router.post("/predict/compliance")
def ml_compliance(payload: FeaturesIn, _: User = Depends(get_current_user)):
    return _or_503(predictors.predict_compliance, payload.features)


@router.post("/predict/insurance")
def ml_insurance(payload: FeaturesIn, _: User = Depends(get_current_user)):
    return _or_503(predictors.predict_insurance, payload.features)
