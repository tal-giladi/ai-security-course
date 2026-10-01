---
id: "20.2"
module: 20
minutes: 16
practice_minutes: 60
prerequisites: ["20.1", "06.1", "09.1"]
objectives:
  - Explain text-centric instruction tuning and the resulting modality gap between text-carried and image-carried instructions.
  - Implement a rasterizing untrusted-content middleware from scratch and measure its effect on injection success.
  - Explain why the same gap that makes the defense work also makes it erasable, and what fine-tuning on rendered instructions does to it.
  - State what the defense does not cover, including pixel-space adversarial examples and steganographic payloads.
  - Write the guarantee analysis for a carrier-changing defense, including its performance cost.
volatility: current
sources:
  - title: "Zhang, Baroian, van Rijn, Shafran, Tramèr — Render Before Reading: converting untrusted text to images exploits a text/non-text safety-training gap"
    url: https://arxiv.org/abs/2609.36121
  - title: "Bagdasaryan et al. — (Ab)using Images and Sounds for Indirect Instruction Injection"
    url: https://arxiv.org/abs/2302.12173
  - title: "Athalye, Engstrom, Ilyas, Kwok — Obfuscated Gradients Give a False Sense of Security"
    url: https://arxiv.org/abs/1806.08096
last_verified: "2026-09-30"
---

# 20.2 · Render before reading

Module 20 gave you four channels. This lesson is the one defense in that chapter that does not inspect anything at all — it simply changes which channel the untrusted content arrives on.

## Why this matters

Multimodal models are more susceptible to an embedded instruction when it arrives as **text** than to the same instruction delivered as an **image**. That is a strange asymmetry, and it is not a property of images: it is an artefact of *text-centric instruction tuning*. Models were trained to be told what to do in text, so an imperative in the text channel lands where the training expects instructions, and the same imperative rendered as pixels is read as content.

A gap between what a model treats as data and what it treats as orders is exactly the kind of thing this course exploits for attacks. Here it can be exploited for defense: **rasterize untrusted content before the model ever reads it**, and the instruction arrives as pixels instead of tokens.

The 2026 paper that proposed this evaluated it across ten models on two injection benchmarks (DirectInject and AgentDojo), and reports that it held up even against adaptive attacks and human red-teamers while preserving benign task utility. Read that as a strong result — and read the next section, because the defense has a documented expiry date.

## Learning objectives

1. Explain text-centric instruction tuning and the resulting modality gap between text-carried and image-carried instructions.
2. Implement a rasterizing untrusted-content middleware from scratch and measure its effect on injection success.
3. Explain why the same gap that makes the defense work also makes it erasable, and what fine-tuning on rendered instructions does to it.
4. State what the defense does not cover, including pixel-space adversarial examples and steganographic payloads.
5. Write the guarantee analysis for a carrier-changing defense, including its performance cost.

## Concept

### The gap is a training artefact, and that cuts both ways

Module 02's argument applies here in a new costume. Instruction-following is not an enforced
property of the system; it is a prior learned from data. The prior says *imperatives in the text
channel are instructions*. Rendering the same bytes to pixels moves them to a channel the model
reads as content, and the prior no longer fires.

That is the whole defense, and it is genuinely cheap — no model change, no auxiliary model, no
detector, roughly forty lines of code. It is also, by the same argument, **not durable**. If a
provider fine-tunes on rendered instructions, the gap closes, and the defense's mechanism
evaporates with it. The paper is unusually honest about this: it reports the erosion effect as a
*confirmation of the mechanism*, because a defense that works for a reason which can be trained
away is a defense on a timer.

So the correct engineering posture is not "adopt it" but "adopt it, and know which change would
retire it". That is a monitoring obligation: a defense tied to a training artefact should be
re-measured when the model changes, which is exactly the regression-testing argument of module 24.

### What it costs, and what it misses

Two costs, both real:

- **Performance.** Rasterized content is far more expensive per character than text — the lab
  prints the ratio: roughly 2,000 pixels for 48 characters. You are trading tokens for pixels,
  and a vision encoder does not read pixels for free. Long documents get expensive.
- **Coverage.** It moves the problem. A pixel-space adversarial perturbation (module 09) or an
  LSB-steganographic payload (module 20.1) rides the *same rasterized image* completely untouched —
  the defense changes the carrier of the text, and says nothing about the bits already in the
  image. If your untrusted input is an image with a payload in its pixels, rendering it is a no-op.

