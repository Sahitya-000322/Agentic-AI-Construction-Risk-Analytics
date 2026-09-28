import subprocess
from pathlib import Path


BASE = Path(__file__).resolve().parent

RISK_PYTHON = BASE / "risk_test_env" / "bin" / "python"
RISK_WORKER = BASE / "risk_worker.py"


def predict_risk(
    helmet,
    vest,
    gloves,
    safety_shoes,
    accident=0
):

    command = [
        str(RISK_PYTHON),
        str(RISK_WORKER),
        str(int(helmet)),
        str(int(vest)),
        str(int(gloves)),
        str(int(safety_shoes)),
        str(int(accident))
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        raise RuntimeError(
            "Risk model failed:\n" + result.stderr
        )

    return result.stdout.strip()