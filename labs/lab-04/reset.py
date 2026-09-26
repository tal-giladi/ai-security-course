"""Reset Lab 04 state: clear the local sink log."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lab" / "sink"))
from sink import SinkLog  # noqa: E402

if __name__ == "__main__":
    SinkLog().clear()
    print("[reset] sink log cleared")
