# OWASP LLM Top 10 2026 — crosswalk and Hidden Context Exposure

- **Topic ID:** owasp-llm-top10-2026
- **Status:** ADD
- **Next review:** n/a
- **Course change:** lessons/frontier/update-01.md (new lesson F.1); references/standards-map.md (appended 2026 crosswalk section); curriculum/course-outline.md (appended F.1 line + dependency row); _sidebar.md (Frontier updates section). Lab code (labs/lab-26-hidden-context/) PENDING — see below.
- **Candidates:** C-20260926-01

## Summary

OWASP GenAI Security Project released the 2026 LLM Top 10 on 2026-08-03: first edition blending
the practitioner vote (75%) with 6,639 real-incident records (25%). Eight of ten entries moved
(Excessive Agency to LLM03, Improper Output Handling to LLM10, …) and System Prompt Leakage was
renamed and broadened to Hidden Context Exposure (LLM08:2026). The course cites 2025 IDs across
~14 lessons; this adds a crosswalk and a lesson that measures hidden-context leakage per slot.

## Evidence

- https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/ — official release page, fetched 2026-09-27; confirms the 2026 edition and release date 2026-08-03 (full list is in the PDF).
- https://www.helpnetsecurity.com/2026/08/06/owasp-2026-llm-top-10-released/ — independent news coverage; methodology (75/25, 6,639 incidents), scope split to the Agentic Top 10 (via search snippet; page blocked by egress proxy).
- https://www.reversinglabs.com/blog/owasp-top-10-for-llm-apps-excessive-agency , https://securityboulevard.com/2026/09/the-owasp-top-10-for-llm-applications-2026-what-changed-and-why-it-matters/ , https://hackerdna.com/blog/owasp-llm-top-10 , https://zenity.io/blog/how-zenity-implements-the-owasp-top-10-for-llm-applications — independent/vendor summaries; the full 1–10 ordering and 2025→2026 moves agree across them (vendor claims only as to their own coverage).
- https://arxiv.org/abs/2307.06865 — Zhang, Carlini, Ippolito: systematic prompt-extraction measurement underpinning "assume hidden context is discoverable".

## What would change the decision

n/a (added). Revisit if OWASP publishes errata to the 2026 numbering (the crosswalk says to
re-verify against the official PDF).

## Implementation status

Lab `labs/lab-26-hidden-context/` (app with 5 canary-tagged slots, 7 probes, decode-aware
scoring, literal/normalize/keyword filters + credential-out-of-context, crosswalk.py, 8 tests,
network_mode: none compose) was written and its own 8 tests passed on 2026-09-27, but it was
**not committed**: the pre-existing suite `python -m pytest lab/tests labs -q` cannot run
(9 collection errors: `lab/models/shim.py` is missing from the repo because `.gitignore` has
`lab/models/*`; 60 other tests pass). Per protocol, lab code waits for a green suite. The
reference code is embedded in the lesson. Ship the lab once the shim is restored.

## History

- 2026-09-27 — ADD — adopted standard that re-numbers every OWASP ID the course cites and generalizes a taught risk; frontier lesson + crosswalk, lab pending on a green test suite — weekly/2026-W39.md — candidates C-20260926-01
