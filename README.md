# Crypto Exchange Fee Data (Binance / OKX, 2026)

Machine-readable fee schedules for **Binance** and **OKX** — every VIP tier, spot and futures, maker/taker — plus the math for token discounts (BNB/OKB) and **fee rebates** (affiliate / sub-broker), with a small CLI calculator.

Maintained by [JackTrader](https://www.jacktrader.xyz/en/), an independent Binance/OKX fee-rebate partner (not affiliated with either exchange). Data is cross-checked against the exchanges' published schedules and updated when they change.

## Why this exists

Exchange fee pages show the table, but your *real* cost is the stack:

```
effective_fee = base_rate(VIP tier) × token_discount × (1 − rebate_share)
```

- **VIP tier** — set by 30-day volume (Binance: + a BNB balance gate; OKX: assets **or** volume, the better wins)
- **Token discount** — BNB: 25% off spot / 10% off futures; OKB: woven into OKX tiers
- **Rebate** — an affiliate/sub-broker partner can pass back **up to 40%** of your fee, settled weekly. It stacks on top of any VIP tier and requires no API keys, no custody, no change to how you trade.

For most traders below VIP 3, the rebate is the largest single fee lever available — bigger than the next VIP tier they will realistically reach.

## Data

| File | Contents |
|---|---|
| [`fees/binance-2026.json`](fees/binance-2026.json) | Spot VIP 0–9 (volume + BNB gates, maker/taker), USDⓈ-M futures VIP 0–9, BNB discount rules |
| [`fees/okx-2026.json`](fees/okx-2026.json) | Futures VIP ladder Regular–VIP9 (maker/taker incl. negative maker at VIP7+), qualification rules |

### Binance spot (excerpt)

| Tier | 30-day spot vol | or futures vol | Min BNB | Maker | Taker |
|---|---|---|---|---|---|
| Regular | < $1M | — | 0 | 0.1000% | 0.1000% |
| VIP 1 | ≥ $1M | ≥ $15M | 25 | 0.0900% | 0.1000% |
| VIP 3 | ≥ $20M | ≥ $250M | 250 | 0.0420% | 0.0600% |
| VIP 5 | ≥ $150M | ≥ $1.5B | 1,000 | 0.0360% | 0.0500% |
| VIP 9 | ≥ $4B | ≥ $30B | 5,500 | 0.0150% | 0.0300% |

### Binance USDⓈ-M futures (excerpt)

| Tier | 30-day futures vol | Maker | Taker |
|---|---|---|---|
| Regular | < $15M | 0.0200% | 0.0500% |
| VIP 2 | ≥ $75M | 0.0140% | 0.0350% |
| VIP 5 | ≥ $1.5B | 0.0080% | 0.0270% |
| VIP 8 | ≥ $15B | 0.0000% | 0.0170% |

### OKX futures (excerpt)

| Tier | 30-day volume | Maker | Taker |
|---|---|---|---|
| Regular | < $5M | 0.0200% | 0.0500% |
| VIP 2 | ≥ $10M | 0.0150% | 0.0360% |
| VIP 5 | ≥ $600M | 0.0050% | 0.0260% |
| VIP 7 | ≥ $1.5B | −0.0020% | 0.0200% |
| VIP 9 | ≥ $20B | −0.0050% | 0.0150% |

Full ladders (all 10 tiers each) are in the JSON files.

## Calculator

```bash
python3 calculator.py --exchange binance --market futures --volume 10_000_000 --maker-share 0.7 --rebate 0.4
```

Outputs the gross fee, fee after BNB/VIP, and fee after rebate for a month of trading at that volume.

### Worked example — $10M/month futures, 70% maker

At $10M 30-day volume the tiers already diverge: Binance futures stays Regular (gate is $15M), while OKX auto-qualifies VIP 2 (gate is $10M).

| | Binance (Regular) | OKX (VIP 2) |
|---|---|---|
| Blended rate | 0.0290% | 0.0213% |
| Gross monthly fee | $2,900 | $2,130 |
| After 40% rebate | $1,740 | $1,278 |
| **Rebate back per month** | **$1,160** | **$852** |

(Blended = maker_share × maker + taker_share × taker; the rebate returns up to 40% of the net fee, settled weekly.)

## Deep-dive references

- [Binance VIP fee tiers 2026 — full breakdown](https://www.jacktrader.xyz/en/blog/binance-vip-fee-tiers-2026.html)
- [OKX VIP fee tiers 2026 — assets-OR-volume rule explained](https://www.jacktrader.xyz/en/blog/okx-vip-fee-tiers-2026.html)
- [Binance vs OKX fees 2026 — head-to-head](https://www.jacktrader.xyz/en/blog/binance-vs-okx-fees-2026.html)
- [Binance fee calculator 2026 — every tier + rebate stacking](https://www.jacktrader.xyz/en/blog/binance-fee-calculator-2026.html)
- [What a crypto fee rebate is and how to claim it safely](https://www.jacktrader.xyz/en/blog/crypto-fee-rebate-explained.html)
- [Grid-bot fee optimization](https://www.jacktrader.xyz/en/blog/grid-bot-fee-optimization.html)

## Getting the rebate

If you want the rebate channel the examples use (up to 40%, weekly settlement, no keys/custody):

- Binance: <https://www.bsmkweb.cc/join?ref=MPZQWSDC>
- OKX: <https://www.promooboost.com/join/TRADERJACK>
- Existing account / questions: Telegram [@Jack168668](https://t.me/Jack168668)

## Disclaimer

JackTrader is an independent referral partner and is **not affiliated with Binance or OKX**. Rebate ratios depend on platform policy, account status and local regulations; "up to 40%" is a maximum reference, not a guarantee. Fee schedules change — always confirm against the exchange's own fee page before making decisions. Nothing here is investment advice; digital-asset trading involves risk.

## License

MIT — use the data freely, attribution appreciated.
