<div class="prereq">

**Prerequisites.** [05.1 Indirect prompt injection](../module-05/lesson-01.md) (the confused
deputy, the egress allowlist, and its *Advanced extension: egress covert channels*),
[16.1 The agent attack surface](../module-16/lesson-01.md),
[16.2 Agent memory poisoning](../module-16/lesson-02.md),
[17.2 Injection defense by design](../module-17/lesson-02.md) (capability tags and provenance),
[23.1 Defensive engineering](../module-23/lesson-01.md) (detectors, FPR, audit logs),
[26.1 Standards mapping](../module-26/lesson-01.md) and
[F.1 OWASP 2026 crosswalk](update-01.md). No GPU, no network.

**You will learn.** What MITRE **ATT&CK v20** added for AI systems (T1698, T1699, T1700,
T1608.007), how those techniques line up with the ATLAS and OWASP IDs you already use, and how
to build, measure, break and harden a detection analytic for **AI-Enabled Exfiltration** modelled
on the one ATT&CK publishes.

**Why this matters.** ATT&CK is what SOCs, SIEM content and threat-intel reports are organized
around. Prompt injection used to be filed under an AI-specific framework (ATLAS) that most
security operations teams do not use. It is now an Enterprise technique, so your findings will be
triaged, tracked and *detected* under ATT&CK IDs.

</div>

# F.2 · MITRE ATT&CK v20: AI techniques in the enterprise matrix

> **Layer:** CURRENT (ATT&CK v20 released 2026-10-13). **Status of claims:** technique names,
> IDs, mitigations and the existence and shape of the T1700 detection strategy are DOCUMENTED
> (read directly on attack.mitre.org, 2026-10-25). The lab's agent and telemetry are synthetic;
> the detectors are the course's own implementations *modelled on* the published analytic
> description, not MITRE code. The AI-search poisoning research example is EMERGING (one group,
> NDSS 2027).
> **Added:** 2026-10-25 by the weekly curriculum review
> ([research/weekly/2026-W43.md](../../research/weekly/2026-W43.md)).

## Why this matters

You already map findings to ATLAS (26.1) and to OWASP (F.1). Neither is what a security operations
center (SOC) runs on. Their detections, dashboards, purple-team plans and threat-intel reports are
indexed by **ATT&CK** technique IDs. Until v20 the honest answer to "which ATT&CK technique is
prompt injection?" was "none". Analysts filed it under *Command and Scripting Interpreter*, under
*Phishing*, or nowhere. The result was that AI incidents never appeared in coverage heat-maps.

v20 changes that, and it does so with more than labels. **T1700 AI-Enabled Exfiltration** ships
with a **detection strategy** (DET0927). That gives you a concrete, published analytic to implement
and then attack, which is exactly the purple-team cycle this course runs on.

## Learning objectives

By the end you can:

1. Name the four ATT&CK v20 AI techniques and their tactics, and map each one to ATLAS, OWASP
   2026 and the lessons and labs where you built it.
2. Write a finding as an ATT&CK *chain* (T1698 → T1700 → T1567) and explain why tagging happens
   after detection, not instead of it.
3. Implement a DET0927-style correlation analytic over agent telemetry and measure its recall per
   attack variant and its false-positive rate (FPR), with confidence intervals.
4. Break that analytic with three adaptations that cost the attacker almost nothing, then harden
   it with runtime provenance, and state the false-positive price of the fix.
5. Explain why some techniques (T1608.007 AI Result Poisoning; policy-conformant misuse) cannot be
   detected from the target's telemetry, and which control applies instead.

## Prerequisites

- **This course:** 05.1 plus its egress extension (deputy, allowlist, carriers; ATT&CK T1071.004
  is already cited there), 16.1/16.2 (agent tools and memory), 17.2 (provenance and readers,
  taint), 23.1 (detector metrics and audit logs), 26.1 (ATLAS mapping), F.1 (OWASP 2026 IDs).
