# Staging — things worth considering

Temporary document for the current week. The daily run appends class **A** and **B**
candidates here (full records); the weekly review evaluates them, archives this content into
`weekly/YYYY-Www.md`, and resets this file. Nothing here is course material.

## Candidates

### C-20261102-01 · Pre-Crime for Agents, at the Last Second: Probing When a Recruited Agent Gives In

- **Class:** B
- **Date discovered:** 2026-11-02
- **Date published:** 2026-10-29
- **Source:** https://arxiv.org/abs/2610.40588 (verified resolves; abstract fetched directly)
- **Organization/researchers:** Leonidas Raghav (sole listed author; no affiliation stated on the page)
- **Category:** detection/monitoring (adjacent: agent-security)
- **What changed:** A pre-generation (not post-hoc output-filter) detector for an agent about to comply with sustained adversarial peer pressure in a multi-agent setting, probing the model's own activations before each call's output is generated rather than classifying text already produced.
- **Technical summary:** Controlled 6-scenario multi-agent setup: a peer agent pressures a target agent for up to 20 rounds to disclose a secret (e.g. a deploy token); the target typically refuses at first, then gives in. A linear probe reads the target's activations at each model call, before generation, to flag the call that will leak. On held-out Qwen3-32B episodes, at a threshold flagging 5% of benign calls the probe catches 82% of leaking calls vs. 26% for a zero-shot LLM-judge monitor; on gpt-oss-20b, a probe on the reasoning trace reaches AUROC 0.91. The authors' own ablations are candid about limits: the probe substantially confounds "about to disclose" with "violates policy" (it also fires on *permitted* disclosures); a bag-of-words classifier trained on the same labeled calls performs nearly as well, so most of the measured gain comes from the labels rather than from reading activations; and the warning is short-range — halting on every alarm would also stop many benign episodes.
- **Why it might matter:** A structurally different detection point than the course's existing output-filter/after-the-fact monitoring content (pre-generation per-call probing vs. classifying produced text), aimed specifically at multi-agent recruitment/collusion pressure — an area the course already tracks as a gap (see Relationship below) and for which it has no probe-monitoring lesson at all yet.
- **Evidence of adoption:** none — single-author preprint, no code stated, no production use.
- **Major organizations using it:** none.
- **Open-source implementation:** none stated on the abstract page.
- **Paper:** https://arxiv.org/abs/2610.40588
- **Code:** none
- **Relationship to existing course material:** adjacent to three existing WAIT topics but mechanism-distinct from each — `agent-oversight-evasion` (agents defeat oversight under pressure; this is a detector, not an attack), `multi-agent-covert-collusion` (peer-agent collusion; this is single-target compliance under peer pressure, not steganographic collusion), and `safety-probe-scaling` (activation-probe monitoring, for which the course has no lesson/placement yet — this paper is a second, independent data point for that same gap). New topic in the registry; not previously logged in any daily file (checked `research.py lookup` + repo-wide grep).
- **Potential course lesson:** none yet — would need the same probe-monitoring placement decision already open on `safety-probe-scaling` (likely a module-23 extension once validated).
- **Confidence:** low — single, unaffiliated author; the authors' own ablations show the result is confounded (fires on permitted disclosures) and is barely ahead of a bag-of-words baseline on the same labels; no code; no independent replication; short-range warning limits practical use.
- **Recommendation:** monitor (WAIT if reviewed). Not mature enough to teach alone; worth citing alongside whichever of `agent-oversight-evasion` / `multi-agent-covert-collusion` / `safety-probe-scaling` next comes up for review, but the disclose-vs-violation confound and the weak margin over a bag-of-words baseline need resolving first, and it needs either released code or independent replication.
