"""Acceptance tests for Lab 30. Run: py -m pytest labs/module-30 -q"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import infra
from infra import Service
import infra_lab


def test_vulnerable_service_is_exploitable():
    s = Service("model-server", bind="public")
    assert infra_lab.exploit_admin(s) is True
    assert infra_lab.exploit_traversal(s) is True


def test_hardened_service_blocks_both_attacks():
    h = Service("model-server", bind="localhost", require_auth=True, block_traversal=True)
    assert infra_lab.exploit_admin(h) is False
    assert infra_lab.exploit_traversal(h) is False


def test_hardened_service_still_serves_legitimate_use():
    h = Service("model-server", bind="localhost", require_auth=True, block_traversal=True)
    assert infra_lab.benign_use(h) is True


def test_network_binding_alone_blocks_remote_attacker():
    only_bind = Service("m", bind="localhost")
    assert infra_lab.exploit_admin(only_bind) is False
    assert infra_lab.exploit_traversal(only_bind) is False


def test_auth_alone_stops_admin_but_not_traversal_needs_path_block():
    only_auth = Service("m", bind="public", require_auth=True)
    assert infra_lab.exploit_admin(only_auth) is False       # no token
    assert infra_lab.exploit_traversal(only_auth) is False    # blocked by missing token here too
    only_path = Service("m", bind="public", block_traversal=True)
    assert infra_lab.exploit_traversal(only_path) is False    # path block stops traversal
    assert infra_lab.exploit_admin(only_path) is True         # but admin is still open


def test_secret_is_synthetic_canary_and_outside_artifact_root():
    assert infra.CANARY in infra.VFS["/etc/ai-secrets.env"]
    assert "/etc/ai-secrets.env" not in [p for p in infra.VFS if p.startswith(infra.ARTIFACT_ROOT + "/")]
