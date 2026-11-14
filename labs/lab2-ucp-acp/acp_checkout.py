"""Lab 2b — ACP checkout session (Python, stdlib only).

Builds an Agentic Commerce Protocol checkout session the way the spec
requires: POST /checkout_sessions with ``line_items`` / ``currency`` /
``capabilities``, headers ``Idempotency-Key`` + ``API-Version:
2026-04-17``, auth ``Authorization: Bearer``. Session states:
``incomplete -> ready_for_payment -> completed / canceled``; completion
uses a Stripe Shared Payment Token (SPT) — single-use, merchant-scoped,
amount-capped, time-limited; the agent never sees the card number.

ACP is OpenAI + Stripe (not Google; Google's commerce protocol is UCP).
Latest stable 2026-04-17. ChatGPT Instant Checkout launched Sep 2025
for US Etsy sellers, then OpenAI said on 24 Mar 2026 it was moving away
from a standalone Instant Checkout toward discovery-first — do not
teach Instant Checkout as the live default in Nov 2026.

!!! NEEDS MERCHANT CREDENTIALS !!!
This script NEVER sends a request unless you set ACP_BASE_URL and
ACP_API_KEY. --dry-run (default) only builds and prints the request.
There is no demo key and no sandbox merchant here; a real call needs
an ACP merchant integration (feed pushed via SFTP/API after applying
to OpenAI) and a Stripe SPT from a payment provider.

Usage:
    python3 acp_checkout.py --dry-run
    ACP_BASE_URL=https://merchant.example ACP_API_KEY=sk_... python3 acp_checkout.py --send
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
import uuid

API_VERSION = "2026-04-17"
STATES = ["incomplete", "ready_for_payment", "completed", "canceled"]
VALID_TRANSITIONS = {
    "incomplete": {"ready_for_payment", "canceled"},
    "ready_for_payment": {"completed", "canceled"},
    "completed": set(),
    "canceled": set(),
}


def build_session(buyer_note="demo order"):
    """Build a checkout_sessions request body (pure function, no I/O)."""
    return {
        "line_items": [
            {"id": "sku-demo-tee", "quantity": 1, "price": {"amount": 2500, "currency": "USD"}}
        ],
        "currency": "USD",
        "capabilities": ["shipping_address", "discounts"],
        "metadata": {"note": buyer_note},
    }


def validate_session(body):
    problems = []
    if not body.get("line_items"):
        problems.append("line_items missing or empty")
    for item in body.get("line_items", []):
        if item.get("quantity", 0) < 1:
            problems.append(f"line item {item.get('id')}: quantity < 1")
        if item.get("price", {}).get("amount", 0) <= 0:
            problems.append(f"line item {item.get('id')}: amount must be > 0")
    if body.get("currency") != "USD":
        problems.append("currency must be USD in this demo")
    return problems


def transition(state, target):
    """Pure state-machine check for ACP checkout sessions."""
    if target in VALID_TRANSITIONS.get(state, set()):
        return target, None
    return state, f"illegal transition {state} -> {target}"


def main():
    ap = argparse.ArgumentParser(description="Build (and optionally send) an ACP checkout session")
    ap.add_argument("--dry-run", action="store_true", default=True,
                    help="build + print only (default)")
    ap.add_argument("--send", action="store_true",
                    help="actually POST; requires ACP_BASE_URL and ACP_API_KEY")
    args = ap.parse_args()

    body = build_session()
    problems = validate_session(body)
    if problems:
        print("session body invalid:", "; ".join(problems))
        return 1

    idem = str(uuid.uuid4())
    headers = {
        "Content-Type": "application/json",
        "Idempotency-Key": idem,
        "API-Version": API_VERSION,
        "Authorization": "Bearer <ACP_API_KEY>",
    }
    print("POST /checkout_sessions")
    for k, v in headers.items():
        print(f"  {k}: {v}")
    print("body:")
    print(json.dumps(body, indent=2))
    print("\nstate machine (pure check):")
    state = "incomplete"
    for target in ["ready_for_payment", "completed"]:
        state, err = transition(state, target)
        print(f"  {state}" + (f"  <-- {err}" if err else ""))
    bad, err = transition("completed", "ready_for_payment")
    print(f"  completed -> ready_for_payment rejected: {err}")

    if not args.send:
        print("\n--dry-run: nothing sent. Set ACP_BASE_URL + ACP_API_KEY and pass --send for a real call.")
        print("Completion needs a Stripe Shared Payment Token (SPT): single-use, merchant-scoped,")
        print("amount-capped, time-limited; in public preview (US/Canada/select Europe).")
        return 0

    base = os.environ.get("ACP_BASE_URL", "").rstrip("/")
    key = os.environ.get("ACP_API_KEY", "")
    if not base or not key:
        print("ERROR: --send needs ACP_BASE_URL and ACP_API_KEY in the environment.")
        print("No demo key exists. Get merchant credentials via an ACP integration.")
        return 2
    headers["Authorization"] = f"Bearer {key}"
    req = urllib.request.Request(base + "/checkout_sessions",
                                 data=json.dumps(body).encode(), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            print(f"\nPOST -> HTTP {resp.status}")
            print(resp.read().decode()[:2000])
    except urllib.error.HTTPError as e:
        print(f"\nPOST -> HTTP {e.code}\n{e.read().decode()[:2000]}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
