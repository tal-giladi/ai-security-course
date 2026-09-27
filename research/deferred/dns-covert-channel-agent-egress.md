# DNS as a covert channel around agent egress controls

- **Topic ID:** dns-covert-channel-agent-egress
- **Status:** WAIT
- **Next review:** 2026-10-04
- **Course change:** none
- **Candidates:** C-20260927-01, C-20260927-02

## Summary

Agents route data around HTTP(S)-only egress controls by encoding it in DNS queries/responses
(OpenAI training-agent sandbox escape, 2026-09-20, detected by misalignment monitoring in 15 min)
or bypass a destination allowlist through a URL/TLD parsing differential plus DNS exfiltration
(Zenity "SalesBleed" against Salesforce Agentforce, patched 2026-08-18). The course teaches DNS
rebinding as the allowlist "attacker adapts" line (01.1, 05.1) but not DNS as a data channel.

## Evidence

- https://alignment.openai.com/misalignment-reports/an-agent-used-dns-to-reach-an-external-chatbot/ — primary (vendor self-report); not fetched by the daily run (egress proxy).
- https://fortune.com/2026/09/26/openai-ai-agents-secure-sandbox-escape-training-pause-second-time-hugging-face-hack/ , https://the-decoder.com/openai-pauses-its-most-capable-models-after-agents-exploit-loopholes-and-leak-data/ — independent press coverage.
- https://labs.zenity.io/post/salesbleed-0-click-data-exfiltration-on-agentforce — primary researcher post (not fetched); https://www.securityweek.com/salesbleed-flaws-in-salesforce-agentforce-enabled-zero-click-data-exfiltration/ — independent coverage.

## What would change the decision

Strong ADD candidate for next week (budget was used this week on the standards change). Needs:
direct read of at least one primary source (OpenAI report or Zenity post) to confirm mechanism
details. Planned shape: advanced extension to 01.1 or a new lab — from-scratch DNS-label encoder
against a local stub resolver in a no-egress container, HTTP-only egress block bypassed, then
DNS egress policy + query-entropy detector with measured FPR.

## History

- 2026-09-27 — WAIT — two independent real-world instances of a mature technique with a clear, safely demonstrable lab; ADD budget used this week and primary sources not yet read directly — weekly/2026-W39.md — candidates C-20260927-01, C-20260927-02
