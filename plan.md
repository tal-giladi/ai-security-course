You are building a complete professional-level course called:

# LLM & Agent Security Research Engineer

The goal is to take me from my current level as an experienced software engineer and LLM learner to **expert-level capability in LLM, generative-AI, and agent security research and engineering**.

This should NOT be a shallow "prompt injection course" or a collection of OWASP articles.

I want a course comparable in depth and seriousness to a professional university/research curriculum combined with advanced red-team/blue-team security training.

I am already studying a separate course called:

**`llm-research-engineer-course`**

You have access to that course/project. Inspect it carefully before designing this course.

Use it as a prerequisite/reference point.

Do NOT unnecessarily duplicate material that I already learn there. Instead:

1. Identify what the existing course already teaches.
2. Identify the security-relevant prerequisites it provides.
3. Build on those foundations.
4. Explicitly fill gaps where security requires additional depth.
5. When something is already sufficiently covered there, link/reference it rather than reproducing an inferior duplicate.

The two courses should eventually form a coherent professional learning path.

---

# 1. PRIMARY GOAL

The end result should prepare me to work professionally as an:

* LLM Security Engineer
* AI Security Engineer
* LLM Red Team Engineer
* AI/Agent Security Researcher
* AI Security Architect
* AI/LLM Application Security Engineer

I want to understand not only **how to attack LLM systems**, but WHY the attacks work, how to mathematically analyze them where appropriate, how to build attacks experimentally, how to detect them, how to mitigate them, and how to research new attacks and defenses.

The course must teach me to think like both:

**RED TEAM**
and
**BLUE TEAM**

with a strong emphasis on:

**PURPLE TEAM / security research**

The ultimate capability should be:

> Given a new LLM/agent architecture that I have never seen before, I should be able to analyze its attack surface, formulate realistic attacks, build experiments to validate them, design defenses, measure whether those defenses actually work, and conduct further security research.

---

# 2. FIRST: AUDIT MY EXISTING LLM RESEARCH ENGINEER COURSE

Before creating the curriculum:

Inspect the existing `llm-research-engineer-course`.

Create an internal dependency map covering:

* mathematics
* probability/statistics
* linear algebra
* optimization
* neural networks
* transformers
* attention
* training
* fine-tuning
* RL / RLHF / preference optimization
* inference
* quantization
* embeddings
* RAG
* evaluation
* agents
* tool use
* model serving
* distributed systems
* etc.

Determine what I already know or will learn there.

Then design this course so that:

```text
LLM Research Engineer
        ↓
LLM & Agent Security Research Engineer
```

is a coherent progression.

Do not assume that because a topic exists in the other course it should be completely omitted. Security sometimes requires a more specialized treatment.

For example:

The other course may explain embeddings.

This course should still teach:

* embedding-space attacks
* malicious embeddings
* retrieval manipulation
* nearest-neighbor attack surfaces
* poisoning
* cross-tenant retrieval leakage
* mathematical analysis of retrieval behavior

but should not reteach basic embeddings from scratch unless necessary.

---

# 3. RESEARCH HOW PROFESSIONAL CURRICULA ARE BUILT

Before writing the curriculum, research how high-quality professional programs in the following areas are structured:

* cybersecurity
* penetration testing
* red teaming
* adversarial machine learning
* AI security
* LLM security
* machine learning research
* security engineering

Use strong sources.

Look at programs and materials from organizations/universities such as:

* Stanford
* MIT
* CMU
* Berkeley
* Oxford
* ETH
* SANS
* OWASP
* NIST
* MITRE
* Microsoft
* Google
* Anthropic
* OpenAI
* Meta
* NVIDIA
* reputable AI security organizations
* major security conferences
* major ML conferences

Do not blindly copy their curricula.

Extract the underlying principles:

* prerequisite structure
* progression of difficulty
* theory → implementation
* labs
* assessment
* research projects
* capstone projects
* professional competencies

