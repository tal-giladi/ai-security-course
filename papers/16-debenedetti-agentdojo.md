# Debenedetti et al. — *AgentDojo: A Dynamic Environment to Evaluate Attacks and Defenses for LLM Agents* (2024)

**arXiv:** [2406.13352](https://arxiv.org/abs/2406.13352) · NeurIPS '24 D&B. **Modules:** [16.1](../lessons/module-16/lesson-01.md), [18.1](../lessons/module-18/lesson-01.md), [24.1](../lessons/module-24/lesson-01.md), [25.1](../lessons/module-25/lesson-01.md). **Labs:** [Lab 16](../labs/lab-16/README.md), [Lab 18](../labs/lab-18/README.md).

## Why it matters
AgentDojo is the reference **benchmark** for the exact threat this course's agent stage builds: prompt-injection attacks against **tool-using agents**, measured on realistic multi-step tasks with *both* a utility metric (did the agent still do the job?) and a security metric (did the injection succeed?). It replaces anecdotes ("we jailbroke the agent") with a reproducible environment, and its two-axis scoring is the model for the guarantee-box thinking (a defense that tanks utility is not a win). It is the natural target paper for M16–M18 and the eval/red-team modules.

## Prerequisites
- Sibling course: agents, tool calling, planning loops.
- This course: [16.1 agent attack surface](../lessons/module-16/lesson-01.md), [05.1 indirect injection](../lessons/module-05/lesson-01.md), [24.1 evaluation](../lessons/module-24/lesson-01.md).

## What to understand
- **Two metrics, always:** benign task utility **and** attack success rate — a defense is only meaningful reported against both (the utility/security frontier).
- **Dynamic environment:** tasks with real tool state and injected content in tool results/data, so injections must survive a *multi-step* execution, not a single turn.
- **Attacks and defenses as pluggable components** — the harness *is* a purple-team loop, which is precisely the shape of the shared agent runtime you build.

## Which sections to read
- §3 (environment + task/injection design), §4 (the utility + attack-success metrics), §5 (baseline attacks/defenses and how weak current defenses are).

## Experiment to reproduce (locally)
Labs 16 and 18 are a miniature AgentDojo: the shared `lab/agents` runtime runs a multi-step task, an indirect injection in a tool result drives a confused-deputy exfiltration, and each defense (least privilege, egress allowlist, approval gate) is scored on **both** whether it blocks the attack *and* whether the benign task still completes. Build the two-axis table across defenses — that table is the paper's contribution in miniature.

## Code to implement
- A two-axis scorer (task-utility × attack-success) over the agent runtime, wired into [`evalkit`](../lab/attack-tools/evalkit.py) with Wilson CIs.
- A defense-comparison harness: run each `Policy` against benign + attack task suites and plot the utility/security frontier.

## Limitations
- The lab's rule-engine brain is a deterministic stand-in for a tool-calling LLM (reproducibility over fidelity — state it); AgentDojo uses real models.
- Benchmarks measure *known* attacks; a passing score is not a safety guarantee (the standing course caveat).

## What later research changed
- Established the norm that agent-security papers report utility **and** attack success; feeds directly into automated red teaming ([25.1](../lessons/module-25/lesson-01.md)) as the environment to search against.
- Related agent-injection/hijack benchmarks (InjecAgent and successors) extend the tool/coverage surface.