- **Sibling course:** none beyond what those lessons use. See
  [`curriculum/prerequisite-map.md`](../../curriculum/prerequisite-map.md).

## Concept

**What v20 added (DOCUMENTED, attack.mitre.org).** These are new Enterprise entries that name AI
behaviour directly:

| ATT&CK ID | Name | Tactic | ATLAS analogue | OWASP 2026 | Where you built it |
|---|---|---|---|---|---|
| **T1699** | Direct Prompt Injection | Execution | AML.T0051.000 | LLM01:2026 | 04.1, lab-04 |
| **T1698** | Indirect Prompt Injection | Execution | AML.T0051.001 | LLM01:2026 | 05.1, 06.1, lab-05, lab-06 |
| **T1700** | AI-Enabled Exfiltration | Exfiltration | (Exfiltration tactic) | LLM02:2026, LLM03:2026 | 05.1 + ext., 18.1, lab-05, lab-32 |
| **T1608.007** | Stage Capabilities: AI Result Poisoning | Resource Development | (Resource Development) | LLM07:2026 | 14.1 (by analogy) |

The same release also added *T1685.007 Impair Autonomous Defenses*, which T1698's page names as one
goal of indirect injection, and *T1696 Anti-Automation Evasion*. Neither is AI-model-specific.

What the technique pages say, in brief:

- **T1699 / T1698.** Malicious instructions arrive either through the model's own interface
  (direct) or hidden in content the system retrieves: web pages, documents, email, tickets, code
  (indirect). The listed mitigations are *Execution Prevention* (enforce authorization outside the
  model), *Privileged Account Management*, *User Account Management* (dedicated agent identities;
  prompt content must not change the authorization context), *Restrict File and Directory
  Permissions*, *Network Segmentation* (indirect) and *User Training*. **Neither page lists a
  detection strategy.**
- **T1700.** Direct or indirect injection drives an enterprise AI assistant or agent to move data
  out *through its sanctioned tool connections*, so the agent looks like it is operating normally.
  The data may then leave via ordinary techniques such as **T1567 Exfiltration Over Web Service**.
  Detection strategy **DET0927** describes analytics for this sequence: an AI-associated process
  accesses data outside its authorized scope, then a transfer-capable tool call or execution
  happens, then an outbound connection or successful transfer goes to a destination outside
  authorized data flows.
- **T1608.007.** The attacker stages public web content (fabricated claims, supporting articles,
  apparently independent sources) so that AI search and answer engines retrieve, cite or recommend
  it. ATT&CK states that preventive controls cannot easily mitigate it, and that the detection
  strategy has **no target-side behavioral analytic**: enterprise telemetry cannot reliably tell
  this staging apart from ordinary publishing.

**The analyst's mental model.** ATT&CK describes *adversary behavior*. ATLAS describes behavior
against *AI systems*. OWASP describes *application weaknesses*. One injection-driven leak is
therefore three records that point at the same event: `T1698 → T1700` (what the adversary did),
`AML.T0051.001` (the AI-specific technique) and `LLM01:2026 + LLM03:2026` (the weaknesses that let
it work). A good report carries all three.

## Intuition

A detection analytic is a sentence about telemetry: *"this agent read something it shouldn't, then
handed it to a tool, then the tool sent it somewhere it shouldn't go."* Each clause is a
condition, and each condition is a place where the attacker can make the sentence false while the
data still leaves:

- *"somewhere it shouldn't go"* is false if the data goes to a destination that is allowed.
- *"handed it"* is false if you can no longer recognize it, because it was encoded.
- *"then"* is false if the steps happen in different sessions, joined through memory.

The hardened analytic rewrites the sentence so that it no longer depends on what the attacker
controls. The runtime, not the payload text, records which protected data was in context. The
principal's whole history counts, not one session. The question becomes whether *this data* is
allowed to reach *this destination*, not whether the host is allowlisted.

