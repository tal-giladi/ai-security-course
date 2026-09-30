---
id: "27.1"
module: 27
minutes: 22
practice_minutes: 90
prerequisites: ["00.1", "02.2", "16.1"]
objectives:
  - Place reconnaissance in the red-team lifecycle and map it to the MITRE ATLAS Reconnaissance tactic (AML.TA0002).
  - Enumerate and map an organization's AI applications, ML components, model infrastructure, and dependencies from passive OSINT and active probing.
  - Fingerprint a deployed model and its serving stack from behavioral and protocol signals without privileged access.
  - Quantify recon completeness and detection risk, and design low-and-slow probing that stays under a defender's alerting thresholds.
  - Build the blue-team side: detect scanning, deny discovery, and reason about what each control does and does not guarantee.
volatility: implementation
sources:
  - title: "MITRE ATLAS — Reconnaissance tactic (AML.TA0002) and techniques"
    url: https://atlas.mitre.org/tactics/AML.TA0002
  - title: "OWASP Top 10 for LLM Applications 2025 — LLM07 System Prompt Leakage, LLM02 Sensitive Information Disclosure"
    url: https://genai.owasp.org/llm-top-10/
  - title: "Cisco Talos / blogs.cisco.com — Detecting exposed LLM servers with Shodan: a case study on Ollama"
    url: https://blogs.cisco.com/security/detecting-exposed-llm-servers-shodan-case-study-on-ollama
  - title: "Wiz — ShadowRay: exposed Ray dashboards and the AI compute attack surface (CVE-2023-48022 and follow-ups)"
    url: https://www.wiz.io/blog/shadowray-attack-ai-workloads-actively-exploited-in-the-wild
last_verified: "2026-09-30"
---

# 27.1 · Reconnaissance for AI targets

Before an attacker touches a single payload, they build a map: which AI applications the target runs, what models sit behind them, where the inference and training infrastructure lives, what open-source components it depends on, and which of those are reachable. Reconnaissance is the phase that decides whether the rest of the engagement is a guided strike or a blind flail — and done well, it happens without the defender ever seeing a single alert.

## Why this matters

Every attack you have built in this course assumed a target you already understood: you knew it was a RAG pipeline (M14), an agent with these tools (M16), an MCP client with those servers (M19). Recon is how that knowledge is *acquired* against a real organization that did not hand you an architecture diagram. Get it wrong and you waste your budget attacking a model that is not there, trip a canary on your first probe, and burn the engagement. Get it right and you arrive at the exploitation phase with an asset inventory, a model fingerprint, and a list of exposed services — while the defender's logs show nothing but ordinary traffic.

Recon is also the cheapest phase to *defend*, and the one defenders most often ignore. An Ollama instance with no authentication on port 11434, a Ray dashboard open on 8265, a model card on Hugging Face that names your internal architecture and training set — each is a gift the target gave away for free. The blue-team half of this lesson is about not giving those gifts, and about noticing when someone is collecting them.

## Learning objectives

1. Situate reconnaissance in the red-team lifecycle and the **MITRE ATLAS Reconnaissance tactic (AML.TA0002)**, mapping each activity to a technique ID.
2. Run **passive OSINT** against an AI target: research materials, model cards, code repositories, job posts, and web assets — leaving no trace on the target.
3. Run **active discovery**: fingerprint the served model and stack, enumerate exposed AI services and endpoints, and map dependencies.
4. Measure **recon completeness** (assets discovered / assets present) against **detection risk** (probability a defender alerts), and tune **low-and-slow** probing to trade one for the other.
5. Implement the **defensive** side — deny discovery, detect scanning — and write the guarantee analysis for each control.

## Concept

### Recon in the red-team lifecycle

A red-team (or realistic adversary) engagement runs roughly: **reconnaissance → resource development → initial access → execution → persistence → exfiltration → impact**. ATLAS mirrors ATT&CK's kill-chain structure for AI systems, and its first tactic is **Reconnaissance (AML.TA0002)**: "the adversary is trying to gather information about the AI system they can use to plan future operations." The output of recon is not an exploit; it is a *target model* — a description precise enough that the next phase can be planned, budgeted, and tailored.

Recon splits into two modes with very different detection profiles:

- **Passive** — collecting information the target *published* or that lives in third-party systems (arXiv, Hugging Face, GitHub, PyPI, LinkedIn, Shodan/Censys scan data, DNS records). You never touch the target's own systems, so there is nothing for the target to log. This is almost always the right place to start.
- **Active** — sending traffic to the target's own systems: port scans, endpoint probes, crafted inference requests to fingerprint the model. This is where you learn the most and where you can get caught.

