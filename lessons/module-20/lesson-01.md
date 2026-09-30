---
id: "20.1"
module: 20
minutes: 10
practice_minutes: 120
prerequisites: ["01.1", "06.1", "09.1", "10.1"]
objectives:
  - "Distinguish the multimodal sub-threats: **semantic** injection (M06), **steganographic** payloads, **pixel-space adversarial** perturbations, and **document** (PDF) attacks."
  - "Implement **LSB steganography** and measure imperceptibility (MSE, max delta) and the extraction attack."
  - "Explain and (via Stage 4) apply **pixel-space PGD** on a vision classifier; know its threat model."
  - "Apply defenses — **re-encoding/quantization** (LSB-strip), provenance, media-content-as-data — and state exactly which threat each covers."
volatility: current
sources:
  - title: "Bagdasaryan et al. — (Ab)using Images and Sounds for Indirect Instruction Injection"
    url: https://arxiv.org/abs/2302.12173
  - title: "Fridrich et al. — Steganalysis of pixel data (RS analysis)"
    url: https://www.drbobwilliams.com/steganalysis.pdf
  - title: "Athalye, Engstrom, Ilyas, Kwok — Obfuscated Gradients Give a False Sense of Security"
    url: https://arxiv.org/abs/1806.08096
last_verified: "2026-09-30"
---
---
# 20.1 · Multimodal security (deep)

Multimodal models and agents accept images, PDFs, and audio — channels that bypass text filters entirely and can carry either *semantic* instructions (M06) or *bit-level* payloads and *pixel-space* perturbations invisible to humans. This is a distinct, growing surface with its own math and its own defenses.

## Why this matters

An attacker who can't get text past your filters can often get an *image* past them — and hide, in
that image, either an instruction (steganography, invisible text) or a perturbation that flips a
vision model's decision. Neither is visible to a human reviewer. If your pipeline OCRs, extracts
metadata, or feeds pixels to a model, it has a channel no prompt filter inspects.

## Learning objectives

1. Distinguish the multimodal sub-threats: **semantic** injection (M06), **steganographic** payloads,
   **pixel-space adversarial** perturbations, and **document** (PDF) attacks.
2. Implement **LSB steganography** and measure imperceptibility (MSE, max delta) and the extraction
   attack.
3. Explain and (via Stage 4) apply **pixel-space PGD** on a vision classifier; know its threat model.
4. Apply defenses — **re-encoding/quantization** (LSB-strip), provenance, media-content-as-data — and
   state exactly which threat each covers.

## Concept

### Four distinct multimodal threats (different mechanisms, different defenses)

| Threat | Mechanism | Visible to human? | Defended by |
|---|---|---|---|
| Semantic injection (M06) | OCR/alt/metadata *text* the model reads as instructions | sometimes | media-content-as-data, provenance |
| Steganography | payload in pixel **bits** (LSB) | no | re-quantization / LSB-strip |
| Pixel-space adversarial | small perturbation flips a **vision model** | no | adversarial training / certification (M09/M10), re-encoding (partial) |
| Malicious document | PDF metadata, invisible/tiny text, embedded scripts | no | sanitize/re-render, disable active content, provenance |

The critical point: **these need different defenses.** Stripping LSBs defeats steganography but does
nothing against a pixel-space adversarial perturbation (which lives in the high bits) or a semantic
OCR injection. Matching defense to threat model is the whole discipline (M09).

### Steganography (LSB)

Hide bits in the least-significant bit of each pixel. Changing the LSB shifts a pixel by at most 1 —
imperceptible (lab: MSE ~0.05, max delta 1) — yet a byte of payload fits in 8 pixels, so a 64×64
image hides ~512 bytes. A pipeline that extracts hidden data (or a detail-sensitive model) recovers
the injected instruction. **Defense:** re-quantize — zero the LSB plane on ingest — which destroys
the payload with near-zero visual cost (lab: MSE ~0.5, still imperceptible).

### Pixel-space adversarial examples

Exactly the Stage-4 attack (FGSM/PGD/CW), with the image as $x$: find $\delta$, $\|\delta\|\le\epsilon$,
that flips the vision model's output. Human-imperceptible, and it *transfers* (M10) — a real threat to
image classifiers and vision-language models. **Defense:** adversarial training / randomized
smoothing (M09/M10); re-encoding helps against *some* perturbations but is not a guarantee and can be
circumvented by attacks that are robust to the transform (BPDA/EOT — evaluation rigor, M10).

### Malicious documents

PDFs carry metadata, invisible/tiny/white-on-white text (OCR/extraction reads it — M06), and can
embed active content. A "document to summarize" is a rich injection carrier. **Defense:** sanitize
(strip metadata/scripts), re-render to images-then-OCR under provenance, and treat all extracted
content as data.

## Intuition

An image is a wall you can write on in three inks: one a human can read (semantic text), one only a
scanner reads (invisible/OCR text), and one written in the wall's own microscopic texture
(steganographic bits) — plus you can subtly repaint the whole wall so a *machine* misreads it
(adversarial perturbation). Painting over the microscopic texture (re-quantize) erases the third ink
but not the others; you need a different remedy for each, and for the perturbation you must retrain
the machine or blur its vision (smoothing). One "scan images for bad stuff" filter cannot catch all
four.

## Technical explanation

## Mathematics

