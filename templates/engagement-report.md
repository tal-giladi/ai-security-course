# AI Red-Team Engagement Report — <Engagement name>

> A professional-grade report template for an AI security engagement (the OSAI-style deliverable).
> Fill every section. Keep the executive summary readable by a non-technical stakeholder; keep the
> findings reproducible by an engineer. One finding = one row in the table + one detailed entry.

## 1. Executive summary

- **What was tested:** <systems / AI components in scope, one or two sentences>.
- **Overall risk:** <Critical / High / Medium / Low> — <one-sentence justification>.
- **Headline:** <the single most important thing leadership must know>.
- **Objectives achieved:** <e.g. "captured both target canaries via a recon → foothold → agent-memory chain">.

## 2. Scope & rules of engagement

- **In scope:** <hosts, apps, AI components, accounts>.
- **Out of scope:** <explicitly excluded systems / actions>.
- **Windows & constraints:** <timeframe, rate limits, data-handling rules, no-destructive-actions clause>.
- **Authorisation:** <who authorised, when>. **Safety:** synthetic canaries only; no real data exfiltrated.

## 3. Methodology

Map the engagement to a named lifecycle and taxonomy (red-team lifecycle + MITRE ATLAS).

| Phase | Actions taken | ATLAS technique(s) |
|---|---|---|
| Reconnaissance | <what you mapped, passive vs active> | <AML.T…> |
| Initial access / foothold | <exploited exposure> | <AML.T…> |
| Execution / lateral movement | <chaining, agent/RAG/memory abuse> | <AML.T…> |
| Objective / impact | <what was achieved> | <AML.T…> |

## 4. Findings

Ranked most-severe first. Severity = impact × likelihood; state both.

| ID | Title | Severity | Affected component | Status |
|---|---|---|---|---|
| F1 | <title> | <Crit/High/Med/Low> | <component> | <Open/Fixed> |
| F2 | … | … | … | … |

### F1 — <title>  (<severity>)

- **Summary:** <one sentence: the defect>.
- **Impact:** <what an attacker gains; tie to a business consequence>.
- **Likelihood / preconditions:** <reachability, auth, what the attacker needs>.
- **Reproduction:** <exact, ordered steps; commands/requests; the synthetic marker observed>.
- **Evidence:** <canary captured, log line, screenshot reference — synthetic only>.
- **Root cause:** <the real cause, not the symptom>.
- **Remediation:** <specific fix> — **and the guarantee analysis:** what the fix guarantees / what it does NOT / how an attacker adapts / false-positive cost / performance cost.
- **Mapping:** <ATLAS technique, OWASP LLM Top 10 item, NIST AI RMF function>.

*(Repeat the block for each finding.)*

## 5. Attack chain narrative

Tell the end-to-end story: how individual findings combined into impact (each single finding may be
lower severity than the chain). A diagram or ordered list of the kill chain, with the one link whose
removal breaks the chain called out.

## 6. Remediation summary & prioritisation

Rank fixes by leverage (which single change removes the most risk / breaks the chain), not by finding
count. Separate quick wins from structural changes.

| Priority | Fix | Findings addressed | Effort | Leverage |
|---|---|---|---|---|
| 1 | <fix> | F1, F3 | <S/M/L> | <why this is highest-leverage> |

## 7. Appendix

- Tooling & versions (with fallbacks used).
- Full request/response logs (synthetic markers).
- Standards crosswalk: OWASP LLM Top 10 / MITRE ATLAS / NIST AI RMF (see `references/standards-map.md`).
