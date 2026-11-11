---
id: "35.1"
module: 35
minutes: 16
practice_minutes: 90
prerequisites: ["16.1", "24.1", "25.1", "32.1"]
objectives:
  - "Explain how an LLM **multi-agent** discovery system (Discovery → Vetting → Exploitation) finds, vets and triages real vulnerabilities, and why the pipeline exists."
  - "Read a discovery system's evaluation the way M24 taught: precision/recall/F1 against ground truth, the ablation that attributes false-positive reduction, and PoC-validation as a triage gate."
  - "Name the **implicit trust error (iTrue)** root cause and the three validation classes (syntactic, semantic, resource-availability) that close it at a trust boundary."
  - "Audit a toy internal-peer message handler against a stated spec rule and write the missing check (uniqueness invariant, mandatory-field presence, bounded allocation)."
  - "Write the guarantee box for an agentic discovery tool, including the governance cost of giving it testbed and code access."
volatility: implementation
sources:
  - title: "Lin, Wang, Li, Dong, Wang — Understanding Implicit Trust Errors in Core Carrier Networks through Multi-Agent Flaw Discovery and Analysis (USENIX Security 2026), arXiv:2607.10315"
    url: https://arxiv.org/abs/2607.10315
  - title: "NVD — CVE-2026-8233 (Dotouch XproUPF, UPF improper access control)"
    url: https://nvd.nist.gov/vuln/detail/CVE-2026-8233
  - title: "3GPP TS 29.244 — Interface between the control plane and the user plane (PFCP)"
    url: https://www.3gpp.org/ftp/Specs/archive/29_series/29.244/
last_verified: "2026-11-11"
---
---
# 35.1 · Agentic vulnerability discovery: the iFinder case study

Agentic systems are now credible vulnerability discoverers, not just assistants — and a security engineer has to evaluate one the way they evaluate any detector. This lesson uses the iFinder / implicit-trust-errors (iTrue) study (USENIX Security 2026) as a worked case: how an LLM multi-agent system found and triaged 84 real flaws in cellular-core code, how to read the numbers behind that claim, and the defensive lesson it keeps pointing at — validate what you receive at every trust boundary, even from an internal peer.

## Why this matters

Two things changed at once. First, the thing being secured: as carrier core networks move from physically isolated hardware to cloud-native deployments, interfaces that used to be "internal" — and therefore implicitly trusted — become reachable, and a component that acts on a peer's message without validating it is now an exposed attack surface. Second, the thing doing the finding: a pattern-guided LLM multi-agent system discovered **84 previously unknown vulnerabilities** across seven open-source 4G/5G cores, of which **83 were confirmed** and **81 assigned CVEs**. You will meet systems like this on both sides of the table — as a tool you run and must evaluate, and as a capability your adversary now has too. Reading its evaluation honestly (M24) is the skill; the defensive root-cause lesson is the payload.

## Learning objectives

1. Explain how an LLM **multi-agent** discovery system (Discovery → Vetting → Exploitation) finds, vets and triages real vulnerabilities, and why the pipeline exists.
2. Read a discovery system's evaluation the way M24 taught: precision/recall/F1 against ground truth, the ablation that attributes false-positive reduction, and PoC-validation as a triage gate.
3. Name the **implicit trust error (iTrue)** root cause and the three validation classes that close it at a trust boundary.
4. Audit a toy internal-peer message handler against a stated spec rule and write the missing check.
5. Write the guarantee box for an agentic discovery tool, including the governance cost of giving it testbed and code access.

## Concept

**What the system is.** iFinder is an LLM multi-agent system built on the Claude Agent SDK; every agent is an LLM session driven by a task prompt and a small tool set (Grep, Glob, Read, plus build/execute), and all agents — and the baseline it is compared against — run on the same model (Claude Opus 4.5). The known-flaw extraction that seeds it used Claude Code. There are no gradients and no custom analyser; the reasoning is the model's, the tools are ordinary code-search and build commands. (Reported detail: a plain **Grep-based** caller search beat AST call-graph construction — the model is better at document search than at driving a call-graph tool.)