## Technical explanation

**Telemetry.** The lab emits one event stream per principal (the human whose task the agent runs):
`prompt` (user or retrieved), `read` (resource, label, in-scope?, value, taint id), `memory_write`
and `memory_read`, `tool` (args, taints) and `net` (destination, allowlisted?, destination
clearance, payload, taints). `taints` is what a provenance-aware runtime can record cheaply: the
taint ids of every protected value currently in the agent's context. This is the coarse version of
17.2's capability tags.

**Detectors.**

1. `rule_unauthorized_dest`: alert on any connection to a non-allowlisted destination. This is
   the 05.1 allowlist turned into an alert.
2. `rule_restricted_read`: alert on any read of restricted data.
3. `det0927_content`: the DET0927 sequence inside one session. An out-of-scope read, then a tool
   call whose arguments contain the value, then a non-allowlisted connection whose payload
   contains it.
4. `det_provenance`: across all of a principal's sessions, alert if any outbound event carries a
   taint whose data label ranks above the destination's clearance
   ($\text{public} < \text{internal} < \text{restricted}$).

**Attack families (10 cases each).** A0 is the baseline T1698 → T1700 chain. A1 is a **ride-along**
to a *sanctioned* public file-share (allowlisted), which is the 05.1 extension's carrier idea and
T1700's "sanctioned tool connections". A2 base64-**encodes** the value. A3 **splits** the chain
across sessions through memory (16.2). A4 combines all three. A5 is **policy-conformant misuse**:
internal data the user may read, posted to an internal wiki the policy allows. **Benign families
(40 cases):** B1 summarizes in-scope documents (half of them restricted) and mails them internally.
B2 fetches a public vendor page that is not allowlisted. B3 reads the user's own restricted record
and then fetches an unrelated public page.

**Tagging.** `tag_case` turns an alerted case into a *hypothesis* chain: a retrieved prompt carrying
the inert injection marker gives T1698 (a user prompt gives T1699), a tainted outbound gives T1700,
and a share destination adds T1567. It runs **after** a detector fires. Tagging is not detection: a
case nobody alerted on never gets a tag.

## Mathematics

**The correlation predicate.** For one session with events $e_1,\dots,e_m$, `det0927_content`
fires iff

$$ \exists\, i<j<k:\ \text{read}_i \wedge \neg\text{inScope}_i \wedge \text{tool}_j \wedge v_i \sqsubseteq \text{args}_j
   \wedge \text{net}_k \wedge \neg\text{allow}_k \wedge v_i \sqsubseteq \text{payload}_k , $$

where $v_i$ is the value read at step $i$ and $\sqsubseteq$ means "appears as a substring". Each
conjunct is a lever for the attacker: A1 falsifies $\neg\text{allow}_k$, A2 falsifies
$\sqsubseteq$, and A3 breaks "same session". The provenance analytic replaces all three:

$$ \text{alert} \iff \exists\, \text{net } e,\ \exists\, t \in T(e):\ \text{rank}(\ell(t)) > \text{rank}(c(\text{dest}(e))), $$

where $T(e)$ is the runtime taint set over the principal's whole history (memory reads re-add
taints), $\ell(t)$ is the data label, and $c$ is the destination clearance. The attacker controls
neither $T$ nor $\ell$ nor $c$.

**Zero observed false positives is not $\text{FPR}=0$.** `det0927_content` raises 0 alerts on 40
benign cases. The Wilson 95% upper bound (04.1) for $k=0,\ n=40,\ z=1.96$ is

$$ \frac{\frac{z^2}{2n} + z\sqrt{\frac{z^2}{4n^2}}}{1+\frac{z^2}{n}} = \frac{0.0480 + 0.0480}{1.0960} \approx 0.088 . $$

**Base rates (precision of an alert).** With recall $R$, false-positive rate $F$ and attack
prevalence $\pi$,

