---
id: "14.2"
module: 14
minutes: 16
practice_minutes: 60
prerequisites: ["14.1", "05.1", "24.1"]
objectives:
  - Explain persistent billable state and why an untrusted tool can convert data it already holds into recurring victim-billed inference cost.
  - Compute cumulative input inflation as a function of turns and tool response size, and state why it is linear and therefore unbounded.
  - Distinguish this attack from exfiltration and excessive agency by its objective and its precondition.
  - Implement and price three context policies - blunt deletion, compression, and a fixed cap - against the same task.
  - Explain why the enforced control is upstream of the context window, and write its guarantee analysis.
volatility: current
sources:
  - title: "Zhang, Xia, Zhang, Cheng, Tu, Wu, Yue — DOW-BENCH: denial-of-wallet attacks on tool-calling LLM agents"
    url: https://arxiv.org/abs/2609.28585
  - title: "OWASP Top 10 for LLM Applications 2026 — LLM06:2026 Unbounded Consumption"
    url: https://genai.owasp.org/llm-top-10/
  - title: "OWASP Top 10 for Agentic Applications 2026 — ASI02 tool misuse"
    url: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
last_verified: "2026-09-30"
---

# 14.2 · Denial of wallet

A new agent attack class with an unusual objective. The attacker does not want your data, does not want to act as you, and never takes a credential. They want you to **pay**. A tool that returns a lot of text costs the host nothing to produce and the agent owner a great deal to re-process, on every subsequent turn.

## Why this matters

Most of this course assumes the attacker's goal is access: read a secret, call a privileged API, exfiltrate something. Denial of wallet inverts that. The attacker already has something they are entitled to — the ability to return tool output — and converts it into recurring, victim-billed inference cost. There is no privilege escalation, no stolen credential, no data leaving the machine, and nothing in the logs that looks like an intrusion. The observable outcome is an invoice.

The mechanism is mundane once you see it. When a host runtime carries a previous tool's return value into later model turns, the provider re-meters that content **on every subsequent call**. So a tool that returns $k$ characters on turn 1 is not billed once — it is billed once per turn for the rest of the session. The host is re-charging the victim for the attacker's data, over and over, and the multiplier grows with session length.

DOW-BENCH formalized this as *persistent billable state* and measured it across six model families over 243 executions. Cumulative input reached **14,293x** the initiating call's size in the worst vector. Naive raw-history retention raised mean session cost by **21–35%** against benign workloads. This is the class OWASP calls **Unbounded Consumption** (LLM06:2026), applied to agents, where the consumer is not the attacker but the agent's own memory of what the attacker said.

## Learning objectives

1. Explain persistent billable state, and why an untrusted tool can convert data it already holds into recurring, victim-billed inference cost.
2. Compute cumulative input inflation as a function of turns and tool response size, and state why it is linear and therefore unbounded.
3. Distinguish this attack from exfiltration and excessive agency by objective and precondition.
4. Implement and price three context policies — blunt deletion, compression, and a fixed cap — against the same task.
5. Explain why the enforced control sits upstream of the context window, and write its guarantee analysis.

## Concept

### Why the context window is a billing surface

Almost every agent framework builds the next request by concatenating messages: the system prompt, the conversation so far, and every tool result the agent has seen. That is the right thing to do for *capability*. It is also a charging model:

$$ \text{cost} = \sum_{t=1}^{T} r \cdot \frac{C_0 + \sum_{i<t} k_i}{1000} $$

where $C_0$ is the initial context and $k_i$ the size of the $i$-th tool result. The first term is the host's; the second is whatever a tool chose to return, and it is multiplied by the number of turns still to come. Differentiate with respect to a single early $k_i$ and you get $r(T - i)/1000$ — **the earlier in the session a hostile tool returns its payload, the more it costs you.** An attacker wants to be turn one.

There is no amplification step and no gadget. The "vulnerability" is that the host treats tool output as data to remember rather than data to budget for.

### Distinguishing it from the attacks you already know

| | Goal | Precondition | Observable |
|---|---|---|---|
| **Exfiltration** | attacker reads data | attacker reaches an egress path | a request leaving with the payload |
| **Excessive agency** | attacker acts as the agent | the agent holds a dangerous capability | a privileged tool call |
| **Denial of wallet** | attacker spends the victim's money | a tool may return an unbounded payload | a bill |

The absence of a visible action is what makes this one hard to catch with intrusion tooling. Your SIEM sees an agent having a long conversation. The defender's real instrument is the **cost per session distribution**, not the event log.