**The pipeline.** Four stages communicate through explicit intermediate artifacts (patterns, candidate reports, feasible-candidate reports, prerequisite messages):

1. **Preprocessing.** Distil 22 known GitHub-issue flaws (from Open5GS + free5GC) and the governing 3GPP specs into **six detection patterns**; a human expert reviewed the patterns before use. Each pattern is a triple — `<information element, dangerous operation, missing validation>` — kept protocol- and language-agnostic.
2. **Discovery Agent.** Backward execution-path analysis: start at a risky use of an information element (a copy or dereference driven by a message field), walk the caller chain back to the message handler, and flag the site if the required validation is absent along the way.
3. **Vetting Agent.** The **code-specification cross-check** — the heart of the false-positive story. Map the candidate to its 3GPP procedure, find the handlers of the procedure's prerequisite messages, expand the context, and re-evaluate whether the flaw is still feasible once earlier-state checks are visible.
4. **Exploitation Agent.** Build protocol-compliant messages and a proof-of-concept, run it in a containerised testbed, read the logs, and refine — capped at **five** iterations. A candidate whose PoC never triggers the intended effect is dropped.

**The six pattern families** map to three root-cause classes you can carry to any protocol: *missing syntactic validation* (Malformed Field, Absent Field), *missing semantic validation* (Invalid Value, Invalid State, Invalid Reference), and *missing resource-availability checks* (Resource Exhaustion).

**The root cause it characterises: iTrue.** An *implicit trust error* is a component acting on a message from an internal peer without validating its **format**, its **semantics**, or the **resource availability** the message implies — because the core was historically assumed to be walled off. The study's contribution is naming this as a recurring *specification-to-implementation gap* rather than a pile of isolated bugs.

## Intuition

Think of the three agents as three different jobs you would otherwise give three people. The Discovery Agent is the junior who reads fast and flags everything that *looks* unchecked — high recall, terrible precision, because it only sees a snippet and cannot know a check happened two messages earlier. The Vetting Agent is the senior who knows the protocol: it pulls up the whole procedure and throws out the "flaws" that are actually validated upstream. The Exploitation Agent is the sceptic who refuses to believe anything until it runs — it builds the thing and watches it crash, or quietly deletes the finding. Each stage trades compute for a cleaner signal, and the published ablation is just the handoff from junior to senior to sceptic, measured.

## Technical explanation

**Reading the headline numbers.** Against 22 ground-truth iTrues, the full pipeline scored **precision 75.0%, recall 68.2%, F1 71.4%** (TP 15 / FP 12 / FN 7) and surfaced **21 new** findings alongside. The comparison point is not a naive LLM — it is a **prompt-only baseline that was already fed the six patterns**, which managed precision 28.2%, F1 31.8%. An *unguided* LLM (no patterns) produced severe hallucinations and no usable result. So two separate things carry the result: the patterns (they lift even the baseline) and the multi-agent structure (it roughly doubles F1 on top).

**The ablation is the teaching point.** Where did the false positives go?

| Configuration | FP | New | Precision | Recall | F1 |
|---|---|---|---|---|---|
| Discovery only (DA) | 62 | 21 | 36.7% | 68.2% | 47.7% |
| + Vetting (DA+VA) | 19 | 21 | 65.5% | 68.2% | 66.8% |
| + Exploitation (DA+VA+EA) | 12 | 21 | 75.0% | 68.2% | 71.4% |

Recall never moves (the Discovery Agent fixes what can *ever* be found; downstream stages only prune). The code-specification cross-check removes **62 → 19** false positives, and runtime PoC-validation removes **19 → 12** more. Valid PoCs: **19/22** for the Exploitation Agent versus **8/22** for the baseline. This is exactly an M24 reading: recall is set by the generator, precision is bought by the judges, and a strong judge (here, "does it actually crash the intended site in a testbed?") is what makes the output triage-ready instead of a pile of candidates.