**Steg capacity & imperceptibility.** LSB embedding changes each used pixel by at most 1, so the
per-pixel error is $\le 1$ and $\text{MSE}\le 1$ regardless of image content — provably imperceptible
by MSE/PSNR. Capacity is 1 bit/pixel (1 byte / 8 pixels); an $H\times W$ image holds $HW/8$ bytes.
**Detectability**, however, is separate from visibility: LSB embedding perturbs the *LSB-plane
statistics* (e.g. it flattens the histogram of value pairs), so a chi-square / RS steganalysis test
can detect it even though a human can't see it — the exercise measures this. Visibility ≠
detectability ≠ removability; a defense (LSB-strip) can *remove* without needing to *detect*.

**Pixel-space vs LSB live in different bits.** An $\ell_\infty$ adversarial perturbation of budget
$\epsilon$ (e.g. 8/255) changes *high-order* bits meaningfully; LSB-strip touches only bit 0, so it
neither creates nor removes the adversarial signal — the mathematical reason one defense does not
cover the other threat model.

## Attack / Defense model

> [!IMPORTANT]
> **Guarantee analysis — re-quantization / LSB-strip (steg defense).**
> - **Stops:** LSB-plane steganographic payloads — deterministically, at negligible visual cost
>   (removes bit 0). No detection needed.
> - **Does NOT stop:** payloads hidden in higher bit-planes or via transform-domain steg, **pixel-space
>   adversarial perturbations** (different bits/threat model), **semantic** OCR/alt/metadata injections
>   (M06), or malicious document scripts.
> - **Attacker adapts:** embed in higher bits (more visible, but re-quantize deeper costs more
>   quality), use transform-domain/robust steg, or switch to semantic/pixel-space channels.
> - **Cost:** minor quality loss; must be applied on *ingest* to all media.
> - **Takeaway:** a cheap, sound defense for *one* channel. Multimodal security requires a **matched
>   set**: re-quantize (steg) + adversarial training/smoothing (pixel-space) + media-content-as-data &
>   provenance (semantic/document). Never assume one media filter covers all four threats.

## Code

`labs/module-20/stego.py`: `embed_lsb`/`extract_lsb` round-trip a payload through pixel LSBs; `mse`
quantifies imperceptibility; `pipeline_extract_and_maybe_exfil` models a pipeline that recovers and
acts on the hidden directive; `strip_lsb` is the re-quantization defense. The header points to reusing
Lab 09's PGD for the pixel-space demonstration.

## Practical lab

**Lab 20** ([`labs/module-20/`](../../labs/module-20/README.md)) — LSB steganography + defense; hook for
pixel-space PGD. numpy, offline.

```bash
py labs/module-20/stego.py
py -m pytest labs/module-20 -q
```

## Exercise

1. **Capacity & detectability.** Measure max payload vs image size; implement a chi-square LSB
   steganalysis test and show the stego image is *detectable* even though imperceptible (visibility ≠
   detectability). Then show LSB-strip *removes* the payload without needing detection.
2. **Higher bit-planes.** Embed in bit 1 or 2; measure the visibility (MSE) and show a single LSB-strip
   misses it — motivating deeper re-quantization and its quality cost.
3. **Pixel-space PGD (reuse Lab 09).** Treat a toy image as classifier input; run PGD to flip its
   label imperceptibly. Show LSB-strip does **not** defend it (different bits), but adversarial
   training does — matching defense to threat model.
4. **Malicious document.** Simulate a PDF whose "invisible text" layer carries an injection (M06);
   show extraction reads it and a sanitize/re-render defense strips it.
5. **Multimodal agent chain (purple team).** Feed a stego/OCR-poisoned image to an agent (M16) whose
   pipeline extracts text; show the confused-deputy exfiltration, then apply the matched defense set
   and re-measure. Write the guarantee box mapping each defense to the threat it covers (and doesn't).

<details><summary>Hint (step 1)</summary>

LSB embedding makes the counts of value pairs $(2k, 2k{+}1)$ nearly equal (it randomizes bit 0),
which a chi-square test on those pair-histograms detects. But detection isn't required to defend:
`strip_lsb` removes the channel unconditionally. Detection matters when you can't re-quantize (e.g.
forensic analysis of received media).

</details>

**Deliverable.** Capacity/steganalysis measurements, the higher-bit-plane result, the pixel-space PGD
+ mismatched-defense demonstration, the malicious-document sim, and the multimodal-agent chain +
matched-defense guarantee box.

## Research paper

**Bagdasaryan et al., "(Ab)using Images and Sounds for Indirect Instruction Injection" (2023)**
(pixel-space multimodal injection) + a **classic LSB steganography/steganalysis** reference (e.g.
Fridrich's RS analysis) + **Athalye et al., "Obfuscated Gradients" / BPDA (2018)** for why
transform-based defenses (like re-encoding) often fail against adaptive attacks. *Why:* the three
pillars — semantic/pixel injection, hidden-bit payloads, and evaluation rigor for transform defenses.
*Read:* Bagdasaryan's injection method; the RS steganalysis idea; BPDA's "don't trust a defense that
just obfuscates gradients." *Reproduce:* the lab's steg + Lab 09's PGD; add a BPDA-style check that
your re-encoding defense doesn't merely obfuscate. *Limits:* real vision-language models are larger;
transfer and robustness are stronger threats than the toy shows.

## Further reading

- OWASP LLM01 (multimodal subtype); NIST AI 100-2 (evasion). Back-links M06, M09, M10.
  [`references/standards-map.md`](../../references/standards-map.md).

## What you should now be able to do

- Distinguish and reproduce the four multimodal attack channels.
- Implement LSB steganography and its re-quantization defense, and measure imperceptibility vs
  detectability.
- Apply pixel-space PGD and explain why it needs a different defense than steganography.
- Assemble a matched multimodal defense set and state what each control covers and misses.