import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tenant import build_store, cross_tenant_leak, answer, ShimModel  # noqa: E402


def test_vulnerable_retriever_leaks_across_tenants():
    leaked, _ = cross_tenant_leak(build_store(), "vuln", ShimModel(seed=9))
    assert leaked, "no-authz retriever should return another tenant's private doc"


def test_prefilter_prevents_cross_tenant_leak():
    leaked, _ = cross_tenant_leak(build_store(), "prefilter", ShimModel(seed=9))
    assert not leaked, "pre-filtering by tenant before ranking must prevent the leak"


def test_postfilter_prevents_leak_but_degrades_availability():
    store, model = build_store(), ShimModel(seed=9)
    leaked, post_ids = cross_tenant_leak(store, "postfilter", model)
    _, pre_ids = cross_tenant_leak(store, "prefilter", model)
    assert not leaked, "post-filter still blocks the leak..."
    assert len(post_ids) < len(pre_ids), "...but crowds out legitimate results (availability bug)"
