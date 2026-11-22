---
id: "15.2"
module: 15
minutes: 18
practice_minutes: 90
prerequisites: ["15.1", "12.1"]
objectives:
  - "Explain how a prefix cache shared across tenants turns a performance optimisation into a membership side channel, and why chained block hashes let one correct guess unlock the rest of a prompt."
  - "Compute the distinguishing advantage of a timing probe from the cached length, the per-token prefill cost and the timing noise, and check it against a simulation."
  - "Implement per-tenant cache salting, measure that it closes the channel, and measure the cross-tenant reuse it gives up."
  - "Show why padding only the hit request fails on a step-based scheduler, by measuring listener requests queued behind the probe."
  - "Write the guarantee analysis for salting, hit-only padding and random delay, including their latency and cost trade-offs."
volatility: concept
sources:
  - title: "Gu, Li, Kuditipudi, Liang, Hashimoto — Auditing Prompt Caching in Language Model APIs (ICML 2025)"
    url: https://arxiv.org/abs/2502.07776
  - title: "Song et al. — The Early Bird Catches the Leak: Unveiling Timing Side Channels in LLM Serving Systems (IEEE TIFS)"
    url: https://arxiv.org/abs/2409.20002
  - title: "vLLM security advisory GHSA-4qjh-9fv9-r85r / CVE-2025-46570 — timing side channel in prefix caching (fixed in 0.9.0)"
    url: https://github.com/vllm-project/vllm/security/advisories/GHSA-4qjh-9fv9-r85r
  - title: "vLLM pull request #17045 — [Core] Prevent side-channel attacks via cache salting"
    url: https://github.com/vllm-project/vllm/pull/17045
  - title: "vLLM documentation — Automatic prefix caching (design)"
    url: https://docs.vllm.ai/en/latest/design/prefix_caching.html
  - title: "Sun, Xiao — Where the Savings Go: The Limits of Hiding Cross-Tenant Cache Hits in LLM Serving (arXiv preprint, 2026)"
    url: https://arxiv.org/abs/2611.20291
  - title: "Zheng et al. — InputSnatch: Stealing Input in LLM Services via Timing Side-Channel Attacks (arXiv preprint)"
    url: https://arxiv.org/abs/2411.18191
last_verified: "2026-11-22"
---

# 15.2 · Shared prefix caches as a cross-tenant side channel

Lesson 15.1 fixed cross-tenant leakage on the retrieval path by authorising in code before ranking. This lesson finds the same kind of leak one layer lower, in the serving engine, where no document is ever returned: a cache shared by all tenants answers faster when someone else already sent your text, and the speed-up alone is enough to read their prompt.

## Why this matters

Every serious LLM serving stack reuses the key/value (KV) state of prompt prefixes it has already
processed, because system prompts, tool definitions and RAG templates repeat across millions of
requests and prefill is the expensive part. If that cache is shared across customers, a cache hit is
a fact about *another customer's* traffic, and it is visible in the time to first token (TTFT).

This is not a hypothetical. Gu et al. (ICML 2025) ran statistical timing audits against real APIs and
detected cache sharing across users in seven providers, including OpenAI. Song et al. (IEEE TIFS)
recovered system prompts and other users' prompts from shared-cache timing. vLLM, the most widely
used open-source engine, published CVE-2025-46570 for exactly this channel and shipped per-request
**cache salting** as the fix. And in November 2026 a preprint showed that the tempting middle ground
(keep sharing, hide the hit) fails on the schedulers real engines use. The pattern is one you will
meet again and again: a performance optimisation creates a side channel, the clean fix gives up the
optimisation, and the clever fix that tries to keep it leaks through a second-order effect.

## Learning objectives

1. Explain how a shared prefix cache becomes a cross-tenant **membership oracle**, and why chained
   block hashes let one correct guess unlock the rest of a templated prompt.
2. Compute a timing probe's **distinguishing advantage** from the cached length, the per-token
   prefill cost and the noise, and check the number against the lab.
3. Implement **per-tenant salting**, show that it closes the channel, and measure the reuse it costs.
4. Show why **hit-only padding** fails on a step-based scheduler, using listener requests.
5. Write the guarantee analysis for salting, hit-only padding and random delay.

## Concept

### Prefill, the KV cache and prefix caching (a short recap)

