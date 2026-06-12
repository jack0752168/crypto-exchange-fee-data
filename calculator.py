#!/usr/bin/env python3
"""Effective crypto trading fee calculator: VIP tier + token discount + rebate.

    effective_fee = base_rate(tier) * token_discount * (1 - rebate_share)

Examples:
    python3 calculator.py --exchange binance --market futures --volume 10_000_000 \
        --maker-share 0.7 --rebate 0.4
    python3 calculator.py --exchange okx --market futures --volume 50_000_000 \
        --maker-share 0.9 --rebate 0.4

Data: fees/binance-2026.json, fees/okx-2026.json (MIT licensed).
"""
import argparse
import json
from pathlib import Path

HERE = Path(__file__).parent


def load(exchange):
    return json.loads((HERE / "fees" / f"{exchange}-2026.json").read_text())


def pick_tier(tiers, volume, key):
    chosen = tiers[0]
    for t in tiers:
        gate = t.get(key) or 0
        if volume >= gate:
            chosen = t
    return chosen


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--exchange", choices=["binance", "okx"], required=True)
    ap.add_argument("--market", choices=["spot", "futures"], default="futures")
    ap.add_argument("--volume", type=float, required=True,
                    help="30-day volume in USD (also used as the monthly traded volume)")
    ap.add_argument("--maker-share", type=float, default=0.5,
                    help="fraction of volume filled as maker (0-1)")
    ap.add_argument("--rebate", type=float, default=0.0,
                    help="rebate share of net fee, e.g. 0.4 for up to 40%%")
    ap.add_argument("--bnb", action="store_true",
                    help="apply BNB fee discount (Binance only)")
    args = ap.parse_args()

    data = load(args.exchange)
    if args.exchange == "binance":
        book = data["spot"] if args.market == "spot" else data["usdm_futures"]
        vol_key = "spot_vol_min_usd" if args.market == "spot" else "futures_vol_min_usd"
    else:
        book = data["futures"]
        vol_key = "vol_min_usd"

    tier = pick_tier(book["tiers"], args.volume, vol_key)
    maker, taker = tier["maker"] / 100, tier["taker"] / 100

    disc = 1.0
    if args.bnb and args.exchange == "binance":
        disc = 1 - (data["discounts"]["bnb_spot"] if args.market == "spot"
                    else data["discounts"]["bnb_futures"])

    blended = (args.maker_share * maker + (1 - args.maker_share) * taker) * disc
    gross = args.volume * blended
    net = gross * (1 - args.rebate)

    print(f"{data['exchange']} {args.market} — tier {tier['tier']} "
          f"(maker {tier['maker']}% / taker {tier['taker']}%)")
    print(f"Blended rate{' after BNB discount' if disc < 1 else ''}: {blended * 100:.4f}%")
    print(f"Gross monthly fee on ${args.volume:,.0f}: ${gross:,.2f}")
    if args.rebate:
        print(f"After {args.rebate:.0%} rebate: ${net:,.2f}  (rebate back: ${gross - net:,.2f})")


if __name__ == "__main__":
    main()
