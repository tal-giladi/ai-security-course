# Curriculum changelog

How the course evolves. Changes happen at most once a week, only when a development clears the
bar in [the weekly review protocol](research/PROTOCOL-weekly.md). New material extends the
existing lessons and labs; it never replaces them. "No curriculum changes this week" is a normal
entry.

## 2026-W43 (2026-10-25)

- **Added** frontier lesson [F.2 · MITRE ATT&CK v20: AI techniques & detecting AI-enabled
  exfiltration](lessons/frontier/update-02.md). ATT&CK v20 (2026-10-13) adds T1698/T1699 (indirect
  and direct prompt injection), T1700 (AI-Enabled Exfiltration, with detection strategy DET0927)
  and T1608.007 (AI Result Poisoning). The lesson crosswalks them to ATLAS, OWASP 2026 and the
  course's labs. The lab builds a DET0927-style correlation analytic, measures recall per attack
  adaptation, FPR and PPV at a realistic base rate, breaks the analytic with a sanctioned-destination
  ride-along, encoding and a session split, and hardens it with runtime provenance at a measured
  false-positive cost. Lab:
  [Lab 35 · ATT&CK v20 AI-enabled exfiltration detection](labs/lab-35-attack-ai-detection/README.md).
  The standards map gained an ATT&CK v20 section. Nothing existing was changed. Review:
  [research/weekly/2026-W43.md](research/weekly/2026-W43.md).

## 2026-W42 (2026-10-18)

- **Added** new lesson [22.2 · Agent skills as a supply-chain trust boundary](lessons/module-22/lesson-02.md)
  — an installed agent skill (metadata + `SKILL.md` prose + bundled scripts) is a new, authentic-but-
  unsafe node in the 22.1 supply-chain graph. Four payload placements the verification gate passes
  (prose; a bundled cache that differs from the inspected source; an under-declared capability; a
  value handed off between two in-scope skills), and the structural controls that close each — a
  scanner, checked-hash loading, runtime capability enforcement, and cross-skill provenance — with ASR
  *and* utility measured at every layer and the provenance false-positive cost shown explicitly. Maps
  to OWASP LLM04:2026 Supply Chain. Lab:
  [Lab 34 · Agent skills as a supply-chain trust boundary](labs/lab-34-skill-supply-chain/README.md).
  Nothing existing was changed. Review: [research/weekly/2026-W42.md](research/weekly/2026-W42.md).

## 2026-W41 (2026-10-11)

- **Added** new lesson [17.2 · Prompt-injection defense by design: plan isolation, capabilities &
  branch steering](lessons/module-17/lesson-02.md) — the Dual LLM pattern (what plan isolation
  guarantees: control-flow integrity), CaMeL-style capability flow control (data-flow bounds, its
  documented blind spots and measured cost), and branch steering against computer-use agents with
  per-branch capability constraints, each with ASR *and* utility measured. Lab:
  [Lab 33 · Capability flow control & branch steering](labs/lab-33-capability-flow/README.md).
  Nothing existing was changed. Review: [research/weekly/2026-W41.md](research/weekly/2026-W41.md).

## 2026-W40 (2026-10-04)

- **Added** advanced extension to [05.1 · Indirect prompt injection](lessons/module-05/lesson-01.md),
  *Egress covert channels* — why an HTTP egress allowlist guards only one carrier, and how DNS
  tunnelling (MITRE ATT&CK T1071.004; OpenAI 2026 sandbox incident; Zenity SalesBleed) and a
  ride-along in a legitimate web-fetch (LLMLeak) bypass it; per-carrier egress control with a
  measured detector FPR/recall and its adaptive bypass. Lab:
  [Lab 32 · Egress covert channels](labs/lab-32-egress-channel/README.md). Nothing existing was
  changed. Review: [research/weekly/2026-W40.md](research/weekly/2026-W40.md).

## 2026-W39 (2026-09-27)

- **Added** [F.1 · OWASP LLM Top 10 2026: crosswalk & hidden-context exposure](lessons/frontier/update-01.md)
  — how every 2025 OWASP ID the course cites maps to the 2026 list, and why "System Prompt
  Leakage" became Hidden Context Exposure, measured per context slot. The 2026 crosswalk is
  appended to the [standards map](references/standards-map.md); nothing existing was changed.
  Lab: [Lab 26 · Hidden context exposure](labs/lab-26-hidden-context/README.md) (shipped the
  same day, after the shared model shim was committed). Review:
  [research/weekly/2026-W39.md](research/weekly/2026-W39.md).

## 2026-09-26 — before the weekly system

- Built the full course (27 modules M00–M26, labs 04–25, capstones, standards map, 16 paper
  reading guides). Added directly during the initial build, before this review process existed;
  future changes flow through the daily/weekly protocols in this folder.