Generating the first output token requires running the whole prompt through the model once
(*prefill*) and storing every layer's keys and values for every prompt position (the *KV cache*). The
sibling course ([LLM Research Engineer](https://tal-giladi.github.io/llm-research-engineer-course/))
covers attention and the KV cache in depth; here you only need one fact: **prefill cost grows with
the number of prompt tokens that are not already cached.**

*Prefix caching* keeps the KV state of past prompts in fixed-size **blocks** (vLLM's default is 16
tokens) and reuses any block whose content and position match. vLLM's design document says how a
block is identified: the hash of a tuple of the parent block's hash, the block's own tokens, and
extra keys (LoRA id, multimodal input hashes, **cache salt**). Two consequences matter for security:

- **Only full blocks are cached, and only along a chain.** A block hits only if every block before
  it also hit. Changing token 3 makes every later block miss.
- **One correct guess unlocks everything after it.** If a victim's prompt is "public template +
  secret field + long public suffix", an attacker who guesses the secret field correctly also gets a
  hit on the whole suffix. A wrong guess misses the whole suffix. The suffix turns a 16-token
  difference into a several-hundred-token difference.

### The channel

Tenant A sends a text. Later tenant B sends a guess and times its first token. If A's text equals the
guess (block-aligned), B's prefill skips the cached blocks and B's TTFT is shorter. B has learned one
bit about A's traffic: *someone sent this*. With a small candidate set (a templated prompt with a
customer name, an account tier, a short code) one bit per candidate is enough to read the field.

There is a quirk that makes the attacker's job harder: **a probe pollutes the cache it measures.**
After B's probe, the guessed text *is* cached, so a second probe of the same guess always hits. The
attacker usually gets one measurement per candidate, which is why the *single-probe* advantage is the
number that matters.

### Three defenses, three different promises

| Defense | What it changes | What it costs |
|---|---|---|
| **Per-tenant salting** (vLLM `cache_salt`) | the salt is mixed into the first block's hash, so only requests with the same salt can share blocks | all cross-tenant reuse; a shared trust group (same salt) keeps reuse inside the group |
| **Hit-only padding** | keep global sharing; delay the reply of a request that hit another tenant's blocks by the time it saved | little, but it does not work (see below) |
| **Random delay on every reply** | add uniform noise to all emissions | latency for *every* request; must be several times the signal |

### Why hit-only padding fails

Real engines run a **step-based scheduler**: each step processes up to a fixed budget of prompt
tokens across the queued requests (chunked prefill), and a step that processes fewer tokens is
shorter. A cache hit means the engine did less work, and that saved work does not disappear when
you pad the hit request's reply: the requests **queued behind it** start and finish earlier. Sun and
Xiao (2026) exploit this with *listeners*: the attacker sends a group of one-token requests, then the
probe, then a second group of one-token requests, all at once. On a miss the probe's prefill fills
the step budget and pushes the trailing group into a later step; on a hit the trailing group finishes
in the same step as the leading group. Padding the probe changes nothing the listeners see.

## Intuition

A shared office printer keeps a copy of every document it has printed recently, and reprints a
cached document instantly. You want to know whether your competitor printed "Offer: 1.2M". You send
that exact document and time it: instant means someone printed it. The office fixes this by giving
each company its own cache (salting): now nobody else's printing can speed you up, and nobody gets
the shared speed-up either. A cleverer fix keeps the shared cache but makes cached reprints *wait*
as if they were printing. It fails, because you also queue two short jobs, one before and one after
your test document. When the test document comes from cache, the printer gets to your second short
job sooner, and no amount of waiting on your test document hides that.

## Technical explanation

The lab's engine (`labs/module-15/prefix_cache/pc_engine.py`) is a deliberately small model of the
mechanisms above:

- `PrefixCache.block_hashes` computes `h_i = SHA-256(h_{i-1} || tokens of block i)`, with `h_0`
  derived from the salt (empty under global sharing). `match` walks the chain until the first miss
  and always leaves at least one token to compute, because the engine needs the last position's
  logits to emit a token.
- `Engine.step` serves the FIFO queue up to `budget` prompt tokens, then advances time by
  `c0 + c1 * tokens_processed + noise`. A request's first token is emitted at the end of the step in
  which its prefill completes. Background traffic from other tenants arrives at half capacity, which
  is what makes the probe's timing noisy.
- `hide_hits=True` delays a cross-tenant hit's reply by `c1 * cached_tokens` (the time it saved).
  `jitter=D` adds a uniform delay in `[0, D]` to every reply.

The two attacks are in `pc_attacks.py`: `probe_direct` (time your own first token) and
`probe_listeners` (mean TTFT of the trailing group minus the leading group). `advantage` chooses a
threshold on half of the trials and reports TPR − FPR on the other half, so the result is not
flattered by fitting the threshold to the test data.

## Mathematics

**Single-probe advantage.** Model the attacker's measured TTFT as Gaussian with the same spread
$\sigma$ for hits and misses, and a hit saving $\Delta = c_1 \cdot n$ for $n$ cached tokens at
prefill cost $c_1$ per token. The best threshold sits halfway between the two means, and the
distinguishing advantage is

$$
\mathrm{Adv} = \mathrm{TPR} - \mathrm{FPR} = 2\,\Phi\!\left(\frac{\Delta}{2\sigma}\right) - 1,
$$

where $\Phi$ is the standard normal CDF. Worked example with the lab's $c_1 = 0.02$ ms/token and
$\sigma = 1.5$ ms (roughly what its background load produces):

| cached tokens $n$ | $\Delta$ (ms) | $\Delta / 2\sigma$ | Adv (formula) | Adv (lab, direct probe) |
|---|---|---|---|---|
| 16 | 0.32 | 0.107 | 0.085 | 0.08 |
| 64 | 1.28 | 0.427 | 0.33 | 0.26 |
| 256 | 5.12 | 1.707 | 0.91 | 0.86 |

For $n = 256$: $\Phi(1.707) \approx 0.956$, so $\mathrm{Adv} \approx 2(0.956) - 1 = 0.91$. The
shape matches the vLLM advisory's real measurement (AUC 0.571 for a 1-token prefix, 0.99 for 8
tokens with a 2-token chunk size) and Sun and Xiao's (advantage at least 0.98 for 256+ tokens with
one probe on a vLLM trace replay): **the leak grows with how much of the prompt the guess shares.**
That is why the known-suffix trick in the Concept section matters so much.

