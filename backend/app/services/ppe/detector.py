"""PPE detection service (ported from teammate D-drive `detector.py`).

Changes vs original:
- Lazy model loading via :func:`get_model` (no import-time crash when the
  ``.pt`` file is absent — raises :class:`PPEModelNotAvailableError` instead).
- Model path configurable via ``PPE_MODEL_PATH`` env var.
- Pure functions take explicit ``model`` arg so tests can inject fakes.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

PPE_CLASSES = ("helmet", "vest", "gloves", "boots")

DEFAULT_MODEL_PATH = os.environ.get(
    "PPE_MODEL_PATH", "ppe_model/ppe_detection_best.pt"
)


class PPEModelNotAvailableError(RuntimeError):
    """Raised when the YOLO PPE model file cannot be loaded."""


_model = None


def get_model_path() -> Path:
    env_path = os.environ.get("PPE_MODEL_PATH")

    if env_path:
        return Path(env_path)

    repo_root = Path(__file__).resolve().parents[4]

    return (
        repo_root
        / "models"
        / "PPE_Detection_Intelligence_v1.0"
        / "models"
        / "ppe_detection_best.pt"
    )

def get_model() -> Any:
    """Load (once) and return the YOLO PPE model.

    Raises:
        PPEModelNotAvailableError: if the model file is missing or the
            ``ultralytics`` package is not installed.
    """
    global _model
    if _model is not None:
        return _model
    try:
        from ultralytics import YOLO
    except ImportError as e:
        raise PPEModelNotAvailableError(
            "ultralytics package not installed. "
            "Install with: pip install -r requirements-ml.txt"
        ) from e
    path = get_model_path()
    if not path.exists():
        raise PPEModelNotAvailableError(
            f"PPE model not found at {path}. "
            "Set PPE_MODEL_PATH env var to a valid .pt file."
        )
    _model = YOLO(str(path))
    return _model


def match_ppe_to_workers(
    persons: list[dict],
    ppe_items: list[dict],
    horizontal_margin_ratio: float = 0.25,
    vertical_margin_ratio: float = 0.15,
) -> list[dict]:
    """Associate detected PPE items with person boxes (center-in-box rule)."""
    workers: list[dict] = []
    for person in persons:
        px1, py1, px2, py2 = person["bbox"]
        person_width = px2 - px1
        person_height = py2 - py1
        worker: dict = {
            "helmet": False,
            "vest": False,
            "gloves": False,
            "boots": False,
            "bbox": (px1, py1, px2, py2),
        }
        for item in ppe_items:
            ix1, iy1, ix2, iy2 = item["bbox"]
            center_x = (ix1 + ix2) / 2
            center_y = (iy1 + iy2) / 2
            horizontal_margin = person_width * horizontal_margin_ratio
            vertical_margin = person_height * vertical_margin_ratio
            if (
                px1 - horizontal_margin <= center_x <= px2 + horizontal_margin
                and py1 - vertical_margin <= center_y <= py2 + vertical_margin
            ):
                worker[item["class"]] = True
        workers.append(worker)
    return workers


def detect_workers_from_boxes(
    boxes: list[dict], class_names: dict[int, str]
) -> list[dict]:
    """Group raw detection boxes into per-worker PPE dicts.

    ``boxes`` items: ``{"class_id": int, "bbox": (x1, y1, x2, y2)}``.
    """
    persons: list[dict] = []
    ppe_items: list[dict] = []
    for box in boxes:
        class_name = class_names[box["class_id"]]
        if class_name == "Person":
            persons.append({"bbox": box["bbox"]})
        elif class_name in PPE_CLASSES:
            ppe_items.append({"class": class_name, "bbox": box["bbox"]})
    return match_ppe_to_workers(persons, ppe_items)


def detect_workers(image_source: Any, conf: float = 0.25) -> list[dict]:
    """Run YOLO inference on an image path or numpy frame.

    Raises:
        PPEModelNotAvailableError: if the model cannot be loaded.
    """
    model = get_model()
    results = model.predict(source=image_source, conf=conf, verbose=False)
    result = results[0]
    boxes: list[dict] = []
    for box in result.boxes:
        class_id = int(box.cls[0])
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        boxes.append({"class_id": class_id, "bbox": (x1, y1, x2, y2)})
    return detect_workers_from_boxes(boxes, model.names)


def missing_ppe(worker: dict) -> list[str]:
    """Return human-readable names of missing PPE items."""
    missing: list[str] = []
    if not worker.get("helmet"):
        missing.append("Helmet")
    if not worker.get("vest"):
        missing.append("Safety Vest")
    if not worker.get("gloves"):
        missing.append("Gloves")
    if not worker.get("boots"):
        missing.append("Safety Shoes")
    return missing
