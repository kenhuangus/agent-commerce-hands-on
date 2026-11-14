"""Lab 3a — PreToolUse policy gate (Claude Code hook).

Claude Code runs this before each matching tool executes and the hook's
exit code is the enforcement: exit 2 BLOCKS the tool call, exit 0
allows it. The model cannot argue with it — it compares two numbers.
``CLAUDE.md`` / ``AGENTS.md`` are context, not enforcement; hooks are.

Rules enforced here (workshop policy, not an industry standard):
  * tool must be on the allowlist (place_order / process_refund / transfer)
  * amount must be <= $500 (the cap from the workshop; set your own)
  * currency must be USD; amount must be a number

Wire it in .claude/settings.json (see settings.example.json):
  { "hooks": { "PreToolUse": [
      { "matcher": "place_order|process_refund|transfer",
        "hooks": [{ "type": "command",
                    "command": "python3 labs/lab3-policy-gate/policy_gate.py" }] } ] } }

Input (stdin JSON): {"tool_name": ..., "tool_input": {"amount": ..., "currency": ...}}
Exit 0 = allow, exit 2 = block (reason on stderr).

Test offline (no Claude Code needed):
    echo '{"tool_name":"place_order","tool_input":{"amount":750,"currency":"USD"}}' | python3 policy_gate.py; echo "exit=$?"
    echo '{"tool_name":"place_order","tool_input":{"amount":120,"currency":"USD"}}' | python3 policy_gate.py; echo "exit=$?"
"""

import json
import sys

ALLOWED_TOOLS = {"place_order", "process_refund", "transfer"}
AMOUNT_CAP_USD = 500


def decide(event):
    """Pure decision: returns (allow: bool, reason: str)."""
    tool = event.get("tool_name", "")
    if tool not in ALLOWED_TOOLS:
        return False, f"tool '{tool}' is not on the allowlist {sorted(ALLOWED_TOOLS)}"
    amount = event.get("tool_input", {}).get("amount")
    if not isinstance(amount, (int, float)) or isinstance(amount, bool):
        return False, "tool_input.amount missing or not a number"
    if amount < 0:
        return False, "amount must not be negative"
    if event.get("tool_input", {}).get("currency", "USD") != "USD":
        return False, "only USD is allowed in this workshop policy"
    if amount > AMOUNT_CAP_USD:
        return False, f"amount ${amount} exceeds policy cap of ${AMOUNT_CAP_USD}"
    return True, f"allowed: {tool} ${amount} within ${AMOUNT_CAP_USD} cap"


def main():
    try:
        event = json.load(sys.stdin)
    except Exception as exc:
        print(f"policy gate: bad JSON on stdin: {exc}", file=sys.stderr)
        return 2
    allow, reason = decide(event)
    if allow:
        return 0
    print(f"policy gate BLOCKED: {reason}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
