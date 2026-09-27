"""OWASP Top 10 for LLM Applications: 2025 -> 2026 crosswalk, as data you can test.

Source: OWASP GenAI Security Project, LLM Top 10 2026 (released 2026-08-03),
https://genai.owasp.org/resource/owasp-genai-llm-top-10-2026/ (table in lessons/frontier/update-01.md).
Usage: py labs/lab-26-hidden-context/crosswalk.py "text citing LLM07 and LLM06:2025"
"""
import re
import sys

OWASP_2025_TO_2026 = {"LLM01": "LLM01", "LLM02": "LLM02", "LLM03": "LLM04", "LLM04": "LLM05",
                      "LLM05": "LLM10", "LLM06": "LLM03", "LLM07": "LLM08", "LLM08": "LLM09",
                      "LLM09": "LLM07", "LLM10": "LLM06"}


def relabel(text: str) -> str:
    """Bare or ':2025' IDs -> ':2026'; IDs already tagged ':2026' are left alone."""
    return re.sub(r"\bLLM(0[1-9]|10)(?::2025)?\b(?!:2026)",
                  lambda m: OWASP_2025_TO_2026["LLM" + m.group(1)] + ":2026", text)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(relabel(" ".join(sys.argv[1:])))
    else:
        for old, new in OWASP_2025_TO_2026.items():
            print(f"{old}:2025 -> {new}:2026")