$$ \text{PPV} = \frac{R\,\pi}{R\,\pi + F\,(1-\pi)} . $$

Worked numbers at $\pi = 10^{-3}$ (one attacked session in a thousand):

- `det_provenance`: $R=1,\ F=0.25 \Rightarrow \text{PPV} = \frac{0.001}{0.001 + 0.24975} \approx 0.0040$.
  Fewer than 1 alert in 250 is real. At 10,000 agent sessions a day that is about 2,500 alerts.
- `det0927_content` at its FPR *upper bound*: $R=0.2,\ F=0.088 \Rightarrow \text{PPV} \approx
  \frac{0.0002}{0.0002+0.0879} \approx 0.0023$. Its point estimate ($\text{PPV}=1$) is an artifact
  of a small benign set.

Both numbers are the reason a SOC demands high-fidelity correlation, and also the reason "it
fired on the demo" is not evidence.

## Attack / Defense model

<div class="callout red">

**Attack (inert).** T1698: a retrieved ticket carries `[[LAB-INJECTION-MARKER]]`. The scripted
agent then reads `payroll/all` (restricted, out of scope) and sends it out (T1700). Adaptations:
sanctioned destination (A1), base64 (A2), memory split (A3), all three (A4), and stay inside policy
(A5). Success means the synthetic canary reaches an attacker-readable destination.

</div>

<div class="callout blue">

**Defense, in increasing strength:** host-allowlist alert → restricted-read alert → DET0927-style
content correlation → provenance correlation (runtime taints, cross-session, label vs clearance).
After that, prevention instead of detection: 17.2 capability flow control and ATT&CK's own
mitigations (authorization outside the model, dedicated least-privilege agent identities).

</div>

Measured (lab 35, deterministic):

```text
detector                   A0   A1   A2   A3   A4   A5   FPR  [95% CI]
rule_unauthorized_dest    1.0  0.0  1.0  1.0  0.0  0.0  0.50  [0.35, 0.65]
rule_restricted_read      1.0  1.0  1.0  1.0  1.0  0.0  0.50  [0.35, 0.65]
det0927_content           1.0  0.0  0.0  0.0  0.0  0.0  0.00  [0.00, 0.09]
det_provenance            1.0  1.0  1.0  1.0  1.0  0.0  0.25  [0.14, 0.40]
```

<div class="callout guarantee">

**Guarantee analysis: the DET0927-style content correlation.**
- **Guarantees:** it alerts on the *literal* three-step chain inside one session, and observed
  FPR on this benign set is 0 (upper bound 0.09). Every conjunct must hold, which makes it a
  high-fidelity alert.
- **Does NOT guarantee:** detection when any conjunct is falsified. That covers a sanctioned
  destination (A1), any encoding (A2), steps split across sessions (A3), and the combination (A4).
- **How the attacker adapts:** they pick an allowlisted carrier (05.1 extension), base64 the
  data, or wait a session. Each costs the attacker one line.
- **False-positive cost:** very low. **Performance cost:** a per-session scan with substring
  checks, $O(m^2 \cdot |v|)$ in the worst case. That is trivial at agent-session scale.

</div>

<div class="callout guarantee">

**Guarantee analysis: provenance correlation (runtime taints, label vs clearance).**
- **Guarantees:** any outbound event made while protected data was in the agent's context, to a
  destination not cleared for that label, alerts. This holds regardless of encoding, carrier
  allowlisting or session split, *provided the runtime records taints faithfully and memory
  preserves them*.
- **Does NOT guarantee:** anything about flows the label policy permits (A5). It also depends on
  correct labels and clearances, and on a runtime that cannot be bypassed: a tool that leaves
  without emitting a `net` event is invisible.
- **How the attacker adapts:** they stay inside policy (A5), launder through a destination that
  is cleared but readable by them, or attack the taint pipeline itself (a tool that drops
  taints; memory that strips them).