**Cost, so you can size it.** Per target implementation: ~**710 s** and ~**9.8M tokens** (Discovery 280 s / 2.1M, Vetting 230 s / 3.3M, Exploitation 200 s / 4.4M). The paper reports no dollar figure. Note what is *not* claimed: iFinder was **not** compared against fuzzing or static analysis on these targets, so "better than fuzzing" is not a conclusion you may carry out of this study — it is positioned as reaching stateful, logic flaws that crash-oriented fuzzers miss, which is a hypothesis the numbers are consistent with, not a head-to-head result.

**The detection pattern as a reusable artifact.** The triple `<information element, dangerous operation, missing validation>` is worth stealing for your own code reviews of any message-driven system: name the untrusted field, name the dangerous thing done with it, and name the check that should precede it. If the third slot is empty, you have an iTrue.

## Mathematics

Standard detector algebra (M24), stated so you can reproduce the table. With true/false positives and false negatives,

$$ \text{precision}=\frac{TP}{TP+FP},\qquad \text{recall}=\frac{TP}{TP+FN},\qquad F_1=\frac{2\,PR}{P+R}. $$

For the full pipeline, $TP=15,\ FP=12,\ FN=7$ give $P=15/27=0.556$ over *ground-truth-matched* reports — but the paper computes precision over **all** flagged items including confirmed-new ones, so $P = 15/(15+12)\cdot\!$ with the new-but-valid findings counted as true, yielding the reported $0.750$; recall stays $15/22=0.682$ because recall is measured only against the 22 known flaws. The lesson: **precision and recall here have different denominators** — recall against a fixed ground-truth set, precision against everything the tool emits — and conflating them is the classic way to misread a discovery tool.

The ablation isolates each stage's effect as a multiplicative survival of false positives: if $s_{VA}$ and $s_{EA}$ are the fractions of false positives that survive each judge, then $62\cdot s_{VA}=19$ gives $s_{VA}\approx0.31$ and $19\cdot s_{EA}=12$ gives $s_{EA}\approx0.63$. Two independent judges, each removing a different kind of error (context-blind hallucination vs. non-triggering candidate), compound — the same defense-in-depth arithmetic you use for controls, applied to a detector's precision.

## Attack / Defense model

> [!IMPORTANT]
> **Guarantee analysis — an agentic discovery system as a security tool.**
> - **Gives you:** scalable, cross-language, cross-protocol candidate discovery with *attached evidence* (a runtime-validated PoC), and a precision high enough to hand confirmed findings to maintainers — 83/84 confirmed is the real-world proof of the triage quality.
> - **Does NOT give you:** completeness. Coverage is bounded by the seed pattern set (recall 68.2%; seven missed cases were pattern-coverage gaps and long cross-module caller chains the Discovery Agent could not reconstruct). A zero means "not matched by a pattern," never "not present."
> - **Fails when:** the vulnerable logic needs a pattern you did not seed, or feasibility hinges on specification semantics the model misjudges. 12 false positives survived even after PoC-validation, because a PoC that crashes the *wrong* site still "succeeds."
> - **Cost:** ~710 s and ~9.8M tokens per target, plus the governance cost below.
> - **Governance takeaway:** this tool reads source and *executes code in a testbed*. Vetting an agentic security tool before granting it code and testbed access is now part of the job — scope its filesystem and network, run it against your own disposable targets, and treat its output as candidates to confirm, never as a certificate of (in)security.

> [!CAUTION]
> **Root cause and defence — the two impact classes, described at root-cause level only.**
> The study's end-to-end impacts are **denial of service** and **session hijacking**. Both reduce to an implicit trust error, and both are closed by validating the peer's message before acting:
> - **DoS (availability).** Root cause: a mandatory field is absent or a value is malformed, and the handler dereferences or allocates on it, or fires a process-ending assertion. Defence: *syntactic* validation (mandatory-field presence, length/bounds) and *bounded resource allocation with graceful rejection* instead of `assert`-and-die.
> - **Session hijacking (integrity).** Root cause: **missing uniqueness validation of a session/rule identifier** lets a reused identifier override the legitimate forwarding rule. Defence: enforce the **uniqueness invariant** on session and rule identifiers at the handler; reject a duplicate rather than letting precedence sorting silently prefer the newer one.
> This lesson and its lab stay at root cause and defence. No attack construction, payloads, or step-by-step procedure appears here, consistent with the authors withholding exploit-grade PoCs until patches propagate.

