from pathlib import Path

from ultralytics import YOLO


# Project root:
# C:\Users\Sahitya\Desktop\Agentic Construction
PROJECT_ROOT = Path(__file__).resolve().parents[3]

MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "PPE_Detection_Intelligence_v1.0"
    / "models"
    / "ppe_detection_best.pt"
)

model = YOLO(str(MODEL_PATH))


def detect_ppe(image_path: str, confidence: float = 0.25):
    """
    Run PPE detection on an image.

    Returns a list of detected objects with:
    - class_id
    - class_name
    - confidence
    - bounding_box
    """

    results = model.predict(
        source=image_path,
        conf=confidence,
        verbose=False,
    )

    result = results[0]
    detections = []

    if result.boxes is None:
        return detections

    for box in result.boxes:
        class_id = int(box.cls[0])
        confidence_score = float(box.conf[0])

        x1, y1, x2, y2 = box.xyxy[0].tolist()

        detections.append(
            {
                "class_id": class_id,
                "class_name": model.names[class_id],
                "confidence": round(confidence_score, 4),
                "bounding_box": {
                    "x1": round(x1, 2),
                    "y1": round(y1, 2),
                    "x2": round(x2, 2),
                    "y2": round(y2, 2),
                },
            }
        )

    return detections