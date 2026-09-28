from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import BaseModel, ConfigDict

from app.dependencies import get_current_user
from app.models.user import User
from app.services.ppe.alerts import check_ppe, play_alarm
from app.services.ppe.detector import (
    PPEModelNotAvailableError,
    detect_workers,
    missing_ppe,
)
from app.services.ppe.logger import save_log
from app.services.ppe.risk import predict_safety_risk

router = APIRouter(prefix="/api/ppe", tags=["ppe"])

MAX_IMAGE_BYTES = 10 * 1024 * 1024


class PPEDetectWorker(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    helmet: bool
    vest: bool
    gloves: bool
    boots: bool
    bbox: list[int]
    risk: str
    risk_source: str
    missing: list[str]
    status: str


class PPEDetectResponse(BaseModel):
    workers_detected: int
    violations: int
    workers: list[PPEDetectWorker]


@router.get("/health")
def ppe_health(_: User = Depends(get_current_user)):
    """Report whether the YOLO PPE model is loadable (never raises)."""
    from app.services.ppe.detector import get_model_path

    path = get_model_path()
    available = path.exists()
    try:
        if available:
            get_model = __import__(
                "app.services.ppe.detector", fromlist=["get_model"]
            ).get_model
            get_model()
    except PPEModelNotAvailableError:
        available = False
    return {
        "available": available,
        "model_path": str(path),
        "detail": "ready" if available else "model file missing — set PPE_MODEL_PATH",
    }


@router.post("/detect", response_model=PPEDetectResponse)
def detect_ppe(
    file: UploadFile = File(...),
    _: User = Depends(get_current_user),
):
    """Detect workers + PPE violations in an uploaded image (max 10 MB)."""
    if file.content_type and not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    content = file.file.read()
    if len(content) > MAX_IMAGE_BYTES:
        raise HTTPException(status_code=413, detail="Image exceeds 10 MB limit")
    if not content:
        raise HTTPException(status_code=400, detail="Empty file")

    try:
        import cv2
        import numpy as np
    except ImportError:
        raise HTTPException(
            status_code=503,
            detail="Image decoding requires opencv-python. "
            "Install with: pip install -r requirements-ml.txt",
        )
    image = cv2.imdecode(np.frombuffer(content, dtype=np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        raise HTTPException(status_code=400, detail="Could not decode image")

    try:
        workers = detect_workers(image)
    except PPEModelNotAvailableError as e:
        raise HTTPException(status_code=503, detail=str(e))

    out: list[PPEDetectWorker] = []
    violations = 0
    for worker in workers:
        risk = predict_safety_risk(
            helmet=worker["helmet"],
            vest=worker["vest"],
            gloves=worker["gloves"],
            safety_shoes=worker["boots"],
        )
        miss = missing_ppe(worker)
        if miss:
            violations += 1
        status = check_ppe(worker, risk["risk"])
        play_alarm(status)
        save_log(status.replace("\n", " | "))
        x1, y1, x2, y2 = (int(v) for v in worker["bbox"])
        out.append(
            PPEDetectWorker(
                helmet=bool(worker["helmet"]),
                vest=bool(worker["vest"]),
                gloves=bool(worker["gloves"]),
                boots=bool(worker["boots"]),
                bbox=[x1, y1, x2, y2],
                risk=risk["risk"],
                risk_source=risk["source"],
                missing=miss,
                status=status,
            )
        )
    return PPEDetectResponse(
        workers_detected=len(out), violations=violations, workers=out
    )
