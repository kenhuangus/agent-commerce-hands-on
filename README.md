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

`index.html` is a 40-slide deck, modelled on Ken's two source decks
([agent-commerce-investment-stack](https://kenhuangus.github.io/agent-commerce-investment-stack/)
and
[agent-commerce-security-site](https://kenhuangus.github.io/agent-commerce-security-site/)):
one slide fills the viewport, with a self-contained deck engine
(no dependencies) — **Prev / Next** buttons,
clickable **progress dots**, slide count, progress bar, **hash deep
links** (`#27` opens slide 27), keyboard
(→ / Space / PageDown = next, ← / PageUp = previous, Home / End,
F = fullscreen), touch swipe, and a wheel that scrolls inside a long
slide first, then moves on. A grid overview (all 40 slides) is in the
top bar. The top bar jumps straight to a section (Agenda, Protocols,
Lab 1–4, Cases, Before).
All three simulators and every code tab work inside the slides.
Slides 1–21 are the original workshop; slides 22–40 add ten theories
and eight practices on agent commerce (see table below).

| # | Slide | # | Slide |
| --- | --- | --- | --- |
| 1 | Cover — Agentic commerce, hands on | 21 | Checkpoint — what you have built so far |
| 2 | Stack at a glance — ecosystem to identity | 22 | Why theory? The map before the market |
| 3 | Stack — protocol, data, model | 23 | Theory 1 — Principal–agent theory and agency costs |
| 4 | Agenda — 180 minutes, four builds | 24 | Theory 2 — Transaction cost economics |
| 5 | Protocols 1 — the live rails | 25 | Theory 3 — Two-sided markets and network effects |
| 6 | Protocols 2 — specs, drafts and the volume argument | 26 | Theory 4 — Mechanism design and auction theory |
| 7 | Lab 1 — x402 flow and simulator | 27 | Theory 5 — Negotiation theory and bargaining |
| 8 | Lab 1 — seller and buyer code | 28 | Theory 6 — Contract theory and incomplete contracts |
| 9 | Lab 1 — steps and done-when | 29 | Theory 7 — Trust and reputation systems |
| 10 | Lab 2 — UCP discovery and ACP checkout code | 30 | Theory 8 — Information asymmetry, signalling, screening |
| 11 | Lab 2 — steps, token scoping, done-when | 31 | Theory 9 — Delegation and mandates |
| 12 | Lab 3 — policy simulator | 32 | Theory 10 — Payment and settlement theory |
| 13 | Lab 3 — hook, wallet policy, awal CLI | 33 | Practice 1 — Personal agents in production |
| 14 | Lab 3 — circuit breaker and steps | 34 | Practice 2 — Business agents and procurement |
| 15 | Lab 4 — memory gate and CaMeL | 35 | Practice 3 — Agent identity and discovery in production |
| 16 | Lab 4 — CuP calculator, benchmarks, pass bars | 36 | Practice 4 — Price discovery and dynamic pricing by agents |
| 17 | Use cases — Amazon blocks Muse, Walmart opens | 37 | Practice 5 — Disputes, chargebacks, refunds |
| 18 | Use cases — Shopify counters, the legal line | 38 | Practice 6 — Liability and insurance for agent errors |
| 19 | Before you come — setup and capstone checklist | 39 | Practice 7 — Regulation: EU AI Act, PSD3, US states |
| 20 | Open questions and primary sources — Part 1 | 40 | Practice 8 — Cost-per-task economics and capstone |

Nothing was cut in the remodel: every section, lab, code block,
simulator, table row, use case, and honest-flag from the scrolling
page is on a slide, split across slides where a section was long.
`assets/deck.js` is kept in the repo as the navigation engine from
the 21-slide remodel; the 40-slide `index.html` carries the same
engine inline.

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
