# Changelog

All notable changes to the fee data are recorded here. Dates are when the data in
this repo was verified against the exchanges' published schedules, not necessarily
when the exchange changed them.

## 2026-06-17
- Added CI: every push validates the fee JSON is well-formed, the VIP ladders are
  complete, and the volume gates are monotonic (`tests/validate.py`), plus a
  calculator smoke test. A bad edit can no longer land silently.
- Added repository topics for discoverability.

## 2026-06-12
- Initial release.
- Binance spot VIP 0–9 (volume + BNB gates, maker/taker).
- Binance USDⓈ-M futures VIP 0–9.
- OKX futures ladder Regular–VIP 9 (including negative maker at VIP 7+).
- BNB / OKB discount rules and rebate model.
- `calculator.py`: effective-fee calculator modelling VIP tier × token discount ×
  rebate stacking.

---

Spotted a stale rate? Open a PR against the JSON in `fees/` — the goal is one
community-maintained source of truth. CI will validate your change automatically.

## 2026-07-07
- Verified fee schedules against live Binance/OKX pages (July 2026).
- Added affiliate/sub-broker program references and free embeddable calculator link.