**Listener shift.** With a per-step budget $B$ and step time $t_s \approx c_0 + c_1 B$, a missed
probe of $n \ge B$ tokens pushes the trailing listeners back by about $\lceil n / B \rceil$ steps. In
the lab $t_s \approx 1 + 0.02 \cdot 256 = 6.12$ ms per step. Padding the probe's reply does not
change this term at all.

**How much random delay?** If each of $k$ listeners per group gets an independent uniform delay
$U[0, D]$, the difference of the two group means has variance $2 \cdot \frac{D^2}{12} / k$; for
$k = 8$ its standard deviation is $D / \sqrt{48} \approx D / 6.93$. Plug that into the advantage
formula with $\Delta = t_s = 6.12$ ms:

| $D$ (ms) | sd (ms) | Adv (formula) | Adv (lab) | mean added latency, every request |
|---|---|---|---|---|
| 6 | 0.87 | 1.00 | 0.94 | 3 ms |
| 20 | 2.89 | 0.71 | 0.51 | 10 ms |
| 60 | 8.66 | 0.28 | 0.18 | 30 ms |

The lab is a little lower than the formula because queue noise adds to the jitter. Either way the
delay has to be about ten times the shift before the advantage falls near 0.1, which is the order of
magnitude Sun and Xiao report, and the attacker can push it back up by adding listeners (the
variance falls as $1/k$).

**The leakage–savings bound (EMERGING, single preprint).** Sun and Xiao prove that a rate-limited
tenant's gain from content written by $k$ other accounts is at most on the order of
$k \times$ (the allowed leakage). Read it as: *any* cross-tenant saving that a customer can see is
leakage by definition, so with zero leakage only the provider keeps the savings. Exact hiding is
possible in principle on one instance, but it means padding every step that might contain a hit, at
a cost that grows with time rather than with the number of hits.

## Attack / Defense model