The resulting curriculum should feel deliberately engineered rather than assembled from web articles.

---

# 4. COURSE STRUCTURE

Build a complete curriculum with multiple stages.

At minimum cover:

## Stage 1 — Security Foundations

Teach the security concepts required to reason about AI systems:

* threat modeling
* attack surfaces
* trust boundaries
* privilege
* authentication
* authorization
* isolation
* sandboxing
* secrets
* data flows
* APIs
* web application security
* supply-chain security
* dependency attacks
* SSRF
* code execution
* injection concepts
* confused deputy problems
* privilege escalation
* data exfiltration

Do not turn this into a generic cybersecurity course.

Only teach traditional security concepts deeply enough to understand AI security.

---

# 5. LLM SECURITY FOUNDATIONS

Teach the security implications of:

* tokenization
* context windows
* attention
* instruction following
* system/user/tool message hierarchy
* training vs inference
* alignment
* RLHF
* preference optimization
* safety training
* refusal behavior
* model behavior boundaries
* model specification
* inference APIs
* streaming
* structured output
* function calling
* tool calling

Explain where the security boundaries actually exist.

For every security mechanism ask:

> What does the mechanism actually guarantee?

and:

> What does it NOT guarantee?

This distinction is extremely important.

---

# 6. PROMPT INJECTION

Cover prompt injection deeply.

Do NOT teach only simple examples.

Include:

* direct prompt injection
* indirect prompt injection
* multi-turn injection
* context manipulation
* instruction hierarchy attacks
* delimiter attacks
* encoding attacks
* obfuscation
* multilingual attacks
* tokenization-aware attacks
* instruction smuggling
* retrieved-document injection
* webpage injection
* email injection
* image/multimodal injection
* cross-agent injection
* memory injection
* tool-result injection
* delayed execution attacks
* persistent attacks

Teach the underlying reason these attacks work.

Include research papers and experiments.

Where meaningful, include mathematical analysis.

---

# 7. JAILBREAKING

Teach jailbreaks as a research topic, not merely a list of prompts.

Cover:

* optimization-based jailbreaks
* automated jailbreak generation
* adversarial suffixes
* universal adversarial attacks
* gradient-based methods
* gradient-free attacks
* black-box attacks
* transferability
* evolutionary attacks
* search-based attacks
* multi-turn jailbreaks
* role/context attacks
* adaptive attacks
* automated red teaming

Where appropriate, derive the mathematics.

For example, if an attack can be formulated as:

```text
argmax_x L(model(x))
```

or an equivalent optimization/search problem, explain:

* objective
* variables
* constraints
* optimization method
* why it works
* computational cost
* limitations

Do not hide the mathematics behind libraries.

---

# 8. ADVERSARIAL MACHINE LEARNING

This should be a substantial section.

Cover:

* adversarial examples
* white-box attacks
* black-box attacks
* transfer attacks
* FGSM
* PGD
* CW
* AutoAttack
* optimization-based attacks
* adversarial perturbations
* robustness
* certified robustness
* poisoning
* backdoors
* trojans
* model extraction
* model inversion
* membership inference
* data reconstruction
* training-data extraction

Teach the mathematical foundations.

Include equations where necessary.

I want to understand the algorithms, not simply run them.

---

# 9. MODEL-LEVEL SECURITY

Cover attacks against the model itself:

* training-data poisoning
* fine-tuning poisoning
* preference-data poisoning
* backdoors
* sleeper-agent style behavior
* model extraction
* model stealing
* model inversion
* membership inference
* training-data memorization
* data extraction
* malicious fine-tunes
* malicious adapters
* LoRA/adaptor security
* model supply-chain attacks
* compromised model weights
* malicious checkpoints

Include realistic experiments where possible.

---

# 10. RAG SECURITY

Build a complete RAG security module.

Cover:

