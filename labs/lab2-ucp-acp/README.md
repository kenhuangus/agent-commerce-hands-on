# Lab 2 — Checkout without a card number: UCP + ACP (35 min)

Two protocols, two halves of checkout. **UCP** (Google + Shopify) is
the merchant-side language for discovery → checkout → post-purchase.
**ACP** (OpenAI + Stripe) is the checkout session + delegated payment.
They separate checkout from payment authorisation — unlike ACP, which
bundles payment via a Shared Payment Token.

Status labels (Nov 2026):

| Protocol | Status |
| --- | --- |
| UCP | **LIVE** in Google AI Mode + Gemini for US shoppers — gated: Google must approve a UCP integration. Latest release v2026-08-25. |
| ACP | **LIVE but discovery-first since 24 Mar 2026** — OpenAI moved away from standalone Instant Checkout. Latest stable 2026-04-17. |
| AP2 (authorisation layer) | **SPECIFIED, no verified live use** — v0.2.0, 28 Apr 2026. Read its mandates as the "signed permission slip", demo only via the GitHub samples. |

## Part A — UCP discovery (runs offline or live)

```bash
python3 ucp_discovery.py --sample
# offline: validates the embedded sample profile

python3 ucp_discovery.py https://<a-shopify-store>/.well-known/ucp
# live: fetches a real merchant profile (Shopify stores publish one)
```

A valid profile has `ucp.version`, `ucp.services` (dict keyed by
service name, e.g. `dev.ucp.shopping`, with a `dev.ucp.shopping.checkout`
capability) and `ucp.payment_handlers` (dict keyed by handler, e.g.
`com.google.pay`, `dev.shopify.shop_pay`). Payment proof is an
AP2 mandate or a Google Pay credential — never a card number. Fall '26
additions to look for: `/ask` (answers from merchant-published facts)
and `/buy` (cart/checkout permalink).

## Part B — ACP checkout session (dry-run by default)

```bash
python3 acp_checkout.py --dry-run
```

Builds `POST /checkout_sessions` with `Idempotency-Key` and
`API-Version: 2026-04-17`, validates the body, and walks the state
machine `incomplete → ready_for_payment → completed / canceled`
(including one illegal transition, rejected on purpose).

**A real call needs merchant credentials.** There is no demo key:

```bash
ACP_BASE_URL=https://merchant.example ACP_API_KEY=sk_... python3 acp_checkout.py --send
```

Completion uses a Stripe **Shared Payment Token (SPT)**: single-use,
merchant-scoped, amount-capped, time-limited; the agent never sees the
card. SPTs are in public preview (US/Canada/select Europe); only
payment providers or PCI DSS Level 1 merchants with their own vaults
can integrate Delegated Payment directly.

## Sources

- https://ucp.dev/ (UCP home, co-developers, AP2/A2A/MCP built-in)
- https://www.agenticcommerce.dev/ (ACP home; OpenAI first implementer, Stripe first PSP)
- https://ap2-protocol.org/ (AP2 v0.2 mandates)
- https://a2a-protocol.org/latest/ (A2A v1.0; AP2 runs as an A2A extension; a2a-x402 carries x402 inside A2A tasks — "A2A-Pay" is a colloquial label, not a standard)
