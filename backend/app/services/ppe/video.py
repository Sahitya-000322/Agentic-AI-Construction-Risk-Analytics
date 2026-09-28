"""Frame-by-frame video PPE processor (ported from teammate ``video_monitor.py``).

Changes vs original:
- No ``cv2.imshow`` / ``waitKey`` / ``VideoWriter`` (illegal in server context).
- Generator API: :func:`iter_video_violations` yields per-sampled-frame results
  so callers (API, CLI, workers) decide what to do with them.
- Detection + risk + violation-tracking composed from the service modules.
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any


def process_frame(
    frame: Any,
    detect_fn=None,
    risk_fn=None,
) -> list[dict]:
    """Detect workers in one frame and attach ``risk`` + ``missing`` fields."""
    from app.services.ppe.alerts import ViolationTracker  # noqa: F401
    from app.services.ppe.detector import detect_workers, missing_ppe

    if detect_fn is None:
        detect_fn = detect_workers
    workers = detect_fn(frame)
    for worker in workers:
        if risk_fn is not None:
            try:
                worker["risk"] = risk_fn(
                    helmet=int(bool(worker.get("helmet"))),
                    vest=int(bool(worker.get("vest"))),
                    gloves=int(bool(worker.get("gloves"))),
                    safety_shoes=int(bool(worker.get("boots"))),
                )
            except Exception:  # noqa: BLE001 — risk is advisory only
                worker["risk"] = "Unknown"
        else:
            worker.setdefault("risk", "Unknown")
        worker["missing"] = missing_ppe(worker)
    return workers


def iter_video_violations(
    video_path: str,
    frame_skip: int = 5,
    max_frames: int | None = None,
    detect_fn=None,
    risk_fn=None,
) -> Iterator[dict]:
    """Yield ``{"frame": n, "workers": [...], "event": ...}`` per sampled frame.

    ``event`` is one of started/ongoing/cleared/clear (see ViolationTracker).

    Raises:
        FileNotFoundError: if the video cannot be opened.
        RuntimeError: if ``opencv-python`` is not installed.
    """
    try:
        import cv2
    except ImportError as e:
        raise RuntimeError(
            "opencv-python is required for video processing. "
            "Install with: pip install -r requirements-ml.txt"
        ) from e

    from app.services.ppe.alerts import ViolationTracker

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise FileNotFoundError(f"Could not open video: {video_path}")
    tracker = ViolationTracker()
    frame_count = 0
    yielded = 0
    try:
        while True:
            success, frame = cap.read()
            if not success:
                break
            frame_count += 1
            if frame_count % frame_skip != 0:
                continue
            workers = process_frame(frame, detect_fn=detect_fn, risk_fn=risk_fn)
            event = tracker.update(any(w["missing"] for w in workers))
            yield {"frame": frame_count, "workers": workers, "event": event}
            yielded += 1
            if max_frames is not None and yielded >= max_frames:
                break
    finally:
        cap.release()