Neither cost is a reason not to do it. They are the reason to state it in a guarantee box rather
than a feature list.

### The general pattern

Worth naming, because it will keep appearing: **this is untrusted-data handling achieved by
changing the type rather than the content.** It is the same family as removing a query
interpreter, storing untrusted values in a type the parser will not dispatch on, or refusing to
coerce an untrusted string into code. All of them work by removing a capability rather than by
detecting abuse — which is why they hold against adaptive attackers who control the payload, and
why they all carry a utility cost and a residual.

## Intuition

If a clerk has been trained that anything written on a form is an instruction, the form is a
dangerous object regardless of what it says. But a photograph of the same form is just a
photograph — nobody obeys it. Making the clerk read a photograph of every form is absurd
administration, and it costs you a lot of photocopies.

It works, though, and it costs nothing in detection effort or false positives, which is a better
trade than a filter that has to guess. But you should know the clerk might one day be trained to
read photographs of forms, at which point the photocopy ritual stops helping and nobody notices
until the incident.

## Technical explanation

### Implementing it

The defense is a middleware at the boundary between "untrusted content" and "model input":

```
tool result / retrieved document  ──▶  sanitize  ──▶  render to pixels  ──▶  vision input
                                  (no text tokens)      (5x7 font, stdlib)
```

There is no detection step and no classifier, which is why it has no false-positive cost on the
security axis. The lab implements the renderer from scratch — a 5×7 bitmap font covering
printable ASCII, rasterized into a pixel grid — and routes three injection payloads through both
carriers to measure the difference.

### Measuring the gap

With $p_t$ the probability the model follows an embedded instruction arriving as text and $p_p$
the same for pixels, the defense's attack success rate is $p_p$ and the modality gap is

$$ \Delta = p_t - p_p $$

The lab reports $\Delta \approx 0.56$ on its stand-in model. Two things follow. First, $\Delta > 0$
is the entire justification, so a deployment should **measure its own model's $\Delta$** rather
than trusting a published number — the gap is model-specific. Second, and less obviously: if
fine-tuning on rendered instructions drives $p_p \to p_t$, then $\Delta \to 0$ and the defense's
value goes to zero with nothing failing visibly. The lab simulates exactly this and prints the
number, because a defense whose failure mode is silent deserves a test.

### Why $n$ matters here more than usual

Because the defense's whole effect size is $\Delta$, and $\Delta$ is estimated from a finite
sample, an evaluation with small $n$ will happily "confirm" a defense that does nothing. Use the
Wilson interval from module 24 and refuse to claim $\Delta > 0$ unless the interval excludes it.
This is the same discipline as the module-23 note: measure the defense, then attack it.

## Mathematics

**Effect size with error bars.** With $n$ trials per carrier, $\hat p_t$ and $\hat p_p$ each carry a
Wilson interval of roughly width $\frac{2}{\sqrt{n}}$ at 95%. The difference $\hat\Delta$ has a
standard error near $\sqrt{\frac{p_t(1-p_t)+p_p(1-p_p)}{n}}$, so detecting $\Delta = 0.1$ at 95%
confidence needs on the order of

$$ n \gtrsim \frac{(z_{0.975})^2 \cdot 2 p(1-p)}{\Delta^2} \approx \frac{2 \cdot 3.84 \cdot 0.2}{0.01} \approx 154 $$

per carrier. At $\Delta = 0.05$ it is roughly four times that. Small published evaluations of
carrier defenses should be read with that number in mind.

**Erosion.** Model fine-tuning on rendered instructions as closing a fraction $\lambda$ of the gap
per epoch: $\Delta_k = \Delta_0 (1-\lambda)^k$. This is the quantity to put on a dashboard — not
"is the defense deployed", which will stay green forever, but "is the measured gap still non-zero".

**Cost.** Let $c_p$ be credits per pixel-token and $c_t$ per text token. Rasterizing a document of
$n$ characters costs $\approx n \cdot (6 \cdot 8) \cdot c_p$ against $n \cdot c_t$. At typical
relative rates this is one to two orders of magnitude, which is the lab's printed pixel count and
the reason the defense is applied to *untrusted tool output*, not to the whole transcript.

## Attack / Defense model

