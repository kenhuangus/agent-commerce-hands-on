// Lab 1 — x402 seller (TypeScript-flavoured Node, zero dependencies).
//
// Same wire format as seller.py: 402 + accepts on a bare GET, then
// PAYMENT-SIGNATURE (base64 JSON) -> 200 + PAYMENT-RESPONSE receipt.
// x402 v2 headers; network is CAIP-2 eip155:84532 (Base Sepolia).
// Demo payload only — no real signature, nothing settles on-chain.
// To settle for real, use @x402/express + a facilitator: https://docs.x402.org/
//
// Run:
//   node seller.mjs            # http://127.0.0.1:4021/premium
//   node buyer.mjs             # in another terminal
//
// Price: 100000 smallest units = $0.10 USDC (6 decimals).

import { createServer } from "node:http";

const PORT = 4021;
const NETWORK = "eip155:84532"; // Base Sepolia
const ASSET = "0x036CbD53842c5426634e7929541eC2318f3dCF7e"; // Base Sepolia USDC
const PRICE = "100000";
const PAY_TO = "0x0000000000000000000000000000000000000000"; // demo payee

const ACCEPTS = {
  scheme: "exact",
  network: NETWORK,
  amount: PRICE,
  asset: ASSET,
  payTo: PAY_TO,
  maxTimeoutSeconds: 60,
  description: "Premium weather report (demo, $0.10 USDC on Base Sepolia)",
};

const b64 = (o) => Buffer.from(JSON.stringify(o)).toString("base64");
const unb64 = (s) => JSON.parse(Buffer.from(s, "base64").toString("utf8"));

const server = createServer((req, res) => {
  const send = (status, body, headers = {}) => {
    const data = JSON.stringify(body);
    res.writeHead(status, { "Content-Type": "application/json", ...headers });
    res.end(data);
  };
  if (req.url !== "/premium") return send(404, { error: "only /premium exists in this demo" });
  const sig = req.headers["payment-signature"];
  if (!sig) return send(402, { x402Version: 2, accepts: [ACCEPTS] });
  let payload;
  try { payload = unb64(sig); } catch (e) { return send(400, { error: `unparsable PAYMENT-SIGNATURE: ${e.message}` }); }
  const problems = [];
  if (payload.scheme !== "exact") problems.push("scheme must be 'exact'");
  if (payload.network !== NETWORK) problems.push(`network must be ${NETWORK}`);
  if (payload.asset !== ASSET) problems.push("asset mismatch");
  if (Number(payload.amount || 0) < Number(PRICE)) problems.push(`amount below price ${PRICE}`);
  if (problems.length) return send(402, { x402Version: 2, accepts: [ACCEPTS], error: problems.join("; ") });
  const receipt = { success: true, transaction: "demo-no-onchain-tx", network: NETWORK, payer: payload.payer ?? "unknown", amount: payload.amount };
  return send(200, { resource: "premium weather data: 21C, clear, wind 12 km/h (demo payload)" }, { "PAYMENT-RESPONSE": b64(receipt) });
});

server.listen(PORT, "127.0.0.1", () => {
  console.log(`x402 v2 demo seller on http://127.0.0.1:${PORT}/premium`);
  console.log(`network=${NETWORK} asset=${ASSET} price=${PRICE} smallest units ($0.10 USDC)`);
});
