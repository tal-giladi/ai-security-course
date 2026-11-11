# Lab 35 — ATT&CK v20 AI techniques: detecting AI-Enabled Exfiltration (T1700)

**For:** lesson [F.2 · MITRE ATT&CK v20: AI techniques in the enterprise matrix](../../lessons/frontier/update-02.md).
**Time:** < 1 s to run, ~60–90 min with exercises. **Hardware:** CPU, offline, no Docker required.
**Deps:** Python 3.11+, stdlib only (reuses `lab/attack-tools/evalkit.py` for Wilson intervals, unchanged).

> [!WARNING]
> **In-process and synthetic.** The "agent" is a scripted generator of telemetry events; nothing
> binds to a socket or leaves the process. Confidential values are synthetic `LAB-CANARY-...`
> markers, destinations are reserved `*.corp.test` / `*.sink.test` / `*.vendor.test` names, and the
> injected instruction is the inert string `[[LAB-INJECTION-MARKER]]`. Only ever study these
> techniques against systems you are authorised to test.

## Goal

ATT&CK v20 (2026-10-13) names **T1698 Indirect Prompt Injection**, **T1699 Direct Prompt
Injection** and **T1700 AI-Enabled Exfiltration**, and ships a detection strategy for T1700
(DET0927): an AI process accessing data outside its scope, then a transfer-capable tool call, then
an outbound connection to an unauthorized destination. You implement that correlation analytic
over synthetic agent telemetry, measure it, break it with three adaptations an attacker gets for
free, and harden it with runtime provenance — measuring recall *and* false-positive cost at every step.

| File | What it is |
|---|---|
| `telemetry.py` | event model + 40 benign cases (3 families) and 60 attack cases (A0–A5) |
| `detect.py` | 2 per-event rules, the DET0927-style content analytic, the provenance analytic, ATT&CK tagger |
| `attack.py` | purple cycle: recall per family with Wilson CIs, FPR, PPV at a 1/1000 base rate |
| `test_lab35.py` | 9 acceptance tests pinning each guarantee box in F.2 |

## Run

```bash
python labs/lab-35-attack-ai-detection/attack.py
python -m pytest labs/lab-35-attack-ai-detection -q
# or, isolated:  cd labs/lab-35-attack-ai-detection && docker compose up
```

Expected (deterministic, seed 35):

```text
detector                   A0   A1   A2   A3   A4   A5   FPR  [95% CI]
rule_unauthorized_dest    1.0  0.0  1.0  1.0  0.0  0.0  0.50  [0.35, 0.65]
rule_restricted_read      1.0  1.0  1.0  1.0  1.0  0.0  0.50  [0.35, 0.65]
det0927_content           1.0  0.0  0.0  0.0  0.0  0.0  0.00  [0.00, 0.09]
det_provenance            1.0  1.0  1.0  1.0  1.0  0.0  0.25  [0.14, 0.40]
```

## Exercises

See lesson F.2 §Exercise. In short: (1) reproduce the table; (2) explain each zero in the
`det0927_content` row; (3) cut `det_provenance`'s FPR on family B3 without losing A0–A4 recall
(hint: taint what *flows into the call's arguments*, not everything in context); (4) explain why
no detector here catches A5, and which control from 17.2 does; (5) add T1699 cases (injection in
the *user* prompt) and confirm the tagger labels them.

## Reset

Nothing persists; re-run the script.
