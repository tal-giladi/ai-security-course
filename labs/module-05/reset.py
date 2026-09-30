"""Reset Lab 05 state: clear the local sink log."""
import sys
from pathlib import Path

# The Academy ships this lab as a zip: labs/module-NN/ + labs/common/.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "common"))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lab" / "sink"))
from sink import SinkLog  # noqa: E402

if __name__ == "__main__":
    SinkLog().clear()
    print("[reset] sink log cleared")