The discipline is to extract every drop from passive sources first, form hypotheses, and let active probing *confirm* a small number of specific questions rather than blindly sweep.

### The AI recon target: four layers

For an AI target, map four layers:

1. **Applications** — the user-facing surfaces that call a model: chatbots, copilots, search, summarizers, agents. Discovered from the product itself, marketing, and JavaScript bundles.
2. **ML components** — the model(s), tokenizer, prompt templates, RAG index, tools/functions, guardrail classifiers. Discovered by fingerprinting and by system-prompt leakage.
3. **Model infrastructure** — the serving stack (vLLM, TGI, Triton, Ollama, TensorFlow Serving, SageMaker, Bedrock, cloud LLM APIs), orchestration (Ray, Kubernetes, KServe), and registries (Hugging Face, MLflow, internal). Discovered by active scanning and fingerprinting default endpoints.
4. **Dependencies & supply chain** — the open-source models, adapters, datasets, and packages the system pulls in (M13, M22). Discovered from repos, `requirements.txt`, lockfiles, SBOMs, and model IDs leaked in errors or headers.

### ATLAS reconnaissance techniques (map your activity)

> [!NOTE]
> **Purple team / research.** The value of naming the technique is shared vocabulary: the red-teamer's report says "AML.T0000 via arXiv" and the blue-teamer knows exactly which sensor should have fired. Map every recon action to a technique.

Under AML.TA0002, the techniques most relevant to an AI target are (names per the ATLAS knowledge base; CURRENT as of 2026-09):

- **AML.T0000 — Search for Victim's Publicly Available Research Materials** (sub-techniques: journals & conference proceedings, pre-print repositories, technical blogs). What models and methods does the org publish?
- **AML.T0001 — Search for Publicly Available Adversarial Vulnerability Analysis.** Has someone already documented how to break this model family?
- **AML.T0003 — Search Victim-Owned Websites.** Product pages, docs, status pages, `robots.txt`, JS bundles.
- **AML.T0004 — Search Application Repositories.** GitHub, package registries, container registries, model hubs.
- **AML.T0006 — Active Scanning.** Direct probing: open ports, AI-related services, and behavioral fingerprinting. Recent ATLAS guidance even includes sending email to org addresses to detect *AI agents managing inboxes*.
- **AML.T0064 — Gather RAG-Indexed Targets** *(EMERGING).* Identify documents/sites a target's RAG pipeline ingests, so you can later poison them (M14). Its appearance in ATLAS reflects how central RAG has become to real deployments.

## Intuition

Reconnaissance is casing a building, not breaking in. The passive phase is everything you can learn from the sidewalk: the company sign, the delivery trucks, the job ad for "someone to run the loading dock," the architectural plans filed with the city. You learn the layout, the vendors, the shift changes — and no camera ever sees you, because you never crossed the property line. Only after you know where the doors are do you walk up and *gently* test one handle, once, at a time when a rattling handle looks like an ordinary passer-by.

The amateur does the opposite: walks straight up and yanks every door and window in sequence at 3 a.m. That is a port scan across every AI service at full speed. It works — you will find the unlocked door — but the guard now knows someone is hunting, and the good targets get locked before you return. For AI targets specifically, the "cameras" include prompt canaries (M14), rate anomaly detectors, WAFs tuned for jailbreak strings, and honeytokens salted into system prompts and documents. The whole art of stealthy recon is maximizing what you learn per unit of suspicion you generate.

## Technical explanation

### Passive OSINT sources for AI targets

