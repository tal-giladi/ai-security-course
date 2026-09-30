import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from supply_chain import (make_malicious_checkpoint, load_with_pickle, marker_was_written,  # noqa: E402
                          clear_marker, save_load_safetensors, Base, make_data, train_base,
                          train_malicious_adapter, clean_acc, backdoor_asr)


def test_pickle_load_executes_embedded_code():
    clear_marker()
    ckpt = Path(tempfile.gettempdir()) / "lab13_test_ckpt.pt"
    make_malicious_checkpoint(ckpt)
    assert not marker_was_written()
    load_with_pickle(ckpt)
    assert marker_was_written(), "pickle.load must execute the embedded __reduce__ payload"
    clear_marker()


def test_safetensors_does_not_execute_code():
    clear_marker()
    m = Base(seed=1)
    x, y = make_data(300, 1)
    train_base(m, x, y, epochs=50)
    _ = save_load_safetensors(m.state_dict())
    assert not marker_was_written(), "safetensors stores tensors only; no code runs"


def test_malicious_adapter_is_a_stealthy_backdoor():
    m = Base(seed=1)
    x, y = make_data(500, 1)
    xte, yte = make_data(500, 2)
    train_base(m, x, y)
    adapter = train_malicious_adapter(m, x, y)
    assert clean_acc(m, xte, yte, adapter) > 0.9, "adapter should preserve clean accuracy (stealth)"
    assert backdoor_asr(m, xte, yte, adapter) > 0.8, "adapter should install a working backdoor"