- **False-positive cost:** real and measured. Coarse context taint flags every public fetch made
  after reading restricted data (B3), FPR 0.25. At $\pi=10^{-3}$, PPV ≈ 0.004. Fine-grained
  dataflow taint (Exercise 3) is the fix.
- **Performance cost:** taint bookkeeping in the agent runtime (a set per context, carried
  through memory). Its engineering cost is larger than its runtime cost.

</div>

<div class="callout guarantee">

**Guarantee analysis: the standard itself (an ATT&CK ID as a "mechanism").**
- **Guarantees:** a shared, SOC-native vocabulary. Your AI findings can now appear in coverage
  maps, detection backlogs and CTI next to everything else.
- **Does NOT guarantee:** that a technique is detectable. T1698 and T1699 list no detection
  strategy, and T1608.007's strategy explicitly has no target-side analytic. Having an ID in the
  matrix is not the same as having coverage.
- **How it goes wrong:** teams mark "T1700 covered" after shipping a literal-match rule like
  `det0927_content`. The coverage map turns green while recall against adapted attacks is 0.
  Report recall per adaptation, not a checkmark.
- **Cost:** re-tagging reports and detections; keeping ATLAS/OWASP cross-references in sync.

</div>

<div class="callout purple">

**Research angle.** "Does the published analytic survive adaptive attackers?" is a measurable
question for every new ATT&CK detection strategy. The method is the one you used for jailbreak
defenses in M24: fix the analytic, enumerate cheap adaptations, and report recall per adaptation
with intervals plus FPR on realistic benign traffic. For T1608.007 the open question runs the
other way: what *answer-side* signal (source diversity, citation provenance) could ever detect it?

</div>

## Real-world examples

- **The ATT&CK v20 release itself (DOCUMENTED).** The updates page lists T1698, T1699, T1700 and
  T1608.007 as new in v20 (2026-10-13). Independent security press covered the release within
  days and noted that only T1700 and T1608.007 ship detection strategies.
- **Procedure examples on T1699 (DOCUMENTED by MITRE).** Two campaign entries are attached. In one,
  an adversary claimed to be a security-firm employee doing defensive testing in order to unlock
  restricted operations (role-claim injection, as in 04.1). In the other, file-write operations
  were embedded in prompts to stage scripts.
- **Data voids in web-searching LLMs (EMERGING, research).** Guerra et al. tested three deployed
  LLM web-search products and found attacker content folded into the synthesized answer in 31% of
  conditions. A single attacker-controlled page could be enough. This is the research picture
  behind T1608.007. It is one group's measurement, to appear at NDSS 2027.
- **Exfiltration through sanctioned channels.** The 05.1 extension covers DNS and allowlisted-host
  carriers. T1700 generalizes the point to any connector the agent is allowed to use, which is why
  the lab's A1 uses an *allowlisted* share.

## Code & Practical lab

<div class="lab">

**Lab 35: ATT&CK v20 AI-Enabled Exfiltration detection.** CPU-only, stdlib only (plus the shared
`evalkit` for Wilson intervals), offline, synthetic `LAB-CANARY-*` values, inert injection marker,
no network. Expected runtime: < 1 s. About 60–90 min for the exercises. CPU-only works; no GPU.

Code: [`labs/lab-35-attack-ai-detection/`](../../labs/lab-35-attack-ai-detection/README.md):
`telemetry.py` (events and cases), `detect.py` (four detectors and the ATT&CK tagger), `attack.py`
(purple cycle and metrics), `test_lab35.py` (9 tests), `docker-compose.yml` (`network_mode: none`).

```bash
py labs/lab-35-attack-ai-detection/attack.py
py -m pytest labs/lab-35-attack-ai-detection -q
```

</div>

The two analytics side by side (from `detect.py`):

