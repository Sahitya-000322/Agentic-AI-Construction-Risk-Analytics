from detector import detect_workers, annotate_workers
from alert import check_ppe
from logger import save_log
from alarm import play_alarm
from risk_predictor import predict_risk


image_path = "test_images/test.jpg"

workers = detect_workers(image_path)

print(f"\n👷 Workers detected: {len(workers)}")

for index, worker in enumerate(workers, start=1):

    print(f"\n--- Worker {index} ---")

    risk = predict_risk(
        helmet=int(worker["helmet"]),
        vest=int(worker["vest"]),
        gloves=int(worker["gloves"]),
        safety_shoes=int(worker["boots"]),
        accident=0
    )

    worker["risk"] = risk

    status = check_ppe(worker, risk)

    print(status)

    play_alarm(status)

    save_log(f"Worker {index}: {status}")


# Create annotated image after risk prediction
annotate_workers(
    image_path,
    workers
)