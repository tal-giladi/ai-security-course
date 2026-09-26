# Paper curriculum

Research-oriented by design (`plan.md` §25): a *curated* reading list, not a link dump. Papers
are placed exactly where the machinery to understand them exists, and each gets its own guide
under `papers/NN-slug.md` with:

**why it matters · prerequisites · what to understand · which sections to read · what experiment
to reproduce · what code to implement · limitations · what later research changed.**

Only papers that changed the field or teach an essential mechanism are included.

## Placement (verified links added with each guide)

- **Prompt injection / instruction hierarchy** (M04–M06): Greshake et al., *Not what you've
  signed up for* (indirect prompt injection); Wallace et al., *The Instruction Hierarchy*.
- **Jailbreaking** (M07–M08): Zou et al., *Universal and Transferable Adversarial Attacks* (GCG);
  Chao et al., *PAIR*; Mehrotra et al., *TAP*.
- **Adversarial ML** (M09–M10): Goodfellow et al., *Explaining and Harnessing Adversarial
  Examples* (FGSM); Madry et al., *Towards Deep Learning Models Resistant to Adversarial Attacks*
  (PGD); Carlini & Wagner (C&W); Croce & Hein, *AutoAttack*.
- **Poisoning / backdoors** (M11): Gu et al., *BadNets*; Hubinger et al., *Sleeper Agents*.
- **Extraction / privacy** (M12): Tramèr et al., *Stealing Machine Learning Models*; Shokri et
  al., *Membership Inference*; Carlini et al., *Extracting Training Data from LLMs*.
- **RAG security** (M14–M15): Zou et al., *PoisonedRAG*.
- **Agents / tools** (M16–M19): relevant agent-hijacking and tool/MCP security research.
- **Standards** (M26): OWASP LLM Top 10, MITRE ATLAS, NIST AI 100-2.

Each entry becomes a full guide as its module is built. *(No guides written yet — see
`TODO_FOR_TAL.md`.)*
