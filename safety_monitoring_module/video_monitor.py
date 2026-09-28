import cv2
import os

from ultralytics import YOLO
from risk_predictor import predict_risk
from alert import check_ppe
from logger import save_log


MODEL_PATH = "ppe_model/ppe_detection_best.pt"
VIDEO_PATH = "test_videos/test.mp4"
OUTPUT_PATH = "runs/video_monitor/output.mp4"

model = YOLO(MODEL_PATH)

# Process every 5th frame
FRAME_SKIP = 5


def detect_frame(frame):

    results = model.predict(
        source=frame,
        conf=0.25,
        imgsz=416,
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

        width = px2 - px1
        height = py2 - py1

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

            horizontal_margin = width * 0.25
            vertical_margin = height * 0.15

            if (
                px1 - horizontal_margin <= center_x <= px2 + horizontal_margin
                and
                py1 - vertical_margin <= center_y <= py2 + vertical_margin
            ):

                worker[item["class"]] = True

        workers.append(worker)

    return workers


def get_violation(worker):

    missing = []

    if not worker["helmet"]:
        missing.append("Helmet")

    if not worker["vest"]:
        missing.append("Vest")

    if not worker["gloves"]:
        missing.append("Gloves")

    if not worker["boots"]:
        missing.append("Safety Shoes")

    return missing


def draw_worker(frame, worker, index):

    x1, y1, x2, y2 = worker["bbox"]

    missing = get_violation(worker)

    if missing:

        status = "PPE VIOLATION"
        details = "Missing: " + ", ".join(missing)

    else:

        status = "SAFE"
        details = "All PPE Present"

    risk = worker.get("risk", "Unknown")

    cv2.rectangle(
        frame,
        (x1, y1),
        (x2, y2),
        (0, 0, 255),
        2
    )

    cv2.putText(
        frame,
        f"Worker {index}: {status}",
        (x1, max(y1 - 45, 20)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (0, 0, 255),
        2
    )

    cv2.putText(
        frame,
        details,
        (x1, max(y1 - 25, 40)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.45,
        (0, 0, 255),
        1
    )

    cv2.putText(
        frame,
        f"Risk: {risk}",
        (x1, max(y1 - 7, 60)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (0, 0, 255),
        2
    )


def main():

    cap = cv2.VideoCapture(VIDEO_PATH)

    if not cap.isOpened():

        print("❌ Could not open video.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps <= 0:
        fps = 25

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    writer = cv2.VideoWriter(
        OUTPUT_PATH,
        fourcc,
        fps,
        (width, height)
    )

    print("\n🎥 Video monitoring started")
    print("🚨 Alert will be shown only once for a continuous violation.")
    print("Press Q in the video window or Ctrl+C in Terminal to stop.\n")

    # Stores whether a violation is currently active
    violation_active = False

    last_workers = []

    frame_count = 0

    try:

        while True:

            success, frame = cap.read()

            if not success:
                break

            frame_count += 1

            # Run detection every 5th frame
            if frame_count % FRAME_SKIP == 0:

                workers = detect_frame(frame)

                last_workers = workers

                current_violation = False
                violation_messages = []

                for index, worker in enumerate(workers, start=1):

                    risk = predict_risk(
                        helmet=int(worker["helmet"]),
                        vest=int(worker["vest"]),
                        gloves=int(worker["gloves"]),
                        safety_shoes=int(worker["boots"]),
                        accident=0
                    )

                    worker["risk"] = risk

                    missing = get_violation(worker)

                    if missing:

                        current_violation = True

                        violation_messages.append(
                            f"Worker {index}: Missing "
                            + ", ".join(missing)
                            + f" | Risk: {risk}"
                        )

                # --------------------------------
                # NEW VIOLATION DETECTED
                # --------------------------------

                if current_violation and not violation_active:

                    print("\n🚨 PPE VIOLATION DETECTED!")

                    for message in violation_messages:
                        print("   " + message)

                    print()

                    os.system(
                        "afplay sounds/mixkit-emergency-alert-alarm-1007.wav"
                    )

                    for message in violation_messages:
                        save_log(
                            "Video Alert: " + message
                        )

                    violation_active = True

                # --------------------------------
                # VIOLATION HAS ENDED
                # --------------------------------

                elif not current_violation and violation_active:

                    print("✅ PPE violation cleared.\n")

                    violation_active = False

            # Draw latest detection
            for index, worker in enumerate(last_workers, start=1):

                draw_worker(
                    frame,
                    worker,
                    index
                )

            writer.write(frame)

            cv2.imshow(
                "Construction Safety Monitoring",
                frame
            )

            # Q key handling
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q") or key == ord("Q"):
                print("\n🛑 Stopping video monitoring...")
                break

    except KeyboardInterrupt:

        print("\n🛑 Video monitoring stopped by user.")

    finally:

        cap.release()
        writer.release()
        cv2.destroyAllWindows()

        print("\n✅ Video monitoring stopped.")
        print(f"🎥 Output saved to: {OUTPUT_PATH}")
        print(f"📊 Frames processed: {frame_count}")


if __name__ == "__main__":
    main()