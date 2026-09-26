# Paper curriculum

Research-oriented by design (`plan.md` §25): a *curated* reading list, not a link dump. Papers
are placed exactly where the machinery to understand them exists, and each gets its own guide
under `papers/NN-slug.md` with:

**why it matters · prerequisites · what to understand · which sections to read · what experiment
to reproduce · what code to implement · limitations · what later research changed.**

Only papers that changed the field or teach an essential mechanism are included.

## Reading guides

Each guide: why it matters · prerequisites · what to understand · which sections to read · what
experiment to reproduce (locally) · what code to implement · limitations · what later research changed.

**Prompt injection / instruction hierarchy** (M04–M06)
- [01 · Greshake et al. — *Not what you've signed up for* (indirect prompt injection)](01-greshake-indirect-injection.md)
- [02 · Wallace et al. — *The Instruction Hierarchy*](02-wallace-instruction-hierarchy.md)

**Jailbreaking** (M07–M08)
- [03 · Zou et al. — *Universal and Transferable Adversarial Attacks* (GCG)](03-zou-gcg.md)
- [04 · Chao et al. — *Jailbreaking Black Box LLMs in Twenty Queries* (PAIR)](04-chao-pair.md)
- [05 · Mehrotra et al. — *Tree of Attacks* (TAP)](05-mehrotra-tap.md)

**Adversarial ML** (M09–M10)
- [06 · Goodfellow et al. — *Explaining and Harnessing Adversarial Examples* (FGSM)](06-goodfellow-fgsm.md)
- [07 · Madry et al. — *Towards Deep Learning Models Resistant to Adversarial Attacks* (PGD)](07-madry-pgd.md)
- [08 · Carlini & Wagner — *Towards Evaluating the Robustness of Neural Networks* (C&W)](08-carlini-wagner.md)
- [09 · Croce & Hein — *AutoAttack*](09-croce-autoattack.md)

**Poisoning / backdoors** (M11)
- [10 · Gu et al. — *BadNets*](10-gu-badnets.md)
- [11 · Hubinger et al. — *Sleeper Agents*](11-hubinger-sleeper.md)

**Extraction / privacy** (M12)
- [12 · Tramèr et al. — *Stealing Machine Learning Models via Prediction APIs*](12-tramer-stealing.md)
- [13 · Shokri et al. — *Membership Inference Attacks* (+ Carlini LiRA)](13-shokri-membership.md)
- [14 · Carlini et al. — *Extracting Training Data from LLMs*](14-carlini-extracting.md)

**RAG security** (M14–M15)
- [15 · Zou et al. — *PoisonedRAG*](15-zou-poisonedrag.md)

**Agents / tools** (M16–M19, M24–M25)
- [16 · Debenedetti et al. — *AgentDojo*](16-debenedetti-agentdojo.md)

**Standards** (M26) — full tables in [`references/standards-map.md`](../references/standards-map.md):
OWASP LLM Top 10, MITRE ATLAS, NIST AI 100-2 / AI RMF.
