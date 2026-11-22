"""Lab 15.2 — the whole purple cycle for the shared-prefix-cache side channel, printed as tables.

    python labs/module-15/prefix_cache/pc_evaluate.py

Offline, standard library only, about 30 s on a laptop CPU. Every number is from the simulator in
``pc_engine.py``; the lesson explains which real systems each row corresponds to.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pc_attacks import advantage, extraction_rate, reuse_fraction  # noqa: E402


def row(*cells):
    print("  ".join(f"{c:>12}" for c in cells))


def main():
    print("1. ATTACK — membership probe on a globally shared cache (advantage = TPR - FPR)")
    row("tokens", "direct", "listener")
    for n in (16, 64, 256, 512):
        row(n, f"{advantage('direct', n):.2f}", f"{advantage('listener', n):.2f}")

    print("\n2. ATTACK — recover LAB-CANARY-NN (1 of 16) from a templated system prompt")
    row("probe", "rate")
    row("direct", f"{extraction_rate('direct'):.2f}")
    row("no suffix", f"{extraction_rate('direct', with_suffix=False):.2f}")
    print("   (chance = 0.06; 'no suffix' guesses only the 16-token canary block)")

    print("\n3. DEFEND — per-tenant salting (vLLM cache_salt pattern), 256-token probe")
    row("probe", "advantage")
    row("direct", f"{advantage('direct', 256, salting='tenant'):.2f}")
    row("listener", f"{advantage('listener', 256, salting='tenant'):.2f}")
    row("extract", f"{extraction_rate('listener', salting='tenant'):.2f}")
    print("   cost: share of prompt tokens served from cache (shared 512-token system prompt)")
    row("workload", "global", "per-tenant")
    row("5 req/tenant", f"{reuse_fraction('global'):.2f}", f"{reuse_fraction('tenant'):.2f}")
    row("1 req/tenant", f"{reuse_fraction('global', tenants=100, requests_per_tenant=1):.2f}",
        f"{reuse_fraction('tenant', tenants=100, requests_per_tenant=1):.2f}")

    print("\n4. ALTERNATIVE DEFENSE — keep sharing, pad only the hit request's reply")
    row("probe", "advantage", "extract")
    row("direct", f"{advantage('direct', 256, hide_hits=True):.2f}",
        f"{extraction_rate('direct', hide_hits=True):.2f}")

    print("\n5. ADAPT — listeners queued behind the probe (the saved time moves them)")
    row("listener", f"{advantage('listener', 256, hide_hits=True):.2f}",
        f"{extraction_rate('listener', hide_hits=True):.2f}")

    print("\n6. RETEST — add random emission delay to every request (step shift is about 6 ms)")
    row("jitter ms", "listener adv", "mean added ms")
    for j in (0, 6, 20, 60):
        row(j, f"{advantage('listener', 256, hide_hits=True, jitter=j):.2f}", f"{j / 2:.0f}")


if __name__ == "__main__":
    main()
