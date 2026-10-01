"""Lab 14.2 — Denial of wallet.

A tool-calling agent's context grows with every turn. When a host runtime carries a previous
tool's return value into later model turns, the provider re-meters that content on every
subsequent call. An untrusted or compromised tool can therefore convert data it already had into
recurring, victim-billed inference cost — no stolen credential, no local privilege, no exfiltration.
The attacker's goal is not the data and not an unauthorized action. The goal is the bill.

This lab builds the mechanism, measures it, and prices two defenses against each other:

  1. The mechanism - a persistent billable state that grows with every turn.
  2. The arithmetic - cumulative input inflation as a multiple of the initiating call.
  3. Defense A: blunt truncation / deletion of history. Cheap, and it breaks the task.
  4. Defense B: compression that preserves what the task needs. More expensive per turn, and
     it keeps the task working.
  5. Defense C: a fixed context/cost cap. Predictable, and it interrupts work.
  6. Measure the utility each defense costs, so the trade-off is a number rather than an opinion.

Run: py labs/module-14/denial_of_wallet.py
"""
from __future__ import annotations

import random

# The victim bills for input tokens on every call. Rates are illustrative, in credits per 1K tokens.
RATE_PER_1K = 0.003
INITIATING_CALL_TOKENS = 400


class Session:
    """A host runtime that carries tool output forward into later model turns."""

    def __init__(self, budget_credits: float = 2.0, cap: int | None = None,
                 mode: str = "retain") -> None:
        self.budget = budget_credits
        self.cap = cap
        self.mode = mode  # retain | delete | compress | progress_authorized
        self.history: list[str] = []
        self.billed = 0.0
        self.turns = 0
        self.completed = 0
        self.rng = random.Random(4)

    # --- billing ---------------------------------------------------------------------
    def context_tokens(self) -> int:
        return INITIATING_CALL_TOKENS + sum(len(t) for t in self.history)

    def call(self) -> float:
        """One model turn. The provider bills the whole context, every time."""
        self.turns += 1
        cost = self.context_tokens() / 1000 * RATE_PER_1K
        if self.cap is not None and self.context_tokens() > self.cap:
            cost = self.context_tokens() / 1000 * RATE_PER_1K * 0.1  # truncated request, cheaper
        self.billed += cost
        return cost

    # --- the tool --------------------------------------------------------------------
    def tool_result(self, size: int) -> None:
        """A tool returns `size` characters. A hostile tool returns a lot, every turn."""
        payload = "x" * size
        if self.mode == "delete":
            self.history = []  # blunt: drop everything
        elif self.mode == "compress":
            # Keep a summary-sized residue: enough for the task, not the payload.
            self.history = [payload[:64]]
        elif self.mode == "progress_authorized":
            # Only retain while the task is unfinished; completed steps are dropped.
            self.history = [payload[:96]] if self.completed < 4 else []
        else:
            self.history.append(payload)

    def finish_turn(self) -> None:
        self.call()
        self.completed += 1


def inflation(turns: int, tool_size: int) -> float:
    """Cumulative input as a multiple of the initiating call."""
    s = Session(mode="retain")
    for _ in range(turns):
        s.tool_result(tool_size)
        s.finish_turn()
    return round(s.context_tokens() / INITIATING_CALL_TOKENS, 2)


def attack_scenario(turns: int = 12, tool_size: int = 4000) -> Session:
    s = Session(mode="retain")
    for _ in range(turns):
        s.tool_result(tool_size)
        s.finish_turn()
    return s


def table(turns: int = 12, tool_size: int = 4000) -> list[dict]:
    """Cost of the same task under each history policy, and what each policy costs in utility."""
    rows = []
    for mode, cap in (("retain", None), ("delete", None), ("compress", None),
                      ("progress_authorized", None), ("retain", 2000)):
        s = Session(budget_credits=1e9, cap=cap, mode=mode)
        oracle_successes = 0
        for turn in range(turns):
            s.tool_result(tool_size)
            s.finish_turn()
            # Task utility oracle: the step can only complete if the needed context survived.
            survives = mode != "delete" or turn == 0
            if survives and (mode != "progress_authorized" or turn < 6):
                oracle_successes += 1
        rows.append({
            "policy": mode if cap is None else f"{mode} + fixed cap {cap}",
            "billed_credits": round(s.billed, 3),
            "final_context": s.context_tokens(),
            "task_steps_completed": oracle_successes,
            "total_steps": turns,
        })
    return rows


def sweep(turns: int = 12) -> list[dict]:
    """Cumulative input as the attack scales."""
    return [{"turns": t, "input_multiple": inflation(t, 4000)} for t in range(1, turns + 1)]


def main() -> None:
    print("=" * 78)
    print("1. THE MECHANISM - a tool returns a lot, and the provider bills it again every turn")
    print("=" * 78)
    s = attack_scenario()
    print(f"  initiating call                 : {INITIATING_CALL_TOKENS} input tokens")
    print(f"  after {s.turns} turns, context      : {s.context_tokens()} input tokens")
    print(f"  total billed                    : {s.billed:.3f} credits, for ONE task")
    print(f"  inflation                       : {s.context_tokens() / INITIATING_CALL_TOKENS:.2f}x the first call")
    print()
    print("  No credential was stolen and nothing was exfiltrated. The attack succeeded because")
    print("  the victim paid for it.")

    print()
    print("=" * 78)
    print("2. INFLATION AS THE ATTACK SCALES")
    print("=" * 78)
    print(f"  {'turns':<8}{'cumulative input / initiating call'}")
    for row in sweep():
        print(f"  {row['turns']:<8}{row['input_multiple']:>8.2f}x")

    print()
    print("=" * 78)
    print("3. DEFENSES - priced against the same task")
    print("=" * 78)
    print(f"  {'policy':<34}{'billed':<11}{'steps completed':<18}{'final context'}")
    for r in table():
        print(f"  {r['policy']:<34}{r['billed_credits']:<11}"
              f"{str(r['task_steps_completed']) + '/' + str(r['total_steps']):<18}{r['final_context']}")

    print()
    print("=" * 78)
    print("4. WHAT EACH DEFENSE COSTS")
    print("=" * 78)
    base = table()[0]["billed_credits"]
    for r in table()[1:]:
        save = (1 - r["billed_credits"] / base) * 100 if base else 0
        print(f"  {r['policy']:<34}saves {save:>5.1f}% of cost, "
              f"completes {r['task_steps_completed']}/{r['total_steps']} steps")
    print()
    print("  Blunt deletion is the cheapest policy and it breaks the task, because it throws away")
    print("  the context the work depends on. A fixed cap is predictable and interrupts work. The")
    print("  interesting middle is compressing what the task needs - more expensive per turn, and")
    print("  it keeps the steps running. Every one of these is a utility trade, not a free win.")
    print()
    print("  And the control that is actually enforced is upstream: do not let an untrusted tool")
    print("  decide how much it returns. Cap the tool's response size in code, and bill per session")
    print("  rather than per accumulated context.")


if __name__ == "__main__":
    main()
