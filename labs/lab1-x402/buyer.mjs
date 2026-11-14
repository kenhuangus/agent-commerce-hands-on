// Lab 1 — x402 buyer (TypeScript-flavoured Node, zero dependencies).
//
// GET /premium -> 402 -> build demo payment payload -> resend with
// PAYMENT-SIGNATURE -> 200 + PAYMENT-RESPONSE receipt.
// Demo payload only (EIP-3009-shaped fields, unsigned). Production
// buyers sign with a real wallet via the x402 SDKs.
//
// Run:
//   node seller.mjs   # terminal 1
//   node buyer.mjs    # terminal 2

const URL = process.argv[2] ?? "http://127.0.0.1:4021/premium";
const PAYER = "0x1111111111111111111111111111111111111111"; // demo payer
const b64 = (o) => Buffer.from(JSON.stringify(o)).toString("base64");

async function get(headers = {}) {
  const res = await fetch(URL, { headers });
  return { status: res.status, headers: res.headers, body: await res.text() };
}

const first = await get();
console.log(`1) GET ${URL} -> ${first.status}`);
if (first.status !== 402) { console.log(`   expected 402, got ${first.status}: ${first.body}`); process.exit(1); }
const accepts = JSON.parse(first.body).accepts[0];
console.log(`   accepts: scheme=${accepts.scheme} network=${accepts.network} amount=${accepts.amount} asset=${accepts.asset}`);
const now = Math.floor(Date.now() / 1000);
const payload = {
  scheme: accepts.scheme,
  network: accepts.network,
  amount: accepts.amount,
  asset: accepts.asset,
  payTo: accepts.payTo,
  payer: PAYER,
  validAfter: now - 60,
  validBefore: now + (accepts.maxTimeoutSeconds ?? 60),
  nonce: `demo-${now}`,
};
console.log("2) resending with PAYMENT-SIGNATURE (demo payload, unsigned)");
const second = await get({ "PAYMENT-SIGNATURE": b64(payload) });
console.log(`   -> ${second.status}`);
if (second.status === 200) {
  const receipt = JSON.parse(Buffer.from(second.headers.get("payment-response"), "base64").toString("utf8"));
  console.log(`   resource: ${JSON.parse(second.body).resource}`);
  console.log(`   receipt: ${JSON.stringify(receipt)}`);
  process.exit(0);
}
console.log(`   payment rejected: ${second.body}`);
process.exit(1);