### Three context policies, three different failures

Every fix trades money for usefulness, and the three most obvious ones fail differently:

- **Blunt deletion** (drop history on every turn) is by far the cheapest and it destroys the task. The lab shows 1 of 12 steps completed: the context the work depends on is exactly what you threw away. DOW-BENCH measured this as succeeding on only 2 of 12 history-dependent tasks.
- **A fixed context or cost cap** is predictable and bounded, but it *interrupts*: work that legitimately needs a long session gets truncated mid-task. It also creates a denial-of-service on yourself, which is why "progress-authorized" retention — dropping only *completed* steps — is the more interesting middle.
- **Compression** keeps a residue sized to what the task needs rather than what the tool returned. More expensive per turn than deletion, and it preserves the task: the lab completes all 12 steps at ~1.8% of the undefended cost.

Notice what none of these is. There is no option here that is "detect the hostile tool". Detection is a fourth path, and it is the worst of them, because the tool's output is indistinguishable from a legitimately verbose one.

## Intuition

Imagine a conference where every attendee's notes are re-read aloud and billed to the room, once per exchange. A guest who brings an unusually long document does not steal anything and disrupts nothing — they just make the room expensive, and the bill arrives at the end, attributed to the host.

The instinctive fix is to stop reading the notes out. But the notes are how the conversation works. The actual fix is upstream and dull: **cap what a guest is allowed to bring in, and bill the room once rather than once per exchange.** Nothing clever happens; that is the point. The interesting attack was never sophisticated — it was a large tool response and a billing model nobody questioned.

## Technical explanation

### Why inflation is linear and therefore unbounded

Let $k$ be the hostile tool's per-turn payload and $T$ the session length. Cumulative input is

$$ C(T) = \sum_{t=1}^{T}\left(C_0 + (t-1)k\right) = T\,C_0 + k\,\frac{T(T-1)}{2} $$

The payload term is **quadratic in $T$** for a fixed per-turn payload, and **linear in $k$**. So an attacker picks whichever axis the host makes cheap. Doubling the session doubles the cost; doubling the payload doubles it too; doubling both quadruples it. That is the whole attack surface, and it is why "we cap sessions at 20 turns" bounds cost without bounding the attack: the per-turn payload is unbounded, and the lab's inflation table is the linear term made visible.

### Pricing a defense honestly

Let $U$ be the fraction of task steps completed and $C$ the billed cost. A defense is only worth discussing as a pair $(C, U)$, because a 99% cost reduction that takes $U$ from 1.0 to 0.08 is not a defense, it is a broken product. The lab prints both columns for exactly this reason, and the module-23 guarantee box below says the same thing in prose: **the utility cost is part of the guarantee, not a footnote.**

### Where the enforced control belongs

All three context policies are mitigations applied to a quantity the attacker influenced. The structural fix is one step earlier: **do not let a tool decide how much it returns.** Cap the response size in the tool wrapper, in code, before the value enters the transcript. Then $k$ has a ceiling the attacker cannot raise, and the quadratic term collapses regardless of what any downstream policy does. This is enforced > probabilistic again — the control does not ask whether the payload is hostile, it removes the freedom to be large.

## Mathematics

**Cost model.** With per-1K-token rate $r$, initial context $C_0$, per-turn hostile payload $k$ and session length $T$:

$$ \text{cost} = \frac{r}{1000}\left(T C_0 + k\frac{T(T-1)}{2}\right) $$

The lab uses $r = 0.003$, $C_0 = 400$, $k = 4000$, $T = 12$: $400 \times 12 + 4000 \times 66 = 268{,}800$ input tokens, **0.806 credits for one task**, against 0.0048 for the initiating call — 121x inflation on a single session.

**Compressed retention.** If a policy retains a residue $c \ll k$ per turn, the payload term becomes $c\,T(T-1)/2$, so the saving is $1 - c/k$ asymptotically. With $c = 64$ and $k = 4000$ that is 98.4%, which is what the lab reports — and it is why compression is cheap *enough* to leave on permanently.

**Detection threshold.** If benign per-session cost has mean $\mu$ and standard deviation $\sigma$, and the attack multiplies cost by $M$, then flagging sessions above $\mu + z\sigma$ needs $z \gtrsim \frac{(M-1)\mu}{\sigma}$ to have any power. A benign mean of, say, 50 credits against a $\sigma$ of 10 puts the attacker's bar above $5\sigma$ — easily met. **Cost-based detection is cheap because the effect size is large**; it is the *base rate* that then decides whether you block or alert.

