# Lab 3 — Security gates that actually ship (35 min)

The workshop rule: **caps live in the wallet, gates live in code,
never in the prompt.**

Status: the only production controls demonstrable with primary docs
are wallet-level spend caps, token scoping, human-approval-by-default,
and code-level tool gates. **IBAC / CapToken, LoA 0–5, SJD identity and
"financial contracts" have no public production standard found — they
are deck framing / aspirational, not industry standards.** The shipping
equivalents are Stripe Shared Payment Tokens, AP2 mandates, and wallet
policy engines. Escrow/timelock is Draft ERC-8183 only; multi-sig for
commerce agents has no verified production deployment.

## Part A — PreToolUse policy gate (real Claude Code hook)

```bash
echo '{"tool_name":"place_order","tool_input":{"amount":750,"currency":"USD"}}' | python3 policy_gate.py; echo "exit=$?"
# exit=2 — BLOCKED, reason on stderr

echo '{"tool_name":"place_order","tool_input":{"amount":120,"currency":"USD"}}' | python3 policy_gate.py; echo "exit=$?"
# exit=0 — allowed
```

Rules: tool on the allowlist (`place_order`, `process_refund`,
`transfer`), amount ≤ **$500**, currency USD. Exit 2 blocks, exit 0
allows. Wire it for real with `settings.example.json` copied to
`.claude/settings.json` — then ask the agent to order $750 of goods
and watch the hook block it while the model adapts (split / escalate).
The gate held regardless.

## Part B — Circuit breaker (pattern you implement)

```bash
python3 circuit_breaker.py
```

Trips on velocity (>10 tx/min), cumulative session spend (>$500), or
3 consecutive failures. States: CLOSED → OPEN (paused, human review)
→ HALF_OPEN (one probe) → CLOSED. No named production circuit-breaker
for commerce agents exists — teach this as a pattern, not a product.

## Production parts this lab stands on

- **Coinbase CDP Server Wallets v2 / Agentic Wallets** — operator-set
  per-call and per-session caps enforced before signing (MPC in AWS
  Nitro Enclave); the agent cannot change them. Policy engine:
  reject-by-default, policy simulation available.
  `awal x402 pay <url> --max-amount 1000000` (= $1.00 USDC).
- **Walmart Agent Gateway** (21 Oct 2026, invite-only) — per-agent
  profiles, $50/$100/$200 caps, human approval by default.
- **Stripe Shared Payment Tokens** — scoped to merchant + amount +
  time, single-use, revocable: a capability token for *payment*.

## Sources

- Claude Code hooks docs (code.claude.com) — PreToolUse, exit 2 blocks
- Coinbase CDP docs — Server Wallets v2 policy engine, `awal` CLI
- https://eips.ethereum.org/EIPS/eip-8183 — ERC-8183 Draft escrow (25 Feb 2026)