| Source | Technique | What it yields |
|---|---|---|
| arXiv / conference papers / tech blog | AML.T0000 | Model architecture, training data, methods the org uses internally |
| Hugging Face org page, model cards | AML.T0004 | Exact model IDs, base models, fine-tune lineage, licenses, eval numbers |
| GitHub / GitLab (org + employees) | AML.T0004 | `requirements.txt`, prompts, config, API shapes, endpoints in code |
| PyPI / npm / container registries | AML.T0004 | Dependency versions → known CVEs (M22) |
| Job postings / LinkedIn | AML.T0000/T0003 | "Experience with vLLM, Ray, Pinecone" names the stack for free |
| Shodan / Censys / ZoomEye | (passive re-use of others' scans) | Exposed Ollama/Ray/Triton/Gradio instances, ports, banners |
| DNS / certificate transparency | AML.T0003 | `api.`, `llm.`, `chat.`, `ml.` subdomains → service inventory |
| The product's own JS bundle | AML.T0003 | API base URLs, model names, feature flags, sometimes keys |

Shodan/Censys deserve emphasis: they scan the whole internet continuously, so querying *their* index for a target's IP ranges is passive from the target's point of view. This is how researchers found large numbers of unauthenticated Ollama servers (default port 11434, no built-in auth) and exposed Ray dashboards (port 8265) — see Real-world examples.

### Active discovery and fingerprinting

Once passive work has produced hypotheses, active probing confirms them. Key methods:

- **Service/port enumeration.** AI stacks have well-known default ports and endpoints: Ollama `:11434/api/tags`, vLLM/TGI/OpenAI-compatible `/v1/models` and `/v1/chat/completions`, Triton `:8000/v2/health/ready` and `/v2/models`, TensorFlow Serving `:8501/v1/models/<name>/metadata`, Ray dashboard `:8265`, Gradio/Streamlit banners, MLflow `:5000`. A single request to a default health or metadata endpoint often names the model and version.
- **Model fingerprinting.** Even a black-box chat endpoint leaks identity:
  - *Tokenizer / BPE artifacts* — how the model splits rare strings, handles emoji or repeated whitespace, and its exact context-length error message narrow the family.
  - *System-prompt leakage* (OWASP **LLM07**) — a well-crafted request can make the model recite its instructions, revealing the template, tools, guardrails, and sometimes secrets.
  - *Behavioral signatures* — refusal phrasing, canned disclaimers, knowledge cutoff, self-identification ("I am …"), and characteristic formatting are strong family/provider signals.
  - *Protocol tells* — response headers (`server:`, `x-*` model or region headers), streaming format (SSE vs chunked), error schemas, and rate-limit headers fingerprint the serving layer.
- **Dependency mapping.** Model IDs in errors/headers, `/v1/models` output, and leaked config map the served model back to a Hugging Face lineage and a dependency set you can check for known issues (M13/M22).

> [!CAUTION]
> **Red team.** The cheapest high-value probe is often a single request to a default metadata endpoint (`/v1/models`, `/api/tags`, `/v2/models`) — it is indistinguishable from a health check, yet it can hand you the exact model name and version. Spend one quiet request there before you ever craft a jailbreak.

### Stealth: staying under the threshold

Active recon is detectable; the goal is to keep detection probability low while covering the asset space. Levers:

- **Volume & rate.** Bursty, high-rate probing lights up rate anomaly detectors. Spread probes over time (low-and-slow).
- **Distribution.** Rotate source IPs/sessions so no single origin accumulates a suspicious pattern.
- **Blend.** Make probes look like ordinary traffic (health checks, normal chat) rather than scanner signatures.
- **Avoid tripwires.** Do not echo or exfiltrate canary/honeytoken strings; do not send known jailbreak payloads during recon — those are exactly what WAFs and prompt firewalls are tuned to catch. Recon is about *identity*, not exploitation; save the payloads for later.
- **Prefer passive.** Every question you answer from Shodan or a model card is a question you never had to ask the target.

> [!TIP]
> **Blue team.** You cannot stop passive OSINT (you already published it), but you *can* deny active discovery cheaply: authenticate every AI endpoint, disable default metadata/health endpoints on the public interface, strip version/model banners and identifying headers, return generic errors, never bind Ollama/Ray/Triton/MLflow to a public interface, and salt system prompts and RAG corpora with honeytokens so any leakage is *attributable*. Then alert on scanning patterns (endpoint fan-out, fingerprinting bursts, metadata-endpoint hits from non-infra sources).

## Mathematics

Model recon as covering a set of assets while accumulating suspicion.

**Completeness.** Let $A$ be the set of discoverable assets present in the target and $D \subseteq A$ the set you discover. Recon **completeness** is

$$ \text{Cov} = \frac{|D|}{|A|}. $$

**Per-probe detection.** Suppose each active probe $i$ is independently detected with probability $p_i$ (a function of its rate, its signature, and whether it hits a tripwire). If a defender's alert fires when *any* probe is detected, the probability of being flagged after $n$ probes is

$$ P_{\text{detect}} = 1 - \prod_{i=1}^{n} (1 - p_i). $$

With a uniform per-probe risk $p$, this is $1-(1-p)^n$, which rises fast: even $p=0.02$ gives $\approx 0.64$ after $n=50$ probes. Two consequences: (1) **passive discovery is free** ($p_i=0$), so maximize $|D|$ from passive sources before any probe; (2) **fewer, higher-yield probes win** — a single metadata-endpoint hit that reveals many assets has tiny $n$ and thus tiny $P_{\text{detect}}$, versus sweeping every path.

**Low-and-slow vs a rate detector.** A common detector flags when probe count in a sliding window $W$ exceeds threshold $\tau$. If you emit probes at rate $r$ (probes per unit time), you avoid the burst rule when $rW < \tau$, i.e. $r < \tau / W$. Slowing $r$ trades *time-to-complete* $\approx |A|/r$ for stealth. But a smarter defender does not count volume; it measures **coverage/entropy** — how many *distinct* AI endpoints a source touches — which low-and-slow does not reduce. That is the adaptive move you will implement in the lab: detect the *shape* of recon, not its speed.

**The red-teamer's objective.** Choose a probe plan to maximize expected discovered value subject to a suspicion budget $B$:

$$ \max_{\text{plan}} \; \mathbb{E}[\text{value}(D)] \quad \text{s.t.} \quad \sum_i p_i \le B. $$

This is why "passive first, then a few surgical probes" is optimal: it puts the mass of $|D|$ on zero-cost sources and spends the tiny budget only where active confirmation is required.

## Attack / Defense model

> [!IMPORTANT]
> **Guarantee analysis — denying active AI-service discovery (auth + disabled metadata endpoints + banner/header scrubbing + generic errors).**
> - **What it guarantees:** an unauthenticated or unauthorized active prober cannot enumerate models via default metadata/health endpoints, cannot read version/model banners, and cannot distinguish services by error schema — raising the number and specificity of probes needed and thus $P_{\text{detect}}$.
> - **What it does NOT guarantee:** it does nothing against passive OSINT (papers, model cards, repos, Shodan data on *already-exposed* hosts), and it does not stop **behavioral** fingerprinting of a *legitimately reachable* model (refusal style, tokenizer tells, knowledge cutoff) — an authorized user of your chatbot can still fingerprint it.
> - **How an attacker adapts:** shift to passive sources; fingerprint behaviorally through the sanctioned chat path; go low-and-slow to stay under rate rules; use others' scan data instead of scanning.
> - **False-positive cost:** internal health checks and monitoring may hit the same endpoints; over-aggressive scrubbing can break legitimate client SDKs that read model metadata.
> - **Performance cost:** authentication and header scrubbing add negligible latency; the real cost is operational (inventory of endpoints, config discipline across every service).

> [!IMPORTANT]
> **Guarantee analysis — scanning detection (rate + coverage/entropy anomaly alerting on AI endpoints).**
> - **What it guarantees:** a high-rate or high-fan-out prober from a single origin is flagged; metadata-endpoint hits from non-infrastructure sources are surfaced for review.
> - **What it does NOT guarantee:** a low-and-slow, IP-rotated, blend-with-normal-traffic prober can stay below any *volume* threshold; passive recon produces no events at all; a determined adversary distributed across many origins defeats per-source entropy.
> - **How an attacker adapts:** slow the rate under $\tau/W$, rotate sources, mimic health-check traffic, and prefer passive sources.
> - **False-positive cost:** security scanners, uptime monitors, and curious users trigger alerts; tuning $\tau$ down raises noise, tuning it up raises misses.
> - **Performance cost:** logging and windowed aggregation across AI endpoints; modest storage and stream-processing load.

## Real-world examples

- **Unauthenticated Ollama at internet scale (CURRENT, DOCUMENTED).** Ollama ships with **no built-in authentication** and a default port of **11434**. Security researchers using Shodan/Censys have repeatedly found large populations of exposed instances (reports through 2026 range from thousands to six figures depending on the crawl). The unauthenticated surface includes `POST /api/pull` (pull any model), `POST /api/generate`/`/api/chat` (run inference on the owner's GPU at the owner's expense), and model creation/deletion. Pure recon — a Shodan query and one `/api/tags` request — inventories a victim's local models. (Sources: Cisco/Talos Shodan case study; multiple exposure reports.)
- **ShadowRay — exposed Ray dashboards (CURRENT, DOCUMENTED).** Ray's dashboard/Jobs API (default port **8265**) is unauthenticated by design in the default configuration; Wiz documented in-the-wild exploitation (tracked under CVE-2023-48022 and later Ray CVEs) where attackers who *found* exposed dashboards submitted jobs that ran arbitrary code on GPU clusters. The find-it step is reconnaissance; the exploitation is a separate phase — but the exposure was discoverable by anyone scanning for port 8265.
- **System-prompt leakage as recon (CURRENT).** OWASP added **LLM07: System Prompt Leakage** to the 2025 Top 10 precisely because deployed apps routinely reveal their instructions, tool lists, and even embedded secrets when prompted. For a red-teamer this is a recon jackpot: the leaked prompt hands you the app's ML-component map (tools, guardrails, template) without any infrastructure access.
- **Model cards and papers as a stack map (FOUNDATIONAL).** An org's Hugging Face page and published papers frequently name the exact base model, fine-tune data, and serving choices — AML.T0000/T0004 with zero probes.

## Code

A compact black-box fingerprinter: it sends a few *benign, non-payload* probes to a chat endpoint and scores which model family the responses are most consistent with. This is identity-only recon — no jailbreak strings, no canary echoing. It is a from-scratch sketch of the behavioral-fingerprinting idea the lab builds out.

```python
# fingerprint.py — behavioral model fingerprinting from benign probes (identity only).
# Sends ordinary questions; scores the response against per-family signatures.
from dataclasses import dataclass

@dataclass
class Signature:
    family: str
    self_id: list[str]        # phrases the model uses to name itself
    refusal_markers: list[str]
    cutoff_hint: str          # a year it tends to cite as its knowledge cutoff

SIGNATURES = [
    Signature("family-A", ["i'm an ai assistant made by"], ["i can't help with that"], "2024"),
    Signature("family-B", ["i am a large language model"], ["i'm unable to provide"], "2023"),
]

BENIGN_PROBES = [
    "In one sentence, who made you and what are you?",
    "What is your knowledge cutoff, if you have one?",
    "Politely decline to do something trivial and show your exact wording.",
]

def score(responses: list[str], sig: Signature) -> int:
    text = " ".join(r.lower() for r in responses)
    s = 0
    s += sum(2 for p in sig.self_id if p in text)
    s += sum(1 for p in sig.refusal_markers if p in text)
    s += 1 if sig.cutoff_hint in text else 0
    return s

def fingerprint(ask) -> tuple[str, dict]:
    """`ask(prompt) -> response_text`. Returns (best_family, all_scores)."""
    responses = [ask(p) for p in BENIGN_PROBES]      # few probes => low P_detect
    scores = {sig.family: score(responses, sig) for sig in SIGNATURES}
    best = max(scores, key=scores.get)
    return best, scores
```

The point is that **three benign questions** — not fifty jailbreak attempts — are enough to shrink the hypothesis space, keeping $n$ (and therefore $P_{\text{detect}}$) tiny. The lab replaces this stub with a mock target that also exposes infrastructure endpoints, and adds the detector that tries to catch the probing.

## Practical lab

> [!WARNING]
> **Lab.** Module 27 lab (`../../labs/module-27/`). CPU-only, offline, **no Docker required** (optional compose provided). Runtime ~5–10 min. **Local-only scope:** the "target" is a set of in-process mock AI services we ship — an Ollama-like host, an OpenAI-compatible server, a Gradio-like app, and a chat model — each seeded with synthetic canaries (`LAB-CANARY-<id>`). The recon engine only ever talks to these in-process mocks; **nothing binds to a public interface and nothing scans any real host.** You run the full purple cycle: recon → observe → detect → mitigate → retest → adapt → measure, and the lab prints completeness, detection rate, false positives, and probe cost.

The lab (`labs/module-27/recon_lab.py`) ships:

- `mock_target.py` — a mini "org" exposing the four layers: default metadata/health endpoints, banners/headers, a chat model with a leakable system prompt, and dependency strings — in **vulnerable** and **hardened** configurations.
- `recon.py` — a passive collector (reads published "OSINT" fixtures) and an active prober/fingerprinter that builds an **asset inventory** and computes **completeness**.
- `detector.py` — a **rate** detector and an adaptive **coverage/entropy** detector.
- The driver runs: (1) noisy recon on the vulnerable target → high completeness, high detection; (2) hardened target → low completeness for active, passive still works; (3) low-and-slow recon evading the rate detector; (4) the coverage detector catching low-and-slow anyway; (5) the attacker adapting (distributed sources) and the final measured trade-off table.

```bash
py labs/module-27/recon_lab.py
py -m pytest labs/module-27 -q
```

## Exercise

Attacks: construct → execute → analyze → measure. Defenses: implement → then bypass your own defense.

1. **Passive-only inventory.** Using only the OSINT fixtures (no probes), build the asset map and compute completeness. Which layers can you fully resolve passively? Show that infrastructure ports and the exact served model usually need *one* active probe each.
2. **Surgical fingerprinting.** Fingerprint the served model using the fewest probes that reach a confident family guess. Plot probes ($n$) vs detection probability ($1-(1-p)^n$) and vs confidence. Find the knee.
3. **Harden and re-measure.** Turn on the hardened target (auth, disabled metadata endpoints, scrubbed banners, generic errors). Recompute active completeness; confirm passive completeness is unchanged. Write both guarantee boxes in your own words.
4. **Low-and-slow.** Tune the prober's rate $r$ below the rate detector's $\tau/W$. Show detection by the rate detector drops to ~0 while completeness stays high but time-to-complete grows. Report the trade.
5. **Adaptive purple cycle.** Switch on the coverage/entropy detector and show it catches the low-and-slow prober (fan-out is unchanged by slowing down). Then adapt the attacker (distribute probes across mock sources) and measure how much distribution is needed to evade it. Produce the final `completeness × detection-rate × false-positives × probes` table and state which single defense bought the most stealth-denial per unit of functionality lost.

<details><summary>Hint (step 5)</summary>

Slowing the rate changes *when* probes arrive, not *how many distinct endpoints one source touches*. The coverage detector keys on the number of distinct AI endpoints/services a source fingerprints in a session, so low-and-slow does not help against it. Distributing across sources lowers per-source fan-out — but each source still needs to touch enough to be useful, so there is a floor on how few endpoints per source you can manage while keeping aggregate completeness high. Measure that floor.

</details>

**Deliverable.** The passive inventory and completeness, the probes-vs-detection knee, the hardened re-measurement with both guarantee boxes, the low-and-slow trade, and the adaptive-detector purple-cycle table with your verdict on the highest-leverage defense.

## Research paper

**Primary read — MITRE ATLAS Reconnaissance tactic (AML.TA0002) and its techniques.** *Why:* it is the industry-standard taxonomy for exactly what you built — a named technique for each recon action, plus real case studies. *Read:* the tactic description and techniques AML.T0000, T0003, T0004, T0006, and the emerging T0064 (Gather RAG-Indexed Targets). *Reproduce:* map every action your lab's recon engine takes to a technique ID and every detector to the signal that should have caught it. *Limits:* ATLAS is a living knowledge base; technique IDs and names shift as the field moves (treat specifics as CURRENT, principles as durable).

**Companion — OWASP Top 10 for LLM Applications 2025, LLM07 (System Prompt Leakage) and LLM02 (Sensitive Information Disclosure).** *Why:* the two Top-10 entries that turn a deployed app into a recon source. *Read:* the leakage scenarios and mitigations; connect "don't put secrets in the system prompt" to "assume the prompt is recon-visible."

## Further reading

- Cisco/Talos, *Detecting exposed LLM servers with Shodan: a case study on Ollama* — practical passive discovery of AI infrastructure.
- Wiz, *ShadowRay* — how exposed Ray dashboards (found by scanning) became in-the-wild compromise of AI compute (CVE-2023-48022 and later Ray CVEs).
- Sibling course, agents & tool-use modules, for the deployment shapes you are fingerprinting: https://tal-giladi.github.io/llm-research-engineer-course/
- This course: [00.1 · Threat modeling for AI systems](../module-00/lesson-01.md), [02.2 · The inference API attack surface](../module-02/lesson-02.md), [16.1 · The agent attack surface](../module-16/lesson-01.md), [14.1 · RAG retrieval attack surface](../module-14/lesson-01.md), and the supply-chain view in [22.1](../module-22/lesson-01.md).

## What you should now be able to do

- Place reconnaissance in the red-team lifecycle and map each action to a MITRE ATLAS Reconnaissance technique.
- Build a four-layer asset map of an AI target — applications, ML components, infrastructure, dependencies — from passive OSINT first, active probing second.
- Fingerprint a served model and its stack from benign protocol and behavioral signals, using the fewest probes that answer the question.
- Quantify the completeness-vs-detection trade-off and design low-and-slow, distributed probing against real detector shapes.
- Deny discovery and detect scanning on the blue-team side, and state precisely what each control does and does not guarantee.
