"""Lab 1 — x402 seller (Python, stdlib only).

Serves a paid endpoint on Base Sepolia (CAIP-2 network ``eip155:84532``)
using the x402 v2 wire format:

  1. Buyer GETs /premium with no payment  -> 402 + payment instructions
  2. Buyer resends with ``PAYMENT-SIGNATURE`` (base64 JSON payload)
  3. Seller checks scheme / network / asset / amount, then serves the
     resource with a ``PAYMENT-RESPONSE`` header carrying a signed receipt.

This is a LOCAL DEMO of the wire format. The payload is NOT a real
EIP-3009 signature and nothing settles on-chain. To settle for real,
use the x402 SDKs (``@x402/express``, ``@x402/evm`` / Python v2) with a
real wallet and a facilitator — see https://docs.x402.org/.

Run:
    python3 seller.py            # listens on http://127.0.0.1:4021
    python3 buyer.py             # in another terminal; pays and prints the receipt

Price: 100000 smallest units = $0.10 USDC (USDC has 6 decimals).
Asset default is Circle's Base Sepolia test USDC; verify the address
against https://docs.x402.org/ before pointing this at any real funds.
No keys, no network calls on import.
"""

import base64
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST = "127.0.0.1"
PORT = 4021

NETWORK = "eip155:84532"  # Base Sepolia, CAIP-2
ASSET = "0x036CbD53842c5426634e7929541eC2318f3dCF7e"  # Base Sepolia USDC
PRICE = "100000"  # smallest units (6 decimals) = $0.10
PAY_TO = "0x0000000000000000000000000000000000000000"  # demo payee; set your own
RESOURCE = "premium weather data: 21C, clear, wind 12 km/h (demo payload)\n"

ACCEPTS = {
    "scheme": "exact",
    "network": NETWORK,
    "amount": PRICE,
    "asset": ASSET,
    "payTo": PAY_TO,
    "maxTimeoutSeconds": 60,
    "description": "Premium weather report (demo, $0.10 USDC on Base Sepolia)",
}


def b64(obj):
    return base64.b64encode(json.dumps(obj).encode()).decode()


def unb64(text):
    return json.loads(base64.b64decode(text).decode())


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):  # keep output clean
        pass

    def _send(self, status, body, headers=None):
        data = body.encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        for k, v in (headers or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path != "/premium":
            self._send(404, json.dumps({"error": "only /premium exists in this demo"}))
            return
        sig = self.headers.get("PAYMENT-SIGNATURE")
        if not sig:
            # x402 v2: 402 + payment instructions in the body.
            self._send(402, json.dumps({"x402Version": 2, "accepts": [ACCEPTS]}))
            return
        try:
            payload = unb64(sig)
        except Exception as exc:
            self._send(400, json.dumps({"error": f"unparsable PAYMENT-SIGNATURE: {exc}"}))
            return
        problems = []
        if payload.get("scheme") != "exact":
            problems.append("scheme must be 'exact'")
        if payload.get("network") != NETWORK:
            problems.append(f"network must be {NETWORK}")
        if payload.get("asset") != ASSET:
            problems.append("asset mismatch")
        if int(payload.get("amount", 0)) < int(PRICE):
            problems.append(f"amount below price {PRICE}")
        if problems:
            self._send(402, json.dumps({"x402Version": 2, "accepts": [ACCEPTS], "error": "; ".join(problems)}))
            return
        receipt = {
            "success": True,
            "transaction": "demo-no-onchain-tx",
            "network": NETWORK,
            "payer": payload.get("payer", "unknown"),
            "amount": payload.get("amount"),
        }
        self._send(200, json.dumps({"resource": RESOURCE}),
                   {"PAYMENT-RESPONSE": b64(receipt)})


if __name__ == "__main__":
    print(f"x402 v2 demo seller on http://{HOST}:{PORT}/premium")
    print(f"network={NETWORK} asset={ASSET} price={PRICE} smallest units ($0.10 USDC)")
    HTTPServer((HOST, PORT), Handler).serve_forever()