* document poisoning
* retrieval manipulation
* embedding manipulation
* malicious documents
* indirect prompt injection
* retrieval authorization failures
* cross-user leakage
* cross-tenant leakage
* metadata attacks
* vector database attacks
* malicious chunking
* poisoned knowledge bases
* stale data
* source spoofing
* citation manipulation
* retrieval denial of service
* malicious tool/retrieval results

Include mathematical understanding of:

* embeddings
* similarity
* nearest-neighbor retrieval
* cosine similarity
* distance metrics
* ranking
* reranking
* ANN indexes
* HNSW where relevant

I should understand how to reason about manipulating retrieval mathematically.

---

# 11. AGENT SECURITY

This must be one of the largest sections.

Modern AI security is increasingly about agents.

Cover:

* tool calling
* function calling
* autonomous agents
* agent loops
* planning
* memory
* external state
* permissions
* credentials
* APIs
* browser agents
* code agents
* multi-agent systems

Security topics:

* excessive agency
* confused deputy
* tool abuse
* privilege escalation
* tool poisoning
* malicious tool descriptions
* malicious tool results
* indirect prompt injection
* agent hijacking
* credential theft
* secret exfiltration
* arbitrary code execution
* filesystem attacks
* network attacks
* SSRF through agents
* destructive actions
* persistence
* memory poisoning
* cross-agent attacks
* agent-to-agent trust
* malicious MCP servers
* malicious MCP tools
* MCP security
* tool authorization
* capability-based security
* least privilege
* approval gates
* human-in-the-loop security

Include realistic multi-step attack chains.

For example:

```text
malicious webpage
    ↓
browser agent reads page
    ↓
indirect prompt injection
    ↓
agent invokes tool
    ↓
tool accesses credential
    ↓
credential exfiltration
```

Then build the corresponding defense.

---

# 12. MCP SECURITY

Treat MCP as an important modern attack surface.

Research the current MCP specification and ecosystem.

Cover:

* MCP architecture
* clients
* servers
* tools
* resources
* prompts
* transports
* authentication
* authorization
* trust boundaries
* malicious servers
* malicious tools
* tool poisoning
* prompt injection through MCP
* data exfiltration
* confused deputy
* capability escalation
* supply-chain risks
* server verification
* sandboxing
* permission models

Because this area changes quickly, design this section so it can be updated independently.

---

# 13. MULTIMODAL SECURITY

Cover:

* image prompt injection
* document injection
* OCR attacks
* visual adversarial examples
* malicious PDFs
* hidden instructions
* invisible text
* image steganography
* audio injection
* video attacks
* cross-modal attacks
* multimodal agent attacks

Build practical labs.

---

# 14. CODE AGENT SECURITY

Create a major section around coding agents.

Cover:

* malicious repositories
* malicious README files
* poisoned dependencies
* package attacks
* build scripts
* post-install scripts
* secrets
* environment variables
* CI/CD attacks
* shell command execution
* arbitrary code execution
* prompt injection in source code
* malicious tests
* malicious issues/PRs
* dependency confusion
* supply-chain attacks

Build realistic local labs.

---

# 15. AI SUPPLY-CHAIN SECURITY

Cover:

* model hubs
* model files
* checkpoints
* safetensors
* pickle risks
* tokenizer files
* configuration files
* LoRA adapters
* datasets
* Python packages
* Docker images
* inference servers
* plugins
* MCP servers
* external APIs

Teach how an AI system can be compromised through dependencies rather than the model itself.

---

# 16. BLUE TEAM

For every significant offensive technique, teach the corresponding defensive engineering.

Cover:

* input filtering
* output validation
* structured outputs
* policy enforcement
* authorization
* capability isolation
* sandboxing
* container isolation
* network isolation
* secret isolation
* tool permissions
* least privilege
* allowlists
* deny lists
* provenance
* content security
* retrieval filtering
* data classification
* monitoring
* anomaly detection
* attack detection
* rate limiting
* abuse prevention
* audit logs
* incident response

