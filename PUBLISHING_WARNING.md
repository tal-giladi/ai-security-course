# Publishing warning — review before making this course public

This course is legitimate professional education in AI/LLM/agent security, but its subject matter is
dual-use by nature. The material below is the honest list of what a reviewer should look at, so the
decision to publish is an informed one rather than a surprise. **Nothing in the course is a weapon
and nothing in it works against a real system**, but a reader could reasonably want to check that
before making it public.

## What the course is

A purple-team curriculum: attacks are built and measured, then defended, then attacked again, so
that a practitioner can both break and harden AI systems they are authorised to test. It is
positioned for defenders, security engineers and researchers.

## What a reviewer should confirm

1. **All offensive work is local and synthetic**, with one documented exception. Every lab except
   Module 34 targets either an intentionally vulnerable app shipped in this repo or an in-process
   mock, on the learner's own machine. There are no real targets, no real credentials, no working
   malware, and no exfiltration endpoints beyond a local sink. Secrets in the labs are synthetic
   canaries of the form `LAB-CANARY-<something>`. Verify by reading `labs/module-*/` and
   `lab/README.md`. Module 34 is reviewed separately in item 7 below.

2. **No network egress from labs.** The labs that use Docker bind services locally and do not route
   traffic off the host. Check any `docker-compose.yml` under `labs/module-*/` for published ports
   and confirm they are localhost-bound or unset.

3. **Payloads demonstrate mechanism, not effect.** Injection strings, jailbreak suffixes and
   poisoning examples end in an inert marker — a canary the learner's own sink records — rather than
   in a destructive or exfiltrating action. Spot-check a few attack scripts.

4. **Named real-world targets appear only as documented public incidents.** Lessons cite real
   products, CVEs and advisories (for example exposed model servers, MCP design issues, published
   vulnerabilities in orchestration platforms). These are references to publicly disclosed events
   and standards, described at the level needed to teach the defense. They are not step-by-step
   instructions against a named live system. Review
   `references/standards-map.md` and the "Real-world examples" sections.

5. **The reconnaissance module (27) is the one to read most carefully.** It teaches how to
   fingerprint AI services and enumerate model infrastructure. The content is standard material from
   any security literature and stays on detection-avoidance framing ("keep your probe rate below the
   defender's alerting threshold", "prefer passive OSINT"), but it is the section a reviewer is most
   likely to want to read personally. The lab is entirely in-process and binds no sockets.

6. **No credential, no malware, no targeting data.** The course does not ship leaked credentials,
   exploit code for an unpatched product, or lists of real targets.

7. **Module 34 is the one to read most carefully after module 27.** It is an optional advanced track
   that breaks the pattern of the rest of the course in two ways, and both are deliberate:

   - **It runs real models.** `labs/module-34/` defaults to
     [`zai-org/GLM-5.3-Flash`](https://huggingface.co/zai-org/GLM-5.3-Flash) — the same
     MIT-licensed model at the centre of the Anthropic 2026-09-29 post — and measures its refusal
     behaviour on published safety benchmarks (JailbreakBench, HarmBench, StrongREJECT). No model
     weights or datasets are committed to git; everything is fetched at runtime by `setup.sh`. The
     lesson also teaches the total-vs-active parameter distinction (320B governs memory, 18B governs
     compute), because getting that backwards is the difference between a $50 job and a $4,400 one.
   - **It modifies weights.** `ablate.py` implements *refusal-direction abliteration* from the
     published Zou et al. paper (arXiv:2406.11717) from scratch — no third-party refusal-removal
     library — and applies a rank-1 projection edit to a local copy of the checkpoint, then
     re-measures and re-iterates. That method is public, peer-visible literature, and the lesson
     labels its own results as the learner's implementation rather than a reproduction of any
     vendor's run. It is explicit that the post published no ablation variant, so a learner's run
     can replicate the study but not the experiment.

   Worth a reviewer knowing: GLM-5.3's weights are MIT-licensed with **no acceptable-use appendix**.
   There is no policy a learner can point at to make this less consequential, which is precisely why
   the module-34 quiz asks learners to reason about what that means rather than to cite a control
   that does not exist.

   What bounds it, and what a reviewer should confirm by reading `labs/module-34/`:

   - **Targets are local only.** The lab operates on a model the learner downloads and hosts. It
     never targets a hosted third-party production API, and it ships no bypass prompt set tuned to
     any specific commercial product.
   - **No harmful corpus in the repo.** Benchmark prompts are fetched at runtime from the public
     datasets. No harmful text, jailbreak string, or jailbreak corpus is committed.
   - **Behaviourally-scored actions are benign.** "Compliance" is measured by whether the model
     emitted a tool call against a local mock endpoint on `127.0.0.1` carrying a `LAB-CANARY-*`
     marker. There is no real target, real credential, or exfiltration endpoint anywhere in it.
   - **Cost is the real caveat, not legality.** It is the only module in the course that requires
     a paid GPU. The lab README carries a cost table and a `> [!WARNING]` before the learner spends
     anything. A reviewer may reasonably want to decide whether the course is free or paid on the
     basis of this module, since it is the part a budget-less learner cannot complete.

   The toy-model labs that teach the same refusal-direction mathematics on CPU, offline and free
   (modules 7 and 25) are unchanged, so no part of this module is required to complete the course.

## Not a concern

- The paper reading guides in `papers/` are study notes on published research.
- The standards crosswalks (OWASP, MITRE ATLAS, NIST) are public frameworks.
- The capstone (module 31) is a simulated environment shipped with the course.

## If you decide to restrict it

`curriculum/course-details.md` has the slug, repo and a suggested free/paid classification. The
Academy can restrict a course at import time; the repo itself may stay public as a docsify site, in
which case the same considerations apply to the Pages build, since it publishes the same markdown.
