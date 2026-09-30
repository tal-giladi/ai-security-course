# Glossary inbox — module 30 (AI infrastructure)

- **Management/admin plane** — a service's control API (load/unload models, submit jobs, reconfigure); unauthenticated + reachable ≈ RCE.
- **Model/inference server** — software serving generations/predictions (e.g. serving stacks with model-load APIs).
- **ML lifecycle services** — experiment trackers, model registries, feature stores; frequent no-auth defaults and file-handling bugs.
- **Cluster/orchestration dashboard** — job scheduler UI; exposed + job submission = cluster RCE (ShadowRay).
- **Path traversal** — escaping an artifact root via ../; fix = resolve-then-confine (safe join).
- **SSRF (server-side request forgery)** — making a server fetch an attacker URL (e.g. cloud instance metadata); fix = destination allowlist.
- **Network exposure control** — bind/segment/gateway; perimeter control, highest leverage (shared factor r across all exploits).
- **Blast radius (container)** — scope of damage from a foothold; bound with least-privilege service accounts, minimal secret mounts, blocked metadata.
- **ShadowRay** — 2024 in-the-wild exploitation of exposed Ray cluster dashboards (CVE-2023-48022).