## Attack / Defense model

> [!IMPORTANT]
> **Guarantee analysis — agent cost controls.**
> - **Stops:** unbounded growth, if you cap the tool's response size in code. With a hard $k_{\max}$, the payload term is bounded by $k_{\max}T(T-1)/2$ regardless of what the tool returns, so the attacker's freedom is removed rather than filtered. A per-session billing ceiling bounds the bill directly.
> - **Does NOT stop:** anything inside the ceiling. A tool that inflates cost up to the cap still inflates it; compression and caps reduce a number, they do not decide intent. Nor does any of this detect the hostile tool, which may be perfectly legitimate and merely large.
> - **Attacker adapts:** shrinks the payload to fit under the cap and lengthens the session instead (the inflation table is a two-axis surface, so pinning one axis moves the attack to the other); or finds the tool whose legitimate output is genuinely large, so the traffic never looks anomalous.
> - **FP cost:** real and specific. Compression that is too aggressive degrades history-dependent tasks; a cap that is too tight truncates legitimate long work; cost-based alerting flags the busiest legitimate users. These are the same utility costs the lab prints in the second column.
> - **Perf cost:** compression and summarization cost tokens and latency on *every* turn, including the overwhelming majority of benign ones — a per-turn tax paid for an attack that is rare. That is the argument for enforcing the cap in code (free) and leaving compression off unless measured.
> - **Takeaway:** cap the tool response in code, bill per session rather than per accumulated context, and treat compression as a measured mitigation rather than a default. If you report this finding, report the utility cost next to the saving — a cost reduction that breaks the task is not a defense.

## Practical lab

**Lab 14.2** ([`labs/module-14/`](../../labs/module-14/README.md)) — the billing mechanism, the
inflation curve, and three context policies priced against the same task. Offline, stdlib only.

```bash
py labs/module-14/denial_of_wallet.py
py -m pytest labs/module-14 -q
```

## Exercise

1. **Find the two axes.** From the lab's cost model, derive how cost scales with $T$ and with $k$ separately. Then implement a host that caps only one of them and show the attacker moving to the other. Which axis is cheaper for the attacker to exploit, and why?
2. **Price compression honestly.** Sweep the retained residue size $c$ from 0 to $k$ and plot cost against steps completed. Where is the knee, and is that the right operating point for a product? Justify it with the utility number, not the cost number.
3. **Make the tool payload bounded in code.** Add a response-size cap in the tool wrapper and re-run the sweep. Show the quadratic term collapse and explain why this is an enforced control while the other three are not.
4. **Detection.** Build a cost-anomaly detector over simulated benign sessions with a known mean and spread. Choose a threshold, compute how many benign sessions it flags, and show the base-rate arithmetic from module 23 deciding block-versus-alert. Then raise $M$ until it stops working.
5. **Adaptation.** Write the evasion from exercise 1 as a concrete host design that looks defensible in review, and state which guarantee box you would have to weaken to accept it.

## Research paper

**Zhang, Xia, Zhang, Cheng, Tu, Wu & Yue, "DOW-BENCH: denial-of-wallet attacks on tool-calling LLM
agents" (2026)**. *Why:* it names the class, derives the vectors from where retained tool output
re-enters billable context, and — unusually — measures a utility cost for each mitigation rather
than reporting savings alone. *Read:* the six vectors and which axis each one pushes on; the
compression-versus-deletion comparison on history-dependent tasks; the progress-authorized
retention policy. *Reproduce:* the lab is a from-scratch reimplementation of the cost model;
extend it with a real model and a real tool to get token counts rather than characters.
*Limits:* the reported rates are per-model-family and pricing-dependent, so treat 14,293x as a
demonstration that the mechanism is unbounded rather than as a constant to quote in a report.
Whether the behaviour is model-specific is not settled.

## Further reading

- OWASP LLM Top 10 2026 — **LLM06:2026 Unbounded Consumption**; and OWASP Agentic Applications
  **ASI02 tool misuse** ([crosswalk](../../references/standards-map.md)).
- Module 23 for the enforced-versus-probabilistic distinction and the base-rate arithmetic;
  module 16 for why an untrusted tool is a confused deputy even when it cannot act.

## What you should now be able to do

- Explain persistent billable state and compute cumulative input inflation from turns and payload size.
- Tell denial of wallet apart from exfiltration and excessive agency by objective and observable.
- Implement and price deletion, compression and capping policies against one task, reporting utility alongside savings.
- Locate the enforced control upstream of the context window, and state what each mitigation still misses.