> [!NOTE]
> **Standards framing (M32).** Two hats. The *tool* is an agentic system and inherits the OWASP agentic risks (ASI02 tool misuse, ASI05 unexpected code execution — it builds and runs code; `references/standards-map.md`), which is why you sandbox it. The *findings* are classic input-validation and state-validation failures at a trust boundary — the carrier-network cousin of everything M04–M06 and M23 teach about never trusting content you did not validate, here applied to an *internal peer* rather than a user.

## Real-world examples

- **84 findings, 81 CVEs, across seven cores.** Open5GS LTE 30, Open5GS 5G 10, free5GC 14, OAI 5G 11, OAI LTE 7, SD-Core 7, eUPF 5 (discovered), spanning two protocols — GTP-C (37) and PFCP (47). At the time of writing **58 were fixed**. The recurrence across independent codebases in C, C++ and Go is the evidence that iTrue is systemic, not a single project's bug.
- **A named CVE you can verify.** The study names **CVE-2026-8233** (Dotouch XproUPF, UPF improper access control; CVSS 3.1 **4.6 MEDIUM**, `AV:A/AC:H/PR:L/UI:N/S:U/C:L/I:L/A:L`, published 2026-05-10) with a companion DoS **CVE-2026-8232** on the same product. The other ~79 CVEs are real but not individually numbered in the paper. (Note: early press coverage printed CVE IDs that do **not** exist on NVD — always resolve a CVE to its NVD record before citing it.)
- **Confirmed on commercial cores.** The session-hijack root cause (duplicate rule-identifier) was reproduced on two real-world commercial 5G cores; one vendor fixed it (the CVE above), the other was still remediating at publication.

## Code

The lab ships the *defensive* core: a stated spec rule, a toy handler, and a validator that flags the exact gap the Discovery/Vetting agents reason about — missing presence, range, uniqueness, and availability checks on fields taken from an internal-peer message. The shape of a single check, which is the whole lesson in six lines:

```python
def enforce_unique_rule_id(session, incoming_rule_id):
    # Spec invariant: a rule identifier must be unique within a session.
    # Missing this check is the iTrue root cause behind the session-hijack class.
    if incoming_rule_id in session.rule_ids:
        return Reject("duplicate rule id", pattern="invalid_reference")
    session.rule_ids.add(incoming_rule_id)
    return Accept()
```

No packets are sent and nothing is exploited: the lab operates on *parsed message records provided as static fixtures* and asks only "is the required validation present before the dangerous operation?"

## Practical lab

**Lab 35** ([`labs/module-35/`](../../labs/module-35/README.md)) — defensive validation at a trust boundary. CPU-only, stdlib only, offline, no network, no sockets. Expected runtime: < 1 s; ~90 min for the exercise.

```bash
py labs/module-35/audit.py
py -m pytest labs/module-35 -q
```

You get `validator.py` (the reference solution — the six-family validator), `fixtures.py` (benign and malformed/duplicate message *records*, static), `audit.py` (prints the code-vs-spec audit table), and `test_lab35.py`.

## Exercise

Defensive cycle: read the spec rule → audit the handler → find the gap → write the check → prove it rejects the bad record and still accepts the good one → classify it by iTrue family.