> [!IMPORTANT]
> **Guarantee analysis — render untrusted content before reading.**
> - **Stops:** injection that depends on being read as a text-channel imperative. In the paper's
>   evaluation this held across ten models and two benchmarks, including against adaptive attackers
>   and human red-teamers, which is why it is worth more than a heuristic filter.
> - **Does NOT stop:** anything carried in the pixels. A pixel-space adversarial perturbation
>   (module 09) or an LSB-steganographic payload (module 20.1) in the same image is unaffected,
>   because the defense changes the carrier of *text*, not the content of *images*. It also does
>   not help when the model's modality gap is already closed — that is the erosion case below.
> - **Attacker adapts:** by targeting the pixels rather than the text (a payload that survives
>   rasterization), or by moving the instruction into a channel the middleware does not cover
>   (alt text, a caption, a filename, an EXIF field). Enumerate the carriers before claiming
>   coverage.
> - **FP cost:** essentially zero on the security axis, which is the honest highlight: there is no
>   classifier to be wrong about. The cost is entirely on the utility and performance axes.
> - **Perf cost:** significant and paid on every untrusted item. Rasterizing is one to two orders
>   of magnitude more expensive per character than text, plus vision-encoder latency. This is why
>   the deployment rule is "untrusted tool output and retrieved documents", not "the whole prompt".
> - **Takeaway:** adopt it for the text channel, measure your own model's gap rather than trusting
>   a published one, and re-measure whenever the model changes — because the mechanism is a
>   training artefact and the defense expires when it is trained away. Pair it with the
>   pixel-channel defenses from module 20.1; it is one of two, not a replacement for them.

> [!NOTE]
> **Reading a guarantee like this one.** "Stops text-channel injection" is a claim about a
> *specific channel of a specific carrier*. Reports go wrong when it is compressed to "mitigates
> multimodal injection". Keep the channel in the sentence, or the reader will not know what is
> covered — which is the failure mode this course's whole guarantee-box pattern exists to prevent.

## Practical lab

**Lab 20.2** ([`labs/module-20/`](../../labs/module-20/README.md)) — a 5×7 bitmap font, the
rasterizing middleware, the measured gap, and the simulated erosion. Offline, stdlib only.

```bash
py labs/module-20/render_defense.py
py -m pytest labs/module-20 -q
```

## Exercise

1. **Measure your own model's gap.** Take a small local multimodal model, run the lab's payloads on both carriers, and report $\hat\Delta$ with a Wilson interval. Does the published ~0.56 hold for it? If not, the defense's value is whatever *your* number says.
2. **Erode it deliberately.** Simulate fine-tuning on rendered instructions and re-measure. Plot $\Delta$ against epochs and state the operational threshold below which you would stop relying on the defense.
3. **Attack the pixel channel.** Add a pixel-space perturbation (module 09's `adv.py`) to the rendered image and show the defense is orthogonal to it. Which module-20.1 control does catch it, and does the combination hold?
4. **Carrier enumeration.** List every place untrusted text can reach a multimodal agent (document body, alt text, caption, filename, EXIF, tooltip, OCR layer). Render one, leave the other three, and measure which the defense actually covers.
5. **Cost at your scale.** Compute the per-document cost multiplier for your real content, then decide the boundary: which items get rasterized and which do not. Write that boundary into the guarantee box.

## Research paper

**Zhang, Baroian, van Rijn, Shafran & Tramèr, "Render Before Reading: converting untrusted text to
images exploits a text/non-text safety-training gap" (2026)**. *Why:* it turns a measured
asymmetry between carriers into a defense that needs no model change, evaluates it broadly, and —
rarely — documents the defense's own erosion condition. *Read:* the direct-injection benchmarks
used; the adaptive-attack and human-red-teamer arms, which are the part that makes the result
worth having; the fine-tuning control that confirms the mechanism. *Reproduce:* the lab is a
from-scratch reimplementation with a stand-in model; extend it per exercise 1. *Limits:* it is a
single recent paper with no independent replication, the gap size is model-specific, and a
provider who fine-tunes on rendered text retires it — so treat the published numbers as a reason
to measure, not as a number to quote.

## Further reading

- Module 20.1 for the pixel channel this defense does not reach; module 06 for the text carriers
  themselves; module 24 for regression-testing the gap when the model changes.
- Bagdasaryan et al. on indirect instruction injection via images, the attack half of this story.

## What you should now be able to do

- Explain the modality gap as a training artefact, and why that makes the defense both effective and erasable.
- Implement a rasterizing middleware from scratch and measure the gap on your own model with error bars.
- State precisely which carriers the defense covers and which it leaves untouched.
- Price the performance cost and decide the boundary at which you would apply it.
