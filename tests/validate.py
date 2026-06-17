#!/usr/bin/env python3
"""Validate the fee JSON files: well-formed, complete tier ladders, monotonic gates.

Run locally or in CI:  python3 tests/validate.py
Exits non-zero on any problem so a bad edit can't land silently.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FEES = ROOT / "fees"


def check(cond, msg, errors):
    if not cond:
        errors.append(msg)


def validate_ladder(name, tiers, gate_key, errors):
    if len(tiers) < 8:
        errors.append(f"{name}: only {len(tiers)} tiers (expected full VIP ladder)")
    last_gate = -1
    for t in tiers:
        for f in ("tier", "maker", "taker"):
            check(f in t, f"{name}: tier missing '{f}': {t}", errors)
        gate = t.get(gate_key)
        if gate is None:
            continue
        check(gate >= last_gate, f"{name}: {gate_key} not monotonic at {t.get('tier')} ({gate} < {last_gate})", errors)
        last_gate = gate


def main():
    errors = []
    files = sorted(FEES.glob("*.json"))
    check(len(files) >= 2, "expected at least binance + okx fee files", errors)
    for fp in files:
        try:
            data = json.loads(fp.read_text())
        except Exception as e:
            errors.append(f"{fp.name}: invalid JSON — {e}")
            continue
        check("exchange" in data, f"{fp.name}: missing 'exchange'", errors)
        check("as_of" in data, f"{fp.name}: missing 'as_of'", errors)
        check("rebate" in data, f"{fp.name}: missing 'rebate'", errors)
        for book_key, gate_key in (("spot", "spot_vol_min_usd"),
                                   ("usdm_futures", "futures_vol_min_usd"),
                                   ("futures", "vol_min_usd")):
            book = data.get(book_key)
            if book and "tiers" in book:
                validate_ladder(f"{fp.name}/{book_key}", book["tiers"], gate_key, errors)

    if errors:
        print("VALIDATION FAILED:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print(f"OK: {len(files)} fee files valid, ladders complete and monotonic.")


if __name__ == "__main__":
    main()