Do not present defenses as magic solutions.

For every defense ask:

```text
What attack does it stop?
What attack does it NOT stop?
How can an attacker adapt?
What is the false-positive cost?
What is the performance cost?
```

---

# 17. SECURITY EVALUATION

Teach how to evaluate an AI system systematically.

Cover:

* attack success rate
* refusal rate
* false positives
* false negatives
* robustness
* attack transferability
* detection precision/recall
* attack coverage
* regression testing
* benchmark design
* evaluation datasets
* automated evaluation
* human evaluation
* adaptive evaluation
* red-team methodology

Teach me to design my own security benchmarks.

---

# 18. AUTOMATED RED TEAMING

Build a complete section around automated attacks.

Cover:

* attack generation
* mutation
* fuzzing
* prompt mutation
* search
* optimization
* evolutionary approaches
* model-based attackers
* attacker/defender models
* automated exploit chains
* automated tool-use attacks
* agentic red teaming

Include implementations.

---

# 19. PURPLE TEAM

The course should repeatedly use this cycle:

```text
ATTACK
   ↓
OBSERVE
   ↓
DETECT
   ↓
MITIGATE
   ↓
RETEST
   ↓
ADAPT ATTACK
   ↓
MEASURE
```

Labs should not end after successfully exploiting something.

I want to implement the defense and then attempt to defeat my own defense.

---

# 20. LOCAL SECURITY LAB

This is mandatory.

The entire course should be designed around a local lab environment.

Use Docker wherever practical.

Create a central lab architecture such as:

```text
llm-security-lab/
    ├── models/
    ├── vulnerable-apps/
    ├── agents/
    ├── rag/
    ├── vector-db/
    ├── attack-tools/
    ├── defense-tools/
    ├── monitoring/
    ├── datasets/
    ├── docker-compose/
    └── labs/
```

Prefer open-source models that can run locally.

Use small models where possible so the labs remain practical.

When larger models are genuinely necessary, clearly identify that requirement.

---

# 21. OPEN-SOURCE SECURITY PROJECTS

Research and incorporate useful existing projects.

Examples may include:

* AI Goat
* Garak
* PyRIT
* Promptfoo
* Giskard
* Inspect AI
* ART
* TextAttack
* SecML
* Lakera-style concepts where reproducible locally
* OWASP resources
* MITRE ATLAS
* other serious open-source AI security projects

But:

**DO NOT make the course dependent on any external project.**

External projects frequently:

* change APIs
* break
* disappear
* become unmaintained
* change installation procedures
* require cloud services

Therefore every external dependency must have a fallback.

For every external project used in a lab:

```text
External Tool
      ↓
Primary Lab
      ↓
Local Minimal Reimplementation
      ↓
Fallback Exercise
```

The student must still be able to complete the learning objective if the external project stops working.

For important attacks, implement simplified versions ourselves.

For example:

If AI Goat demonstrates an attack:

1. Use AI Goat if useful.
2. Understand its implementation.
3. Build our own minimal vulnerable application.
4. Perform the attack against our application.
5. Implement the defense.
6. Retest.

This principle should apply throughout the course.

---

# 22. DOCKER REQUIREMENTS

All practical exercises should preferably be reproducible with:

```bash
docker compose up
```

or an equivalent documented command.

Provide:

* Dockerfiles
* docker-compose files
* environment configuration
* seed data
* vulnerable applications
* test scripts
* attack scripts
* defense implementations
* reset scripts
* cleanup scripts

The labs must be isolated from my real machine as much as reasonably possible.

Never require attacking real external systems.

All offensive exercises must target:

* local containers
* intentionally vulnerable applications
* explicitly authorized lab environments
* synthetic data

---

# 23. REALISTIC LABS

Do NOT create trivial exercises such as:

> "Send this prompt and see if the model says something bad."

I want realistic security engineering exercises.

Examples:

### Lab: RAG poisoning

Build:

