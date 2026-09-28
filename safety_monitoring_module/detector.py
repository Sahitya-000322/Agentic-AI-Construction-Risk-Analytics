from ultralytics import YOLO
import cv2
from pathlib import Path

MODEL_PATH = "ppe_model/ppe_detection_best.pt"

model = YOLO(MODEL_PATH)


def detect_workers(image_path):

    results = model.predict(
        source=image_path,
        conf=0.25,
        verbose=False
    )

    result = results[0]

    persons = []
    ppe_items = []

    for box in result.boxes:

        class_id = int(box.cls[0])
        class_name = model.names[class_id]

        x1, y1, x2, y2 = map(int, box.xyxy[0])

        if class_name == "Person":

            persons.append({
                "bbox": (x1, y1, x2, y2)
            })

        elif class_name in ["helmet", "vest", "gloves", "boots"]:

            ppe_items.append({
                "class": class_name,
                "bbox": (x1, y1, x2, y2)
            })

    workers = []

    for person in persons:

        px1, py1, px2, py2 = person["bbox"]

        person_width = px2 - px1
        person_height = py2 - py1

        worker = {
            "helmet": False,
            "vest": False,
            "gloves": False,
            "boots": False,
            "bbox": (px1, py1, px2, py2)
        }

        for item in ppe_items:

            ix1, iy1, ix2, iy2 = item["bbox"]

            center_x = (ix1 + ix2) / 2
            center_y = (iy1 + iy2) / 2

            horizontal_margin = person_width * 0.25
            vertical_margin = person_height * 0.15

            if (
                px1 - horizontal_margin <= center_x <= px2 + horizontal_margin
                and
                py1 - vertical_margin <= center_y <= py2 + vertical_margin
            ):

                worker[item["class"]] = True

        workers.append(worker)

    return workers


def annotate_workers(image_path, workers, output_path="runs/annotated/ppe_result.jpg"):

    image = cv2.imread(image_path)

    for index, worker in enumerate(workers, start=1):

        px1, py1, px2, py2 = worker["bbox"]

        missing = []

        if not worker["helmet"]:
            missing.append("Helmet")

        if not worker["vest"]:
            missing.append("Vest")

        if not worker["gloves"]:
            missing.append("Gloves")

        if not worker["boots"]:
            missing.append("Safety Shoes")

        if missing:
            status = "PPE VIOLATION"
            details = "Missing: " + ", ".join(missing)
        else:
            status = "SAFE"
            details = "All PPE Present"

        risk = worker.get("risk", "Unknown")

        # Worker bounding box
        cv2.rectangle(
            image,
            (px1, py1),
            (px2, py2),
            (0, 0, 255),
            2
        )

        # Worker status
        cv2.putText(
            image,
            f"Worker {index}: {status}",
            (px1, max(py1 - 45, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 0, 255),
            2
        )

        # Missing PPE
        cv2.putText(
            image,
            details,
            (px1, max(py1 - 25, 40)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (0, 0, 255),
            1
        )

        # Risk level
        cv2.putText(
            image,
            f"Risk: {risk}",
            (px1, max(py1 - 7, 60)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 0, 255),
            2
        )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cv2.imwrite(str(output_path), image)

    print(f"Annotated image saved to: {output_path}")

    return str(output_path)


# Compatibility with the old single-worker function
def detect_worker(image_path):

    workers = detect_workers(image_path)

    if not workers:
        return {
            "helmet": False,
            "vest": False,
            "gloves": False,
            "boots": False
        }

    return workers[0]

