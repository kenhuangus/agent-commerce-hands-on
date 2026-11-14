"""Lab 2a — UCP merchant discovery (Python, stdlib only).

Fetches a merchant's UCP profile at GET /.well-known/ucp and validates
the shape the protocol requires: ``ucp.version``, ``ucp.services``,
``ucp.payment_handlers``. Real Shopify profiles carry services and
payment_handlers as dicts keyed by name (see SAMPLE_PROFILE, trimmed
from allbirds.com, fetched 2026-11-13); the validator also accepts
the list shapes some secondary summaries show.

UCP (Universal Commerce Protocol) is Google + Shopify (not Meta/Shopify;
Meta joined the Tech Council in Apr 2026). Latest release v2026-08-25.
Live in Google AI Mode + Gemini for US shoppers, but going live is
gated — Google must approve a UCP integration. Do not promise a
student can go live without that approval.

Usage:
    python3 ucp_discovery.py --sample
        # offline: validates the embedded sample profile (no network)
    python3 ucp_discovery.py https://<shopify-store>/.well-known/ucp
        # live: fetches a real merchant profile (Shopify stores publish one)
    python3 ucp_discovery.py --url https://example.com/.well-known/ucp

No keys required. Network is only used when you pass a real URL.
"""

import argparse
import json
import sys
import urllib.request
import urllib.error

SAMPLE_PROFILE = {
    # Trimmed from a REAL profile fetched 2026-11-13 from
    # https://www.allbirds.com/.well-known/ucp (Shopify store).
    # Real shape: services is a dict keyed by service name, and
    # payment_handlers is a dict keyed by handler name — not the
    # list shapes some secondary summaries show. The validator below
    # accepts both shapes.
    "ucp": {
        "version": "2026-08-25",
        "services": {
            "dev.ucp.shopping": [
                {"version": "2026-08-25", "transport": "mcp",
                 "endpoint": "https://weareallbirds.myshopify.com/api/ucp/mcp"}
            ],
            "dev.ucp.common": [
                {"version": "2026-08-25", "transport": "mcp",
                 "endpoint": "https://weareallbirds.myshopify.com/api/ucp/mcp"}
            ],
        },
        "capabilities": {
            "dev.ucp.shopping.checkout": [{"version": "2026-08-25"}],
            "dev.ucp.shopping.cart": [{"version": "2026-08-25"}],
            "dev.ucp.common.ask": [{"version": "2026-08-25"}],
        },
        "payment_handlers": {
            "com.google.pay": [{"id": "gpay", "version": "2026-01-11"}],
            "dev.shopify.shop_pay": [{"id": "shop_pay", "version": "2026-04-08"}],
        },
    }
}

# Fall '26 additions (per ucp.dev reporting): merchant-published facts
# and a buy permalink. Shown here as the shape to look for, not as a
# claim that every store exposes them.
SAMPLE_EXTRA_ENDPOINTS = ["/ask", "/buy"]


def validate(profile):
    """Return (ok, problems, notes) for a parsed UCP profile dict.

    Accepts both the real profile shape (services/payment_handlers as
    dicts keyed by name, as Shopify stores publish) and the list
    shapes shown in secondary summaries.
    """
    problems, notes = [], []
    ucp = profile.get("ucp")
    if not isinstance(ucp, dict):
        return False, ["top-level 'ucp' object missing"], notes
    version = ucp.get("version")
    if not version:
        problems.append("ucp.version missing")
    else:
        notes.append(f"version {version} (latest release known Nov 2026: v2026-08-25)")
    services = ucp.get("services")
    capabilities = ucp.get("capabilities") or {}
    if isinstance(services, dict):
        names = list(services.keys())
        notes.append(f"services: {', '.join(names)}")
        has_checkout = ("dev.ucp.shopping.checkout" in capabilities
                        or "dev.ucp.shopping" in names)
    elif isinstance(services, list) and services:
        kinds = [s.get("type") for s in services if isinstance(s, dict)]
        notes.append(f"services: {', '.join(kinds)}")
        has_checkout = "checkout" in kinds
    else:
        problems.append("ucp.services missing or empty")
        has_checkout = False
    if services and not has_checkout:
        problems.append("no checkout service/capability found")
    handlers = ucp.get("payment_handlers")
    if isinstance(handlers, dict):
        notes.append(f"payment_handlers: {', '.join(handlers.keys())}")
    elif isinstance(handlers, list) and handlers:
        notes.append(f"payment_handlers: {', '.join(handlers)}")
    else:
        problems.append("ucp.payment_handlers missing or empty")
    if handlers:
        notes.append("payment proof is an AP2 mandate or Google Pay credential, not a card number")
    return (not problems), problems, notes


def fetch_profile(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return None, {"error": str(e)}


def main():
    ap = argparse.ArgumentParser(description="Fetch and validate a UCP merchant profile")
    ap.add_argument("url", nargs="?", help="profile URL, e.g. https://store.example/.well-known/ucp")
    ap.add_argument("--url", dest="url_opt", help="same as positional URL")
    ap.add_argument("--sample", action="store_true", help="validate the embedded sample profile (offline)")
    args = ap.parse_args()
    if args.sample:
        profile = SAMPLE_PROFILE
        print("sample profile (offline, shape from ucp.dev reporting):")
        print(json.dumps(profile, indent=2))
    else:
        url = args.url_opt or args.url
        if not url:
            ap.error("give a URL or --sample")
        status, profile = fetch_profile(url)
        if profile is None or "error" in (profile or {}):
            print(f"fetch failed ({url}): HTTP {status} {profile}")
            return 1
        print(f"GET {url} -> HTTP {status}")
        print(json.dumps(profile, indent=2)[:2000])
    ok, problems, notes = validate(profile)
    print()
    for n in notes:
        print(f"  ok: {n}")
    if problems:
        for p in problems:
            print(f"  PROBLEM: {p}")
        print("RESULT: profile INVALID as a UCP merchant profile")
        return 1
    print("RESULT: valid UCP profile shape")
    print(f"  also look for Fall '26 endpoints: {', '.join(SAMPLE_EXTRA_ENDPOINTS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