```python
def det0927_content(case):
    for events in _sessions(case):                       # ONE session at a time
        for i, r in enumerate(events):
            if r.kind != "read" or r.detail["in_scope"]:
                continue
            v = r.detail["value"]
            for j in range(i + 1, len(events)):
                t = events[j]
                if t.kind == "tool" and v in t.detail["args"]:          # literal content match
                    if any(n.kind == "net" and not n.detail["authorized"]   # host allowlist
                           and v in n.detail["payload"] for n in events[j + 1:]):
                        return True
    return False

def det_provenance(case):
    labels = {}
    for e in case.events:                                # whole principal history
        if e.kind == "read" and e.detail["label"] != "public":
            labels[e.detail["taint"]] = e.detail["label"]
        if e.kind == "net":
            clearance = LABEL_RANK[e.detail["clearance"]]
            if any(LABEL_RANK[labels.get(t, "public")] > clearance for t in e.detail["taints"]):
                return True                              # label > clearance: flow violation
    return False
```

Read the table above as a purple-team story. The published-style analytic is precise and almost
useless against an attacker who adapts. The hardened analytic recovers every adapted chain, at a
measured 25% FPR that comes from coarse taint. Nothing in telemetry catches A5, because nothing in
A5 violates the policy. That is an authorization problem (17.2), not a detection problem.

## Exercise

Purple-team cycle: attack → observe → detect → mitigate → retest → adapt → measure.

1. **Reproduce and explain.** Run the lab. For each zero in the `det0927_content` row, name the
   conjunct of the correlation predicate that the attack falsifies.
2. **Tag.** Add a family A6 where the injection marker is in the *user* prompt (T1699) and the
   exfiltration goes to the collector. Confirm that `tag_case` produces `T1699 → T1700` and that
   all four detectors fire on it.
3. **Mitigate the false-positive cost.** Make B3 stop alerting without losing A0–A4 recall.
   <details><summary>Hint</summary>Coarse context taint marks *every* call made after a
   restricted read. What should actually carry the taint?</details>
   <details><summary>Stronger hint</summary>Have the runtime attach to a `tool`/`net` event only the
   taints of values that *flow into its arguments*, as in 17.2's per-argument provenance. B3's
   holiday fetch has no restricted argument.</details>
   <details><summary>Solution sketch</summary>Record `arg_taints` per call: in the generator, set
   them to the taints of the values actually interpolated into `args`/`payload` (for A3/A4, the
   value re-read from memory carries its taint). Make `det_provenance` check `arg_taints`. B3's FPR
   goes to 0 and A0–A4 stay at 1.0. Then state the new residual: an attacker who makes the model
   *paraphrase* the data into a fresh string breaks value-level dataflow unless model outputs that
   depend on tainted inputs inherit the taint, which is exactly CaMeL's design choice and its
   utility cost (17.2).</details>
4. **Adapt again.** Against your fixed detector, write the cheapest A7 that still leaks: a
   paraphrase, or a destination whose clearance is too high, or a tool path that emits no `net`
   event. Measure it, and write the guarantee box line it falsifies.
5. **Standards hygiene.** For lab-05, lab-18 and lab-32 write one line each: ATT&CK chain, ATLAS
   ID, OWASP 2026 ID. Then mark which ones ATT&CK gives you a *detection strategy* for.

## Research paper