1. **Code-vs-spec audit.** For each stated spec rule (mandatory field present; identifier unique within a session; value within range; allocation within capacity), read the matching handler in `exercise.py` and decide whether it enforces the rule. Write a one-line verdict per handler as a `<information element, dangerous operation, missing validation>` triple — empty third slot means a finding.
2. **Write the missing check.** Implement the absent validations so the fixed handler **rejects** each malformed/duplicate record and still **accepts** every benign one. Run `pytest`; the provided tests encode the pass condition.
3. **The uniqueness invariant.** Make the handler enforce "a rule identifier is unique within a session," and in two sentences explain why *rejecting* the duplicate (not sorting by precedence) is what closes the session-hijack class — at root-cause level, no attack steps.
4. **Bounded allocation.** Replace an unbounded allocation / assertion with a capacity check that returns a graceful rejection; show the validator no longer flags `resource_exhaustion` and that no exception is raised on the burst fixture.
5. **Reflection on the ablation.** In a short paragraph, explain why the code-specification cross-check cut false positives from **62 to 19** while leaving recall unchanged — connect it to "a snippet cannot see a check performed in an earlier protocol state," and to the M24 rule that judges buy precision, not recall.

<details><summary>Hint (step 5)</summary>

The Discovery Agent flags a site because the check is not in the lines it is looking at. Many of those are false — the check exists, just upstream, in an earlier message's handler. The Vetting Agent's only job is to *expand the context* to the whole 3GPP procedure and look again; it cannot find a *new* real flaw (so recall is fixed), it can only reclassify a candidate as validated-elsewhere (so precision rises). That is the detector version of "defense in depth": two judges that fail differently.

</details>

**Deliverable.** The completed `validator.py` additions (or `exercise.py` fixes), the per-handler triple audit, the uniqueness and bounded-allocation fixes with passing tests, and the ablation reflection.

## Research paper

**Lin, Wang, Li, Dong & Wang, "Understanding Implicit Trust Errors in Core Carrier Networks through Multi-Agent Flaw Discovery and Analysis" (USENIX Security 2026), [arXiv:2607.10315](https://arxiv.org/abs/2607.10315).** *Why:* the first systematic root-cause study of core-network implementation flaws *and* the first multi-agent system to discover them at scale, with an ablation that cleanly separates where its precision comes from. *Read:* Section 4 (the four agents and the code-specification cross-check), Section 5 (RQ1 detection table and RQ2/RQ3 ablation — this is the M24 content), and Section 6.2 (the two case studies, read for *root cause and defence*, which is all you need). *Reproduce (defensive):* the lab is a miniature of the validation gap the Discovery Agent reasons about. *Limits:* recall is bounded by the seed patterns; no fuzzing/static-analysis head-to-head; exploit-grade PoCs are deliberately withheld. *Artifacts:* Zenodo [20534406](https://zenodo.org/records/20534406), code at [github.com/LinZiyuu/iFinder](https://github.com/LinZiyuu/iFinder) (license is `NOASSERTION` — **not** a standard OSS license; check terms before reuse), findings at [linziyuu.github.io/iFinder-Website](https://linziyuu.github.io/iFinder-Website/).

## Further reading

- 3GPP **TS 29.244** (PFCP), **TS 29.274** (GTPv2-C), **TS 29.281** (GTP-U), and **TS 33.210** (NDS/IP) — the governing specs; NDS/IP mandates IPsec/mutual authentication on internal interfaces, the deployment-level complement to in-handler validation.
- GSMA guidance on GTP firewalls, and zero-trust segmentation of signalling interfaces — never expose core signalling interfaces (N4/PFCP, S5/S8, S11) to untrusted networks; audit cloud configuration continuously.
- [`references/standards-map.md`](../../references/standards-map.md) — OWASP LLM 2026 and Agentic (ASI) crosswalks used in the guarantee boxes above; [25.1](../module-25/lesson-01.md) (automated red teaming) and [24.1](../module-24/lesson-01.md) (evaluation) for the reading discipline applied here.

## What you should now be able to do

- Describe a Discovery → Vetting → Exploitation multi-agent discovery pipeline and what each stage buys.
- Read such a system's evaluation correctly: separate recall (vs ground truth) from precision (vs all output), read the ablation as judges buying precision, and treat a PoC as a triage gate.
- Name the iTrue root cause and close it with syntactic, semantic, and resource-availability validation at a trust boundary — including the uniqueness invariant behind the session-hijack class and bounded allocation behind the DoS class.
- Write a guarantee box for an agentic discovery tool, and say why vetting and sandboxing such a tool before giving it code and testbed access is now part of the work.
