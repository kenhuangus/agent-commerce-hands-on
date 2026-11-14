# Agentic Commerce Hands-On Workshop — 3 Hours, Working Code

**Live site:** https://kenhuangus.github.io/agent-commerce-hands-on/

A 3-hour hands-on workshop that combines Ken Huang's two decks —
the seven-layer agentic commerce investment stack and the agentic
commerce security foundations — into one build session with working
code and real-world use cases. Every protocol is taught at its true
status as of November 2026: what is live, what is a spec, and what is
deck framing.

**Workshop rule:** caps live in the wallet, gates live in code, never
in the prompt.

## The site is a slide deck

`index.html` is a 21-slide deck, modelled on Ken's two source decks
([agent-commerce-investment-stack](https://kenhuangus.github.io/agent-commerce-investment-stack/)
and
[agent-commerce-security-site](https://kenhuangus.github.io/agent-commerce-security-site/)):
one slide fills the viewport, with the same navigation engine
(`assets/deck.js`, no dependencies) — **Prev / Next** buttons,
clickable **progress dots**, slide count, progress bar, **hash deep
links** (`#12` opens slide 12), keyboard
(→ / Space / PageDown = next, ← / PageUp = previous, Home / End,
F = fullscreen), touch swipe, and a debounced wheel (a long lab slide
scrolls internally first, then the wheel moves on). The top bar jumps
straight to a section (Agenda, Protocols, Lab 1–4, Cases, Before).
All three simulators and every code tab work inside the slides.

| # | Slide | # | Slide |
| --- | --- | --- | --- |
| 1 | Cover | 12 | Lab 3 — Security Gates |
| 2 | The Stack at a Glance | 13 | Lab 3 — Enforcement Points |
| 3 | The Stack: Protocol, Data, Model | 14 | Lab 3 — Steps, Breaker & Outcome |
| 4 | Agenda — 180 Minutes | 15 | Lab 4 — Poison the Memory |
| 5 | Protocols 1 — Live Rails | 16 | Lab 4 — Score It: Completion under Policy |
| 6 | Protocols 2 — Specs, Drafts & Volume | 17 | Use Cases 1 — Amazon vs Walmart |
| 7 | Lab 1 — Charge a Machine | 18 | Use Cases 2 — Shopify & the Law |
| 8 | Lab 1 — Seller & Buyer Code | 19 | Before You Come |
| 9 | Lab 1 — Steps & Outcome | 20 | Open Questions & Sources |
| 10 | Lab 2 — Checkout Without a Card | 21 | Closing |
| 11 | Lab 2 — Steps & Outcome | | |

Nothing was cut in the remodel: every section, lab, code block,
simulator, table row, use case, and honest-flag from the scrolling
page is on a slide, split across slides where a section was long.

## Agenda — 180 minutes, four builds

| Time | Block | Lab |
| --- | --- | --- |
| 0:00 – 0:25 | The landscape: what is live, what is a spec | — |
| 0:25 – 1:00 | Lab 1 — Charge a machine: x402 micropayments | [Lab 1](labs/lab1-x402/) · 35 min · TypeScript or Python |
| 1:00 – 1:35 | Lab 2 — Checkout without a card number: UCP + ACP | [Lab 2](labs/lab2-ucp-acp/) · 35 min · HTTP + JSON |
| 1:35 – 1:45 | Break — leave your Lab 2 session in `ready_for_payment`; Lab 3 tries to break it | — |
| 1:45 – 2:20 | Lab 3 — Security gates that actually ship | [Lab 3](labs/lab3-policy-gate/) · 35 min · Python |
| 2:20 – 2:50 | Lab 4 — Poison the memory, then score honestly | [Lab 4](labs/lab4-memory-eval/) · 30 min |
| 2:50 – 3:00 | Capstone checklist + thresholds | — |

## The labs

- **Lab 1 — x402** (`labs/lab1-x402/`): a paid API endpoint and an
  auto-paying client in TypeScript and Python, x402 v2 headers
  (`PAYMENT-SIGNATURE` / `PAYMENT-RESPONSE`), Base Sepolia
  (`eip155:84532`), $0.10 USDC. Runs fully offline on localhost.
- **Lab 2 — UCP + ACP** (`labs/lab2-ucp-acp/`): fetch a live merchant
  UCP profile at `/.well-known/ucp`; build an ACP checkout session
  (`Idempotency-Key` + `API-Version: 2026-04-17`) with a Shared
  Payment Token. Dry-run by default — a real ACP call needs merchant
  credentials (see the lab README).
- **Lab 3 — Policy gates** (`labs/lab3-policy-gate/`): a real Claude
  Code `PreToolUse` hook (`policy_gate.py`, exit 2 blocks amounts
  over $500) plus a circuit-breaker pattern and CDP / `awal` notes.
- **Lab 4 — Memory + eval** (`labs/lab4-memory-eval/`): a memory
  provenance guard (quarantines untrusted writes) and a Completion
  under Policy calculator.

Every lab has its own README with run steps. All code runs offline
with no keys and no network calls on import; nothing here is a stub,
a TODO, or smoke code.

## Run locally

```bash
git clone https://github.com/kenhuangus/agent-commerce-hands-on.git
cd agent-commerce-hands-on
python3 -m http.server 8000
# open http://localhost:8000/
```

Each lab runs from its own directory — see its README.

## Status labels used in this workshop

- **LIVE** — production use verified with primary docs (x402 for API
  micropayments; UCP in Google AI Mode / Gemini, US, gated; ACP
  discovery-first since 24 Mar 2026; A2A v1.0).
- **SPEC** — published specification, no verified live use (AP2
  v0.2.0; ERC-8004 draft; ERC-8183 escrow draft).
- **DRAFT / PATTERN** — deck framing or a design pattern, not a
  shipped standard (IBAC / CapToken, LoA 0–5, SJD, "A2A-Pay" as a
  name — use a2a-x402 — circuit breakers, multi-sig for commerce
  agents).

Corrections to the source decks, verified against primary docs in
Nov 2026: ACP is OpenAI + Stripe (not Google); UCP is Google +
Shopify (not Meta/Shopify); AP2 is specified only, with no verified
live use.

## Sources

Source decks (Ken Huang):

- Agentic commerce investment stack — https://kenhuangus.github.io/agent-commerce-investment-stack/
- Agentic commerce security site — https://kenhuangus.github.io/agent-commerce-security-site/

Primary protocol docs:

- https://docs.x402.org/ — x402 v2 (402 flow, facilitator verify/settle)
- https://ucp.dev/ — Universal Commerce Protocol (v2026-08-25)
- https://www.agenticcommerce.dev/ — Agentic Commerce Protocol (2026-04-17)
- https://ap2-protocol.org/ — Agent Payments Protocol (v0.2.0)
- https://a2a-protocol.org/latest/ — Agent2Agent (v1.0.1)
- https://eips.ethereum.org/EIPS/eip-8183 — ERC-8183 escrow (Draft)

## Agentic Academy

This workshop is the Agentic Commerce course in Ken's Agentic Academy
Saturday series: **Sat, Nov 21, 2026 — Agentic Commerce course, $338
per course, code SUBSTACK30 = 30% off ($236.60)**. Source: Ken's
Agentic Academy catalog update, 2026-11-11 (four Saturday courses
Nov 21, Nov 28, Dec 5, Dec 12, 2026; $338 per course; SUBSTACK30,
one use per order; site training.distributedapps.ai).