```text
Document ingestion
       ↓
Embedding
       ↓
Vector DB
       ↓
Retriever
       ↓
LLM
```

Poison the knowledge base.

Measure retrieval changes.

Exploit the system.

Implement defenses.

Measure the defense.

---

### Lab: Agent credential theft

Build an agent with:

* tools
* filesystem access
* fake credentials
* HTTP access
* sensitive files

Create an indirect injection attack that attempts to exfiltrate a fake secret.

Then progressively implement:

* permission restrictions
* sandboxing
* network controls
* tool authorization
* detection

Measure each defense.

---

### Lab: MCP tool poisoning

Create:

```text
MCP client
     ↓
trusted tool
     ↓
malicious/poisoned tool
```

Demonstrate the attack.

Then implement a security model.

---

### Lab: Model extraction

Deploy a local model API.

Treat the model as a black box.

Attempt to reconstruct its behavior.

Measure query cost and fidelity.

---

### Lab: Membership inference

Use a controlled dataset.

Train a small model.

Implement membership inference.

Measure the attack.

Then investigate mitigation.

---

# 24. MATHEMATICS

This is important.

Do NOT turn this into a purely application-security course.

Where mathematical understanding is relevant, teach it properly.

Include:

* probability
* information theory
* optimization
* gradients
* loss functions
* statistical hypothesis testing
* distributions
* entropy
* KL divergence
* cross entropy
* cosine similarity
* vector spaces
* matrix operations
* adversarial optimization
* constrained optimization
* statistical inference
* ROC/AUC
* precision/recall
* confidence intervals
* hypothesis testing
* information leakage
* differential privacy concepts where relevant

For mathematical attacks:

1. explain the intuition
2. define the mathematical formulation
3. derive the important equations
4. implement it from scratch
5. compare it with an existing library
6. run the experiment
7. analyze the results

Do not allow libraries to hide the underlying algorithm.

---

# 25. PAPERS

This must be research-oriented.

For every major subject identify important papers.

Prefer:

* original papers
* high-quality conference papers
* major security research
* official technical reports
* authoritative standards

Relevant venues include:

* USENIX Security
* IEEE S&P
* ACM CCS
* NDSS
* NeurIPS
* ICML
* ICLR
* ACL
* EMNLP
* AAAI
* SaTML
* Black Hat research
* DEF CON research

Do not simply collect hundreds of papers.

Select the papers that actually changed the field or teach an important concept.

For each required paper provide:

* why it matters
* prerequisites
* what to understand
* which sections to read
* what experiment to reproduce
* what code to implement
* what limitations it has
* what later research changed

---

# 26. RESEARCH REPRODUCTION

The advanced stages should require reproducing published attacks.

Examples:

```text
Read paper
   ↓
Understand attack
   ↓
Implement minimal version
   ↓
Run experiment
   ↓
Compare with paper
   ↓
Explain differences
   ↓
Attempt improvement
```

This is important because the goal is expert-level security research rather than tool usage.

---

# 27. CAPSTONE PROJECTS

Create several increasingly difficult capstones.

At least:

### Capstone 1

Secure a vulnerable LLM application.

### Capstone 2

Red-team a RAG application.

### Capstone 3

Red-team an autonomous agent.

### Capstone 4

Build a complete AI security evaluation framework.

### Capstone 5 — Research project

Design and investigate a novel security hypothesis.

The final project should resemble a small academic security research project:

```text
Hypothesis
↓
Threat model
↓
Related work
↓
Attack design
↓
Implementation
↓
Experiments
↓
Measurements
↓
Defense
↓
Adaptive attack
↓
Results
↓
Limitations
↓
Future work
```

---

# 28. PROGRESS TRACKER

The course must have a persistent progress tracker.

Because the course is learned through GitHub Pages, create a GitHub-friendly progress system.

For example:

```text
progress/
    roadmap.md
    progress.json
    stage-01.md
    stage-02.md
    ...
```

