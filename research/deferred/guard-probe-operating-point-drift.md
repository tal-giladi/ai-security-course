# Guardrail probes change operating point when the backbone model is updated

- **Topic ID:** guard-probe-operating-point-drift
- **Status:** WAIT
- **Next review:** 2027-01-17
- **Course change:** none
- **Candidates:** C-20261117-01

## Summary

A frozen guard/probe keeps its AUC across backbone updates while its false-positive rate at the shipped threshold drifts by up to 15x; the fix is recalibrating the threshold per backbone version.

## Evidence

- https://arxiv.org/abs/2611.19216 — single preprint, two authors; code link unconfirmed.

## What would change the decision

Confirmed code, or a second group showing AUC-stable / FPR-drift on deployed guard classifiers. Would be a short 24.1 or 23.1 extension (re-measure FPR at the threshold after every model update).

## History

- 2026-11-22 — WAIT — methodologically important and cheap to teach, but single preprint with unconfirmed code; 23.1/24.1 already teach operating-point evaluation, so the delta is small — weekly/2026-W47.md — candidates C-20261117-01