**Strom et al., "MITRE ATT&CK: Design and Philosophy" (MITRE, 2018, revised 2020),
[PDF](https://attack.mitre.org/docs/ATTACK_Design_and_Philosophy_March_2020.pdf).** *Why:* it
defines tactics, techniques and procedures and how ATT&CK decides what becomes a technique. It is
the right lens for reading v20's AI entries: a technique describes adversary *behavior* and is
not a vulnerability class. That is why T1700 is a separate entry from T1698 rather than a
consequence of it. *Read:* the sections on the model's structure and on technique criteria. *Skip:*
the matrix-specific history. *Code this after reading:* the tagger in lab 35, extended to emit
tactic names.

**Emerging research for T1608.007:** Guerra, Jobe, Nambiar, Pöpper & Abouzied, "Data-Void
Exploits in Web-Searching LLMs" (to appear at NDSS 2027),
[arXiv:2610.30365](https://arxiv.org/abs/2610.30365). Read for the threat model (a single page in
a data void) and the measurement design across three products and five data-void strategies.
**Foundational for T1698:** [paper 01, Greshake et al.](../../papers/01-greshake-indirect-injection.md).

## Further reading

- ATT&CK updates page (v20): <https://attack.mitre.org/resources/updates/>
- Technique pages: [T1698](https://attack.mitre.org/techniques/T1698/),
  [T1699](https://attack.mitre.org/techniques/T1699/),
  [T1700](https://attack.mitre.org/techniques/T1700/) (includes DET0927),
  [T1608.007](https://attack.mitre.org/techniques/T1608/007/).
- Press summary of the release (commentary, not a primary source):
  [GBHackers](https://gbhackers.com/mitre-attack-v20-ai-techniques/amp/).
- [`references/standards-map.md`](../../references/standards-map.md): the course's ATT&CK v20
  crosswalk section.

## Assessment

<details><summary>Q1. An agent reads a poisoned ticket and then posts payroll data to a sanctioned file-share. Write the ATT&CK chain and its ATLAS/OWASP cross-references.</summary>

`T1698 Indirect Prompt Injection → T1700 AI-Enabled Exfiltration → T1567 Exfiltration Over Web
Service`. The ATLAS analogue is AML.T0051.001. The OWASP weaknesses are LLM01:2026 (injection),
plus LLM03:2026 (excessive agency) and LLM02:2026 (disclosure).

</details>

<details><summary>Q2. Your DET0927-style rule fired on every red-team run and raised no false positives in 40 benign sessions. Is T1700 "covered"?</summary>

No. The red-team runs were the literal chain (A0). Recall against a sanctioned destination,
encoding or a session split is 0 for content correlation. Also, 0/40 false positives only bounds
FPR below about 0.09 (Wilson), which at a 1/1000 base rate allows a PPV as low as about 0.002.
Report recall per adaptation, with intervals.

</details>

<details><summary>Q3. Why does the provenance analytic catch A2 (base64) when content matching cannot?</summary>

It never inspects the payload text. The runtime records which protected values were in context
when the call was made (taints), and the check compares the data label with the destination
clearance. Encoding changes the bytes, not the provenance.

</details>

<details><summary>Q4. Why does no detector catch A5, and what should?</summary>

A5 moves internal data to a destination the policy clears for internal data. No telemetry
condition is violated, so detection has nothing to fire on. The fix is authorization: a per-task
data-flow policy (17.2 capability flow control: this task's outputs may only reach these
readers), and ATT&CK's own mitigation that retrieved content must not change the authorization
context.

</details>

<details><summary>Q5. Why does ATT&CK say T1608.007 has no target-side analytic?</summary>

The adversary's work happens on the public web, before any interaction with your systems, and it
looks like ordinary publishing or SEO. Your telemetry only shows an AI tool retrieving a page,
which is normal. Defenses live on the answer-engine side (source diversity, provenance of
citations) and in user verification, not in enterprise logs.

</details>

## What you should now be able to do

- Map any AI finding to an ATT&CK v20 chain plus ATLAS and OWASP 2026 IDs.
- Implement a published-style correlation analytic and measure recall per adaptation with
  intervals, FPR, and PPV at a realistic base rate.
- Break a content-matching analytic three ways and harden it with runtime provenance, stating the
  false-positive price.
- Say which AI techniques are not detectable from target telemetry and which controls apply.

## Progress checkpoint

```bash
py course.py complete F.2
py course.py next
```

**Next:** return to wherever you are in the main sequence. When you write up a capstone
([projects/capstones.md](../../projects/capstones.md)), tag each finding with its ATT&CK v20
chain as well as its ATLAS and OWASP 2026 IDs.
