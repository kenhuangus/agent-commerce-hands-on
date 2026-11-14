"""Lab 1 — x402 buyer (Python, stdlib only).

Flow: GET /premium -> 402 with accepts -> build a payment payload ->
resend with PAYMENT-SIGNATURE -> 200 + PAYMENT-RESPONSE receipt.

The payload here is a DEMO authorisation object (EIP-3009-shaped
fields: from/to/value/validAfter/validBefore/nonce). It is NOT a real
signature and settles nothing on-chain. A production buyer signs with
a real wallet via the x402 SDK (``@x402/axios`` / Python v2 client)
and the seller verifies/settles through a facilitator.

Run:
    python3 seller.py   # terminal 1
    python3 buyer.py    # terminal 2 (defaults to http://127.0.0.1:4021/premium)
    python3 buyer.py http://127.0.0.1:4021/premium
"""

import base64
import json
import sys
import time
import urllib.request
import urllib.error

URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:4021/premium"
PAYER = "0x1111111111111111111111111111111111111111"  # demo payer address


def b64(obj):
    return base64.b64encode(json.dumps(obj).encode()).decode()


def get(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, resp.headers, resp.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.headers, e.read().decode()


def main():
    status, _, body = get(URL)
    print(f"1) GET {URL} -> {status}")
    if status != 402:
        print(f"   expected 402, got {status}: {body}")
        return 1
    accepts = json.loads(body)["accepts"][0]
    print(f"   accepts: scheme={accepts['scheme']} network={accepts['network']} "
          f"amount={accepts['amount']} asset={accepts['asset']}")
    now = int(time.time())
    payload = {
        "scheme": accepts["scheme"],
        "network": accepts["network"],
        "amount": accepts["amount"],
        "asset": accepts["asset"],
        "payTo": accepts["payTo"],
        "payer": PAYER,
        # EIP-3009-shaped authorisation fields (demo values, unsigned):
        "validAfter": now - 60,
        "validBefore": now + accepts.get("maxTimeoutSeconds", 60),
        "nonce": f"demo-{now}",
    }
    print("2) resending with PAYMENT-SIGNATURE (demo payload, unsigned)")
    status, headers, body = get(URL, {"PAYMENT-SIGNATURE": b64(payload)})
    print(f"   -> {status}")
    if status == 200:
        receipt = json.loads(base64.b64decode(headers["PAYMENT-RESPONSE"]).decode())
        print(f"   resource: {json.loads(body)['resource'].strip()}")
        print(f"   receipt: {receipt}")
        return 0
    print(f"   payment rejected: {body}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
