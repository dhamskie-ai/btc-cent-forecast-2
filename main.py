#!/usr/bin/env python3
"""btc-cent-forecast-01 entry: gentle mean reversion toward the 24h mean.

Forecast = last close + 0.15 * (mean of last 1440 closes - last close),
clamped to the scorer's price grid (5 decimals, (0, 10_000_000)).

Why: on the kit's practice window (92h of 1-minute closes, 17 backtest
checkpoints with full 72h history) this tilt beat the persistence
baseline by ~5.5% mean absolute error (49,206 vs 52,041 cents), with a
flat sensitivity curve for k in 0.10-0.25, while every momentum variant
lost to persistence on the same checkpoints. On the five directly-scorable
practice cases (p00-p04) it scores 48,310 cents vs persistence 47,055 --
slightly worse, inside noise -- so the edge is small and regime-dependent,
not a certainty: it wins the second half of the practice window and loses
the first. The tilt is small on purpose: BTC's 4-hour move is close to a
random walk, so the honest median forecast stays near the last price; the
15% pull toward the 24-hour mean is a modest, regime-robust correction,
not a big bet.

Deterministic: pure arithmetic over the input prices, no randomness, no
clock, no network. Two runs write byte-identical outputs.
"""
import json
import math
import os
from pathlib import Path

MIN_PRICE = 0.00001
MAX_PRICE = 9_999_999.99999
K = 0.15
WINDOW = 1440


def grid(price):
    """Clamp to (0, 10_000_000) and round to the 5-decimal price grid."""
    if not math.isfinite(price):
        price = 1.0
    price = min(MAX_PRICE, max(MIN_PRICE, price))
    return round(price, 5)


def read_prices(case):
    """Return the finite closes of the case's single market, or []."""
    try:
        markets = case.get("markets") or []
        prices = markets[0].get("prices") if markets else None
        if isinstance(prices, list):
            return [p for p in prices if isinstance(p, (int, float)) and math.isfinite(p)]
    except Exception:
        pass
    return []


def forecast(prices):
    """Last close pulled 15% toward the mean of the last 1440 closes."""
    last = prices[-1]
    window = prices[-WINDOW:] if len(prices) > WINDOW else prices
    mean = sum(window) / len(window)
    return grid(last + K * (mean - last))


def main():
    in_dir = Path(os.environ.get("MAKEFUN_INPUT_DIR", "/input"))
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    for in_file in sorted(in_dir.glob("*.in")):
        case_id = in_file.name[: -len(".in")]
        price = 1.0
        try:
            case = json.loads(in_file.read_text(encoding="utf-8"))
            prices = read_prices(case)
            if prices:
                price = forecast(prices)
        except Exception:
            # Never crash: an invalid case ranks below every valid entry
            # and takes no prize, so keep a valid-format output instead.
            price = 1.0
        out = {"forecasts": [{"case": case_id, "price": price}]}
        (out_dir / f"{case_id}.out").write_text(json.dumps(out) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