Each lesson should have:

* status
* prerequisites
* completion checkbox
* lab completion
* exercises
* papers
* implementation tasks
* assessment
* confidence level

Use GitHub-compatible Markdown.

Progress should be easy to update through commits.

If practical, create a visual GitHub Pages dashboard.

---

# 29. GITHUB PAGES

The entire course must be designed for GitHub Pages.

I want:

* navigation
* sidebar
* searchable lessons if practical
* curriculum roadmap
* progress tracker
* code examples
* equations
* diagrams
* lab instructions
* references
* paper links
* project links
* prerequisites
* estimated time
* difficulty level

The site should work well on desktop.

Do not make the course dependent on a proprietary learning platform.

The repository itself should remain useful if GitHub Pages is disabled.

---

# 30. LESSON FORMAT

Every lesson should use a consistent structure:

```text
# Lesson

## Why this matters

## Learning objectives

## Prerequisites

## Concept

## Intuition

## Technical explanation

## Mathematics

## Attack / Defense model

## Real-world examples

## Code

## Practical lab

## Exercise

## Research paper

## Further reading

## Assessment

## What you should now be able to do

## Progress checkpoint
```

Do not force every section into tiny lessons.

Lessons should be long enough to actually teach the concept.

---

# 31. TEACHING STYLE

The teaching should be similar to a strong university instructor + experienced security researcher.

For difficult concepts:

1. intuition
2. simple example
3. formal definition
4. mathematics
5. implementation
6. realistic example
7. attack
8. defense
9. limitations

Do not assume I understand a security concept simply because I am a software engineer.

At the same time, do not explain basic programming concepts unnecessarily.

I am an experienced C#/.NET software engineer.

Use:

* Python for ML/security experiments
* C# where it provides useful real-world integration examples
* Docker
* Linux/WSL
* Git/GitHub

---

# 32. ASSESSMENT

Do not make the course merely passive reading.

Use:

* conceptual questions
* mathematical exercises
* implementation exercises
* attack exercises
* defense exercises
* debugging exercises
* threat-modeling exercises
* research exercises

Exercises should require reasoning.

Avoid trivial:

> "Run this command."

Instead:

> "The system has these trust boundaries. Find the attack path."

or:

> "Modify the attack so the existing defense no longer detects it."

---

# 33. SECURITY BOUNDARIES

The course is for authorized security research.

All offensive labs must use controlled environments.

Build intentionally vulnerable local applications and fake credentials/data.

Never design exercises around compromising real systems.

The emphasis is:

**understand → reproduce → exploit locally → defend → evaluate**

---

# 34. VERSIONING AND MAINTENANCE

LLM security changes extremely quickly.

Design the curriculum so that the stable foundations are separated from fast-moving material.

For example:

```text
FOUNDATION
    ↓
CURRENT TECHNOLOGY
    ↓
FAST-MOVING MODULES
```

MCP, agent frameworks, model APIs, tools, and attack techniques should be modular.

Do not rewrite the entire course every time a framework changes.

Prefer teaching underlying security principles and maintaining small technology-specific modules.

---

# 35. EXTERNAL RESOURCE FAILURE POLICY

For EVERY external:

* GitHub repository
* Docker image
* model
* dataset
* website
* API
* framework
* security tool

record:

```text
Primary source
Version/date
Purpose
License
Installation
Known failure modes
Fallback
Local alternative
```

Never make a core learning objective dependent on a single external repository.

If a GitHub repository disappears tomorrow, I should still be able to complete the lesson.

---

# 36. CURRENT INFORMATION

Because this field changes rapidly, research the current state of:

* LLM security
* agent security
* MCP security
* AI red teaming
* adversarial ML
* RAG security
* model security
* AI supply chain
* AI security evaluation

Do not rely on outdated 2023-era LLM security material when newer research has substantially changed the understanding.

At the same time, do not replace foundational material merely because it is old.

Distinguish:

