# btc-cent-forecast-01 — BTC 4-hour price forecast

Entry for make.fun's `btc-cent-forecast-01` ($250): a program that reads one
case (BTC/USDC 1-minute closes for the 72 hours up to a checkpoint) and
writes one number — the expected price 240 minutes (4 hours) after the
checkpoint.

## Design

`main.py` (Python 3.13, standard library only) forecasts

    last close + 0.15 * (mean of last 1440 closes - last close)

clamped to the scorer's 5-decimal price grid. No network, no randomness, no
clock: two runs write byte-identical outputs. Any malformed input falls back
to a valid-format output instead of crashing (a crashed/invalid case ranks
below every valid entry and takes no prize).

Why this tilt: BTC's 4-hour move is close to a random walk, so the honest
median forecast stays near the last price. On the kit's practice window
(92 hours of closes, 17 backtest checkpoints with full 72h history) the
15% pull toward the 24-hour mean beat the persistence baseline by ~5.5%
mean absolute error (49,206 vs 52,041 cents), with a flat sensitivity
curve for k in 0.10–0.25, while every momentum variant lost to persistence
on the same checkpoints. The edge is small and regime-dependent (it wins
the second half of the practice window, loses the first; on the five
directly-scorable practice cases p00–p04 it scores 48,310 vs persistence
47,055) — an honest small bet, not a certainty. A prize needs a score
strictly below the house baseline's on the final; pure persistence can
never win one, so the entry must deviate — this is the smallest deviation
with the best combined evidence.

## Local scores (backtest, mean absolute error in cents, lower is better)

| variant | 17 checkpoints | p00–p04 |
|---|---|---|
| persistence (house baseline) | 52,041 | 47,055 |
| **this entry (rev 24h mean, k=0.15)** | **49,206** | 48,310 |
| momentum 60 min, k=0.5 | 56,190 | 37,169 |
| momentum 240 min, k=0.25 | 57,194 | 45,560 |

The momentum variants win on the five practice cases but lose on the full
17-checkpoint backtest; the mean-reversion tilt is the only direction that
wins the larger set. The final is 12 unseen cases — beating the baseline
there is likely, not guaranteed. A prize needs a score strictly below the
baseline's on the final, with every case valid.

## Run locally

```sh
mkdir -p out && MAKEFUN_INPUT_DIR=../btc-cent-forecast-01-kit/input MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Files

- `main.py` — the entry (Python 3.13, stdlib only)
- `LICENSE` — MIT
- `.makefun/owner.json` — entry wallet (Dham's Solana payout address)