> [!IMPORTANT]
> **Guarantee analysis: per-tenant cache salting (the deployed fix).**
> - **Guarantees:** a request can only reuse blocks written under the same salt, so its timing
>   carries no information about other salts' traffic. In the lab the advantage falls to chance
>   (0.05 direct, 0.03 listener) and canary extraction to the 1-in-16 guess rate.
> - **Does NOT guarantee:** isolation *inside* a salt group (users of one tenant who share a salt can
>   still probe each other), isolation if the salt is guessable or set by the client without the
>   server checking it, or protection from other shared-resource channels (scheduler load, GPU
>   contention, semantic caches, hardware faults). It also does nothing if any code path forgets
>   to pass the salt.
> - **How the attacker adapts:** get an account in the victim's salt group; find a request path that
>   drops the salt; switch to a channel the salt does not cover (queue load, a semantic cache).
> - **False-positive cost:** none; it is a key change, not a detector.
> - **Performance cost:** all cross-tenant prefix reuse. In the lab's workload (a 512-token shared
>   system prompt) cache-served tokens fall from 88% to 71% with 5 requests per tenant, and to 0%
>   with one request per tenant. Trust groups recover part of it, at the price of shared exposure.

> [!IMPORTANT]
> **Guarantee analysis: hit-only padding and random delay (keep sharing, hide the hit).**
> - **Guarantees:** hit-only padding hides the probe's *own* TTFT (lab: direct advantage 0.00).
> - **Does NOT guarantee:** anything about other requests. On a step-based scheduler the saved work
>   reaches every request queued behind the hit (lab: listener advantage 1.00, canary extraction
>   1.00). Random delay only lowers the advantage statistically.
> - **How the attacker adapts:** listeners; more listeners per group to average away jitter.
> - **False-positive cost:** none.
> - **Performance cost:** random delay taxes every user (30 ms mean at the lab's useful setting);
>   exact hiding needs padding work whose cost grows with time.

> [!WARNING]
> Measuring another customer's cache state on a shared API is an attack on that customer, whatever
> your intent. Run timing probes only against engines you operate, such as the lab's simulator or a
> local vLLM instance with no other users.

**Progression, not replacement.** Everything 15.1 taught still holds: authorisation must be enforced
in code on a trusted principal. Salting is that same rule applied to a cache key: the tenant identity
from your auth context, not from the request body, decides which blocks a request may touch. Hit-only
padding is the cache-level version of "trust the model to keep the secret": it tries to hide a
leak instead of removing the shared state that causes it.

## Real-world examples

- **Gu et al., ICML 2025.** Statistical timing audits detected global cross-user cache sharing in
  seven API providers, including OpenAI, at the time of the audit, and inferred that OpenAI's
  embedding model is a decoder-only Transformer from timing alone. DOCUMENTED (peer-reviewed).
  Provider caching policies change; check the current documentation of any provider you use.
- **Song et al., IEEE TIFS.** Timing side channels from shared KV and semantic caches; a
  token-by-token search recovers system prompts and other users' prompts. DOCUMENTED.
- **vLLM CVE-2025-46570 (GHSA-4qjh-9fv9-r85r, CVSS 3.1 base 2.6, fixed in 0.9.0).** TTFT reveals
  prefix-cache hits. Fix: PR #17045 added an optional `cache_salt` request field, mixed into the first
  block's hash so that only requests with the same salt share blocks; later blocks inherit it through
  the parent hash. CURRENT (checked 2026-11-22 against the advisory, the PR and the design document).
- **Sun and Xiao, 2026 (arXiv preprint, not yet replicated).** Hiding hits fails through scheduler
  step shifts on vLLM and SGLang; one probe detects cached texts of 256+ tokens with advantage at
  least 0.98; random delays must be about ten times the shift to bring the advantage to 0.1.
  EMERGING.
- **InputSnatch (arXiv preprint).** Combines timing probes with a learned candidate generator to
  recover inputs from cache-sharing services. EMERGING.

## Code

`labs/module-15/prefix_cache/pc_engine.py` holds `PrefixCache` and `Engine`; read
`PrefixCache.block_hashes` and `Engine.step` first, because every result follows from them.
`pc_attacks.py` holds the two probes, the `advantage` measurement, `extract_canary` (a victim system
prompt of public template + one `LAB-CANARY-NN` block + public suffix) and `reuse_fraction`.
`pc_evaluate.py` runs the whole cycle.

## Practical lab

**Lab 15.2** ([`labs/module-15/prefix_cache/`](../../labs/module-15/prefix_cache/README.md)): attack,
defend, adapt, retest. Offline, standard library only, about 10 seconds.

```bash
python labs/module-15/prefix_cache/pc_evaluate.py
python -m pytest labs/module-15/prefix_cache -q
```

Expected shape of the output: direct-probe advantage rising from about 0.08 (16 tokens) to above 0.85
(256 tokens); canary recovery at 1.00 with the known suffix and near chance without it; salting
bringing every attack to chance while cache-served tokens fall; hit-only padding stopping the direct
probe but not the listeners; jitter needing tens of milliseconds to matter.

## Exercise

1. **By hand first.** With $c_1 = 0.02$ ms/token and $\sigma = 1.5$ ms, how many cached tokens does
   a single probe need for an advantage of 0.5? Check your answer with `advantage("direct", n)`.
2. **The suffix effect.** Run `extract_canary` with and without the public suffix
   (`with_suffix=False`), then change `SUFFIX` in `pc_attacks.py` to 4, 12 and 28 blocks. Plot recovery rate against suffix length and explain the curve with
   the advantage formula.
3. **Defend, then bypass your own defense.** Turn on salting (`salting="tenant"`) and give two
   tenants the same salt with `salt_of={"acme": "shared", "globex": "shared"}` (a trust group). Show that the attack works again,
   then write the rule that decides who may share a salt.
4. **Price the delay.** For `hide_hits=True`, find the smallest `jitter` that brings the listener
   advantage below 0.1. Then double the number of listeners (change the default `k=8` in
   `probe_listeners` to 16) and find it again. What does
   this say about random delay as a defense?
5. **Guarantee box.** Write your own guarantee analysis for "per-tenant salt plus a shared salt for
   public system prompts only", and name the attacker it still does not stop.

<details><summary>Hint (step 1)</summary>

$2\Phi(x) - 1 = 0.5$ means $\Phi(x) = 0.75$, so $x \approx 0.674$. Then
$\Delta = 2\sigma x \approx 2.02$ ms and $n = \Delta / c_1 \approx 101$ tokens. Because only full
blocks are cached, round up to 112 (7 blocks of 16). Queue noise makes the lab lower (about 0.44 at 112 tokens), so you need a few
more blocks in practice.

</details>

<details><summary>Hint (step 4)</summary>

The difference of two group means has standard deviation $D\sqrt{2/(12k)}$. Doubling $k$ divides
it by $\sqrt 2$, so the defender must raise $D$ by about 41% for every doubling of listeners, and
every honest user pays $D/2$ on average. The attacker's listeners cost almost nothing.

</details>

## Research paper

**Gu et al., "Auditing Prompt Caching in Language Model APIs" (ICML 2025)**, read together with
**Sun and Xiao, "Where the Savings Go" (2026 preprint)**. *Why:* the first shows how to *detect* a
shared cache on a black-box API with a statistical test and a controlled false-positive rate (the
defender's and auditor's view); the second shows why hiding hits instead of removing sharing fails.
*Read:* Gu et al.'s audit procedure and hypothesis test, then Sun and Xiao's threat model and the
listener construction. *Skip on first pass:* the full proof of the leakage bound. *Reproduce:* the
lab reproduces both mechanisms on a simulator; exercise 4 reproduces the delay-versus-advantage
curve. *Limits:* the 2026 result is a single preprint without released code; treat its exact numbers
as EMERGING until another group reproduces them.

## Further reading

- [vLLM automatic prefix caching design](https://docs.vllm.ai/en/latest/design/prefix_caching.html):
  how block hashes, extra keys and `cache_salt` fit together.
- [vLLM advisory GHSA-4qjh-9fv9-r85r](https://github.com/vllm-project/vllm/security/advisories/GHSA-4qjh-9fv9-r85r)
  and [PR #17045](https://github.com/vllm-project/vllm/pull/17045): a real disclosure and fix.
- Song et al., [The Early Bird Catches the Leak](https://arxiv.org/abs/2409.20002) (IEEE TIFS):
  token-by-token prompt recovery and semantic-cache channels.
- Back to [15.1](lesson-01.md) for authorisation on a trusted principal; back to
  [12.1](../module-12/lesson-01.md) for membership inference, the same question asked of a model's
  weights instead of a cache.

## What you should now be able to do

- Explain how a shared prefix cache becomes a membership oracle, and why a known suffix amplifies it.
- Compute a probe's advantage from cached length, prefill cost and noise, and check it in a simulator.
- Deploy per-tenant salting, state exactly what it isolates, and measure the reuse it costs.
- Break hit-only padding with listener requests and explain why the saved work leaks.
- Write the guarantee analysis for each cache-timing defense, including who pays the latency.
