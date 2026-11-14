"""Lab 3b — Circuit breaker for a shopping agent (Python, stdlib only).

No named production circuit-breaker for commerce agents was found as
of Nov 2026 — this is a DESIGN PATTERN to implement, not a shipped
product. Closest real analogues: Skyfire-style rate/velocity limits,
Coinbase maxBudgetUsd / subagent-spawn-depth caps, and Walmart's
account-level kill switch ("agents that break terms will be blocked").

The breaker trips (OPEN) when any of these fire, pauses the agent,
and requires human review before it closes again:
  * velocity: more than MAX_TX_PER_MINUTE transactions in a rolling minute
  * cumulative spend: session spend above SESSION_CAP_USD
  * failures: CONSECUTIVE_FAILURES failed tool calls in a row

States: CLOSED (normal) -> OPEN (paused) -> HALF_OPEN (one probe
transaction, then CLOSED on success or OPEN again on failure).

Run:
    python3 circuit_breaker.py
    # demo: 12 rapid $40 orders trip the velocity rule; a $600 order
    # trips the cumulative cap; the breaker pauses and needs review.

Coinbase CDP note (production part): CDP Server Wallets v2 enforce
operator-set per-call and per-session caps at the infrastructure layer
before signing — the agent cannot change them. Policy simulation is
available. The `awal` CLI equivalent is:
    awal x402 pay https://api.example.com/premium --max-amount 1000000
($1.00 USDC, 6 decimals). Networks: Base, Base Sepolia, Polygon, Solana.
"""

import time

MAX_TX_PER_MINUTE = 10
SESSION_CAP_USD = 500.0
CONSECUTIVE_FAILURES = 3


class CircuitBreaker:
    def __init__(self, max_tx_per_minute=MAX_TX_PER_MINUTE,
                 session_cap_usd=SESSION_CAP_USD,
                 max_failures=CONSECUTIVE_FAILURES):
        self.max_tx_per_minute = max_tx_per_minute
        self.session_cap_usd = session_cap_usd
        self.max_failures = max_failures
        self.state = "CLOSED"
        self.tx_times = []
        self.session_spend = 0.0
        self.failures = 0
        self.trip_reason = None

    def _trip(self, reason):
        self.state = "OPEN"
        self.trip_reason = reason
        return False, f"TRIPPED ({reason}) — agent paused, human review required"

    def attempt(self, amount_usd, success=True, now=None):
        """Check one transaction. Returns (allowed, message)."""
        now = now if now is not None else time.time()
        if self.state == "OPEN":
            return False, f"OPEN ({self.trip_reason}) — blocked, needs human review"
        if self.state == "HALF_OPEN" and not success:
            return self._trip("probe transaction failed in HALF_OPEN")
        self.tx_times = [t for t in self.tx_times if now - t < 60]
        if len(self.tx_times) >= self.max_tx_per_minute:
            return self._trip(f"velocity: {len(self.tx_times)} tx in the last minute (max {self.max_tx_per_minute})")
        if self.session_spend + amount_usd > self.session_cap_usd:
            return self._trip(f"cumulative spend ${self.session_spend + amount_usd:.2f} exceeds session cap ${self.session_cap_usd:.2f}")
        if not success:
            self.failures += 1
            if self.failures >= self.max_failures:
                return self._trip(f"{self.failures} consecutive failures")
            return True, f"recorded failure {self.failures}/{self.max_failures} (tx still counted)"
        self.failures = 0
        self.tx_times.append(now)
        self.session_spend += amount_usd
        if self.state == "HALF_OPEN":
            self.state = "CLOSED"
            return True, "probe succeeded — breaker CLOSED"
        return True, f"allowed — session spend now ${self.session_spend:.2f}"

    def human_review(self, approve):
        """Human reviews the pause. Approve -> HALF_OPEN (one probe tx)."""
        if self.state != "OPEN":
            return f"no review needed, breaker is {self.state}"
        if not approve:
            return "review declined — breaker stays OPEN"
        self.state = "HALF_OPEN"
        self.tx_times = []
        self.failures = 0
        return "review approved — HALF_OPEN, one probe transaction allowed"


def main():
    cb = CircuitBreaker()
    print("== velocity demo: 12 rapid $40 orders, max 10/min ==")
    for i in range(1, 13):
        ok, msg = cb.attempt(40.0, now=1000.0 + i)
        print(f"  tx {i:2d}: {'ALLOW' if ok else 'BLOCK'} — {msg}")
    print(f"== human review: {cb.human_review(approve=True)}")
    ok, msg = cb.attempt(40.0, now=2000.0)
    print(f"  probe tx: {'ALLOW' if ok else 'BLOCK'} — {msg}")
    print("== cumulative cap demo: $460 spent, then a $60 order ==")
    cb2 = CircuitBreaker()
    for amount in (200.0, 260.0, 60.0):
        ok, msg = cb2.attempt(amount, now=3000.0)
        print(f"  ${amount:6.2f}: {'ALLOW' if ok else 'BLOCK'} — {msg}")
    print("== failure demo: 3 failed calls in a row ==")
    cb3 = CircuitBreaker()
    for i in range(1, 4):
        ok, msg = cb3.attempt(10.0, success=False, now=4000.0 + i)
        print(f"  failure {i}: {'ALLOW' if ok else 'BLOCK'} — {msg}")
    print("\nAll three trips are patterns, not products — see the module docstring.")


if __name__ == "__main__":
    main()
