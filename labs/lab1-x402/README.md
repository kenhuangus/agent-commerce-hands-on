# Lab 1 — Charge a machine: x402 micropayments (35 min)

A paid API endpoint and an auto-paying client, using the **x402 v2**
wire format against **Base Sepolia (`eip155:84532`)**.

Status: **LIVE** — x402 is a production protocol (Coinbase, May 2025;
x402 Foundation / Linux Foundation since Jul 2026). Its verified live
use is API/data micropayments, not retail shopping. No named retail
merchant checkout on x402 was found as of Nov 2026.

## What you build

- `seller.py` / `seller.mjs` — serves `/premium` for $0.10 USDC
  (100000 smallest units, 6 decimals). Bare GET → `402` + payment
  instructions; GET with `PAYMENT-SIGNATURE` → `200` + `PAYMENT-RESPONSE`
  receipt header.
- `buyer.py` / `buyer.mjs` — handles the 402, builds the payment
  payload, resends, prints the receipt.

## Run (Python, no dependencies)

```bash
python3 seller.py   # terminal 1 — http://127.0.0.1:4021/premium
python3 buyer.py    # terminal 2 — expect: 402, then 200 + receipt
```

## Run (TypeScript / Node 18+, no dependencies)

```bash
node seller.mjs
node buyer.mjs      # terminal 2
```

## Try breaking it

- Pay less than the price: edit `buyer.py`'s amount to `"1"` and watch
  the seller answer 402 again with an error.
- Send a wrong network (`eip155:1`) and watch the same rejection.
- Note what the seller does **not** do: it never checks a signature
  against a chain. That is the facilitator's job in production
  (`/verify` + `/settle` at https://docs.x402.org/).

## Honest limits

- The payload is a **demo authorisation object** (EIP-3009-shaped
  fields, unsigned). Nothing settles on-chain here. A production buyer
  signs with a real wallet through the x402 SDKs (`@x402/axios`,
  `@x402/evm`, Python v2 client).
- v2 headers are `PAYMENT-SIGNATURE` / `PAYMENT-RESPONSE`. v1 used
  `X-PAYMENT` / `X-PAYMENT-RESPONSE` — do not teach v1 as current.
- Network is CAIP-2 (`eip155:84532`), not `base-sepolia`.

## Sources

- https://docs.x402.org/ (402 flow, facilitator verify/settle)
- https://docs.x402.org/guides/migration-v1-to-v2 (v1 → v2 headers, CAIP-2)
- https://docs.x402.org/sdk-features (SDKs, updated 2026-11-12)
