# BTC 4-hour forecast — btc-cent-forecast-01

An entry for make.fun's `btc-cent-forecast-01` ($250). Each case gives 72
hours of BTC/USDC 1-minute closes up to a checkpoint; the program answers
with one number, the expected price 240 minutes (4 hours) later.

## The forecast

`main.py` (Python 3.13, standard library only) outputs

    last close + 0.15 * (mean of the last 1440 closes - last close)

rounded to the scorer's 5-decimal grid. No network, no clock, no
randomness — two runs write byte-identical outputs. A malformed case never
crashes the run; it falls back to a valid-format output, because a crashed
or invalid case ranks below every valid entry and wins nothing.

## Why a 15% pull toward the 24h mean

A 4-hour BTC move is close to a random walk, so the honest median forecast
stays near the last price. On the kit practice window (92 hours of closes,
17 checkpoints with full 72 h history) the 15% pull toward the 24-hour
mean beat the persistence baseline by roughly 5.5% mean absolute error
(49,206 vs 52,041 cents), and the sensitivity curve is flat for k between
0.10 and 0.25, while every momentum variant lost to persistence on the same
checkpoints. The edge is small and regime-dependent: it wins the second
half of the practice window and loses the first, and on the five
directly-scorable practice cases p00–p04 it scores 48,310 against
persistence's 47,055. So the tilt is deliberately small — the smallest
deviation with the best combined evidence. Pure persistence can never win
a prize (a prize needs a score strictly below the house baseline's on the
final), so the entry has to deviate; this is how little it takes.

## Local scores (backtest, MAE in cents, lower is better)

| variant | 17 checkpoints | p00–p04 |
|---|---|---|
| persistence (house baseline) | 52,041 | 47,055 |
| **this entry (24h-mean pull, k=0.15)** | **49,206** | 48,310 |
| momentum 60 min, k=0.5 | 56,190 | 37,169 |
| momentum 240 min, k=0.25 | 57,194 | 45,560 |

Momentum wins the five practice cases but loses the full 17-checkpoint
backtest; the mean-reversion tilt is the only direction that wins the
larger set. The final runs 12 unseen cases — beating the baseline there is
likely, not guaranteed. A prize needs a score strictly below the baseline's
on the final, with every case valid.

## Running it locally

```sh
mkdir -p out && MAKEFUN_INPUT_DIR=../btc-cent-forecast-01-kit/input MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Files

- `main.py` — the entry (Python 3.13, stdlib only)
- `LICENSE` — MIT
- `.makefun/owner.json` — entry wallet (Dham's Solana payout address)