```text
FOUNDATIONAL
CURRENT
EMERGING
DEPRECATED
```

where appropriate.

---

# 37. STANDARDS AND FRAMEWORKS

Integrate relevant standards/frameworks, including where applicable:

* OWASP Top 10 for LLM Applications
* OWASP Agentic AI resources
* MITRE ATLAS
* NIST AI Risk Management Framework
* NIST adversarial ML material
* relevant NIST cybersecurity standards
* relevant ISO standards
* model/system security frameworks

Do not teach these as memorization exercises.

Map them to actual attacks and labs.

For example:

```text
OWASP category
      ↓
Threat
      ↓
Concrete vulnerability
      ↓
Local vulnerable application
      ↓
Attack
      ↓
Defense
      ↓
Test
```

---

# 38. FINAL COMPETENCY MAP

At the end of the course create a competency matrix.

For every major capability:

```text
Capability
Theory
Mathematics
Implementation
Attack
Defense
Research
Assessment
```

I should be able to see exactly what I can do after completing the course.

---

# 39. DO NOT RUSH THE CURRICULUM

Do not immediately start generating hundreds of lesson files.

First:

1. inspect my existing LLM Research Engineer course
2. research professional curricula
3. research current LLM/AI security curricula
4. identify authoritative sources
5. build the dependency graph
6. build the complete curriculum
7. identify overlaps with my existing course
8. identify missing prerequisites
9. design the lab architecture
10. design the progress system
11. only then generate the course content

Create a clear master curriculum before generating all lessons.

The curriculum should be large enough to genuinely produce expert-level capability.

Do not artificially limit the course to a convenient number of weeks or lessons.

---

# 40. IMPORTANT QUALITY REQUIREMENT

Do not optimize for the number of topics.

Optimize for **depth and capability**.

I would rather have:

```text
50 extremely good lessons
```

than:

```text
300 shallow lessons
```

The same applies to tools and papers.

The course should teach me to understand and independently solve new AI security problems, not merely recognize names such as:

* prompt injection
* jailbreak
* RAG poisoning
* model extraction
* agent hijacking

I want to understand the mechanisms underneath them.

---

# 41. FINAL DELIVERABLE

Create the complete repository with:

```text
course/
├── README.md
├── curriculum/
├── lessons/
├── labs/
├── exercises/
├── projects/
├── papers/
├── references/
├── progress/
├── tools/
├── docker/
├── datasets/
├── scripts/
└── docs/
```

Include:

* complete curriculum
* dependency graph
* GitHub Pages site
* progress tracker
* Docker lab infrastructure
* lesson templates
* practical labs
* exercises
* attack implementations
* defense implementations
* research-paper reading list
* research reproduction projects
* capstones
* setup documentation
* troubleshooting
* external-tool fallback strategy

The final course should feel like a serious **LLM/Agent Security Research Engineer program**, not an online tutorial.

The central philosophy is:

> **Understand the system → understand the attack surface → understand the mathematics → reproduce the attack → build the exploit → build the defense → attack the defense → measure the result → read the research → develop new attacks and defenses.**

Build the curriculum around that principle.

#Very important:
Every learning material must have a corresponding practical exercise. Do not allow any significant concept, technique, attack, defense, mathematical method, framework, or security principle to be taught only theoretically. For each learning material, create at least one hands-on exercise that requires me to actually apply what I learned, preferably in the local Docker lab. Exercises should progress from implementation and experimentation to realistic security scenarios and should require reasoning rather than simply following commands. For attack topics, I should actually construct, execute, analyze, and measure the attack; for defense topics, I should implement the defense and then attempt to bypass or defeat it; for mathematical topics, I should implement the relevant mathematics from scratch and use it in an actual security experiment. When appropriate, include multiple exercises of increasing difficulty, culminating in a realistic, non-trivial scenario that combines the material with concepts from previous lessons. A lesson should not be considered complete until its practical exercise has been completed.