import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from stego import (make_image, embed_lsb, extract_lsb, strip_lsb, mse,  # noqa: E402
                   pipeline_extract_and_maybe_exfil, PAYLOAD, CANARY)


def test_payload_round_trips_and_is_visually_invisible():
    clean = make_image()
    stego = embed_lsb(clean, PAYLOAD)
    assert extract_lsb(stego) == PAYLOAD
    assert mse(clean, stego) < 1.0, "LSB embedding must be near-imperceptible"


def test_pipeline_exfiltrates_from_stego_image():
    stego = embed_lsb(make_image(), PAYLOAD)
    rec, exfil = pipeline_extract_and_maybe_exfil(stego, defended=False)
    assert CANARY in rec and exfil


def test_lsb_strip_destroys_payload_at_low_visual_cost():
    stego = embed_lsb(make_image(), PAYLOAD)
    rec, exfil = pipeline_extract_and_maybe_exfil(stego, defended=True)
    assert not exfil and CANARY not in rec
    assert mse(stego, strip_lsb(stego)) < 1.0, "stripping the LSB plane is near-imperceptible"
