# Results (engine v2.0.0, generated from logs by analysis/decode_and_report.py)

All P&L is in points (USD per oz) after 0.3 pts round-trip cost. R = net P&L / initial risk. CIs are 95% cluster-bootstrap intervals of the mean per trade (5,000 resamples, seed 12345), clustered by linked-event group and, separately, by UK day. Max DD is the largest peak-to-trough fall of cumulative P&L in entry order.

Periods: **P1** 2026-08-03..10-23 (12 weeks, first used as out-of-sample on 15 Nov, now *seen*), **P2** 10-26..10-30 (seen), **P3** 11-02..11-13 (the period the rules were designed on). No period here is untouched.

## 1. PRIMARY: corrected events, point-in-time footprints, identical 5m execution

### Corrected (primary analysis)

| Period | Rule | Subset | n | Win % | Avg win | Avg loss | Exp pts | 95% CI pts (linked) | 95% CI pts (day) | Exp R | 95% CI R | Cost (R) | Med risk | Total pts | Max DD pts | Max DD R |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P1 | cont | all | 114 | 36 | 7.9 | -8.74 | -2.75 | -4.64..-0.96 | -4.51..-0.88 | -0.2 | -0.4..0.01 | 0.06 | 6.75 | -313.95 | -313.95 | -24.73 |
| P1 | cont | FILTERED: early footprint | 46 | 17 | 10.12 | -10.61 | -7.0 | -10.23..-3.76 | -10.09..-3.75 | -0.55 | -0.8..-0.27 | 0.05 | 8.04 | -322.03 | -322.03 | -25.33 |
| P1 | cont | complement: no early footprint | 68 | 48 | 7.36 | -6.71 | 0.12 | -1.82..2.12 | -1.52..1.77 | 0.04 | -0.23..0.32 | 0.06 | 5.71 | 8.08 | -72.94 | -11.55 |
| P1 | fade | all | 128 | 41 | 7.23 | -6.47 | -0.91 | -2.4..0.72 | -2.53..0.7 | -0.1 | -0.28..0.1 | 0.07 | 5.25 | -116.04 | -152.67 | -22.42 |
| P1 | fade | FILTERED: early footprint | 52 | 46 | 9.05 | -7.44 | 0.17 | -2.79..3.53 | -2.65..3.35 | 0.01 | -0.28..0.31 | 0.06 | 7.29 | 8.77 | -52.3 | -7.1 |
| P1 | fade | complement: no early footprint | 76 | 37 | 5.67 | -5.91 | -1.64 | -3.15..-0.13 | -3.0..-0.33 | -0.17 | -0.42..0.09 | 0.08 | 4.58 | -124.81 | -145.0 | -19.43 |
| P2 | cont | all | 10 | 30 | 5.45 | -4.26 | -1.35 | -4.05..1.81 | -3.64..-0.01 | -0.34 | -1.07..0.41 | 0.09 | 4.18 | -13.48 | -18.18 | -4.13 |
| P2 | cont | FILTERED: early footprint | 2 | 50 | 5.98 | -2.71 | 1.63 | -2.71..5.98 | -2.71..5.98 | 0.15 | -1.12..1.43 | 0.1 | 4.18 | 3.27 | -2.71 | -1.12 |
| P2 | cont | complement: no early footprint | 8 | 25 | 5.19 | -4.52 | -2.09 | -4.91..1.41 | -5.13..-0.06 | -0.46 | -1.09..0.46 | 0.09 | 4.58 | -16.75 | -16.75 | -3.71 |
| P2 | fade | all | 11 | 36 | 6.64 | -3.39 | 0.26 | -2.69..3.73 | -2.87..5.65 | -0.15 | -0.78..0.55 | 0.09 | 3.83 | 2.83 | -12.67 | -3.32 |
| P2 | fade | FILTERED: early footprint | 2 | 50 | 5.44 | -2.75 | 1.34 | -2.75..5.44 | -2.75..5.44 | 0.15 | -1.12..1.42 | 0.1 | 3.83 | 2.69 | -2.75 | -1.12 |
| P2 | fade | complement: no early footprint | 9 | 33 | 7.04 | -3.5 | 0.02 | -3.29..4.28 | -3.73..6.02 | -0.22 | -0.86..0.54 | 0.09 | 4.78 | 0.15 | -9.92 | -2.19 |
| P3 | cont | all | 15 | 60 | 15.62 | -4.31 | 7.64 | 2.04..13.46 | 4.38..10.96 | 0.46 | -0.13..1.05 | 0.05 | 7.76 | 114.67 | -6.67 | -1.24 |
| P3 | cont | FILTERED: early footprint | 9 | 67 | 16.82 | -4.61 | 9.68 | 2.22..17.02 | 3.53..15.34 | 0.66 | -0.04..1.28 | 0.03 | 12.37 | 87.11 | -8.04 | -1.16 |
| P3 | cont | complement: no early footprint | 6 | 50 | 13.21 | -4.02 | 4.59 | -2.96..13.5 | -3.22..13.39 | 0.17 | -0.7..1.04 | 0.08 | 6.38 | 27.57 | -9.71 | -2.16 |
| P3 | fade | all | 17 | 12 | 8.88 | -7.14 | -5.25 | -9.38..-1.51 | -8.95..-1.56 | -0.78 | -1.1..-0.33 | 0.09 | 4.37 | -89.32 | -94.55 | -14.64 |
| P3 | fade | FILTERED: early footprint | 9 | 11 | 12.54 | -10.25 | -7.72 | -14.07..-0.78 | -14.4..-0.47 | -0.78 | -1.08..-0.21 | 0.05 | 6.18 | -69.44 | -69.44 | -6.98 |
| P3 | fade | complement: no early footprint | 8 | 12 | 5.23 | -3.59 | -2.48 | -4.92..0.27 | -5.38..0.37 | -0.78 | -1.18..-0.1 | 0.13 | 3.48 | -19.88 | -25.11 | -7.67 |

## 2. ORIGINAL definition (as first reported), identical 5m execution

Original = all in-session first breaks including levels already crossed between 17:00 and 24:00 UK; 'early footprint' uses the legacy break-anchored baseline.

### Original

| Period | Rule | Subset | n | Win % | Avg win | Avg loss | Exp pts | 95% CI pts (linked) | 95% CI pts (day) | Exp R | 95% CI R | Cost (R) | Med risk | Total pts | Max DD pts | Max DD R |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P1 | cont | all | 145 | 36 | 7.48 | -7.59 | -2.19 | -3.75..-0.67 | -3.8..-0.63 | -0.21 | -0.38..-0.03 | 0.09 | 5.96 | -317.23 | -317.23 | -32.51 |
| P1 | cont | FILTERED: early footprint | 54 | 22 | 9.03 | -9.37 | -5.28 | -8.13..-2.39 | -8.19..-2.21 | -0.4 | -0.65..-0.12 | 0.05 | 7.22 | -285.2 | -285.2 | -21.99 |
| P1 | cont | complement: no early footprint | 91 | 44 | 7.02 | -6.13 | -0.35 | -1.97..1.32 | -1.82..1.13 | -0.09 | -0.33..0.16 | 0.11 | 5.35 | -32.03 | -112.68 | -19.55 |
| P1 | fade | all | 145 | 39 | 7.1 | -6.09 | -0.91 | -2.27..0.57 | -2.28..0.51 | -0.13 | -0.31..0.05 | 0.08 | 4.92 | -131.62 | -165.06 | -28.29 |
| P1 | fade | FILTERED: early footprint | 55 | 38 | 9.56 | -6.58 | -0.42 | -3.16..2.78 | -3.16..2.52 | -0.14 | -0.42..0.14 | 0.07 | 6.81 | -22.95 | -66.39 | -11.69 |
| P1 | fade | complement: no early footprint | 90 | 40 | 5.66 | -5.78 | -1.21 | -2.6..0.17 | -2.41..-0.03 | -0.13 | -0.36..0.11 | 0.08 | 4.54 | -108.67 | -128.86 | -18.05 |
| P2 | cont | all | 14 | 29 | 5.21 | -4.88 | -1.99 | -4.53..0.69 | -4.1..0.35 | -0.35 | -0.9..0.21 | 0.08 | 4.18 | -27.93 | -32.63 | -5.69 |
| P2 | cont | FILTERED: early footprint | 3 | 33 | 4.48 | -6.04 | -2.53 | -9.36..4.48 | -9.36..0.88 | -0.25 | -1.12..1.41 | 0.08 | 3.19 | -7.59 | -12.07 | -2.16 |
| P2 | cont | complement: no early footprint | 11 | 27 | 5.45 | -4.59 | -1.85 | -4.44..1.27 | -3.89..-0.15 | -0.38 | -1.01..0.3 | 0.08 | 4.18 | -20.33 | -25.03 | -4.94 |
| P2 | fade | all | 12 | 42 | 5.74 | -3.39 | 0.41 | -2.33..3.65 | -2.87..4.84 | -0.03 | -0.65..0.67 | 0.1 | 3.83 | 4.96 | -12.67 | -3.32 |
| P2 | fade | FILTERED: early footprint | 1 | 100 | 5.44 |  | 5.44 | None..None | None..None | 1.42 | None..None | 0.08 | 3.83 | 5.44 | 0.0 | 0.0 |
| P2 | fade | complement: no early footprint | 11 | 36 | 5.81 | -3.39 | -0.04 | -2.81..3.38 | -3.67..4.79 | -0.16 | -0.78..0.53 | 0.1 | 3.61 | -0.47 | -12.67 | -3.32 |
| P3 | cont | all | 20 | 50 | 15.59 | -4.93 | 5.33 | 0.52..10.59 | 2.72..8.42 | 0.24 | -0.29..0.77 | 0.06 | 8.07 | 106.61 | -21.94 | -2.51 |
| P3 | cont | FILTERED: early footprint | 11 | 64 | 16.61 | -5.77 | 8.47 | 1.63..15.83 | 5.41..13.02 | 0.58 | -0.08..1.2 | 0.03 | 10.45 | 93.19 | -14.15 | -2.09 |
| P3 | cont | complement: no early footprint | 9 | 33 | 13.21 | -4.37 | 1.49 | -4.08..8.51 | -4.16..7.64 | -0.19 | -0.9..0.63 | 0.09 | 4.28 | 13.42 | -9.71 | -2.35 |
| P3 | fade | all | 19 | 10 | 8.88 | -7.1 | -5.42 | -8.97..-2.06 | -8.62..-2.01 | -0.81 | -1.09..-0.41 | 0.09 | 4.44 | -102.9 | -108.13 | -16.74 |
| P3 | fade | FILTERED: early footprint | 8 | 12 | 12.54 | -8.16 | -5.58 | -10.95..0.8 | -10.6..1.07 | -0.74 | -1.08..-0.1 | 0.06 | 7.54 | -44.6 | -44.6 | -5.96 |
| P3 | fade | complement: no early footprint | 11 | 9 | 5.23 | -6.35 | -5.3 | -10.25..-1.53 | -9.81..-1.19 | -0.85 | -1.14..-0.36 | 0.11 | 3.69 | -58.3 | -63.52 | -10.78 |

## 3. 1-minute execution refinement (corrected events, P2 and P3 only; 1m history ends 2026-10-25)

### Corrected, 1m exits

| Period | Rule | Subset | n | Win % | Avg win | Avg loss | Exp pts | 95% CI pts (linked) | 95% CI pts (day) | Exp R | 95% CI R | Cost (R) | Med risk | Total pts | Max DD pts | Max DD R |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P2 | cont | all | 10 | 30 | 5.45 | -4.26 | -1.35 | -4.05..1.81 | -3.64..-0.01 | -0.34 | -1.07..0.41 | 0.09 | 4.18 | -13.48 | -18.18 | -4.13 |
| P2 | cont | FILTERED: early footprint | 2 | 50 | 5.98 | -2.71 | 1.63 | -2.71..5.98 | -2.71..5.98 | 0.15 | -1.12..1.43 | 0.1 | 4.18 | 3.27 | -2.71 | -1.12 |
| P2 | cont | complement: no early footprint | 8 | 25 | 5.19 | -4.52 | -2.09 | -4.91..1.41 | -5.13..-0.06 | -0.46 | -1.09..0.46 | 0.09 | 4.58 | -16.75 | -16.75 | -3.71 |
| P2 | fade | all | 11 | 36 | 6.64 | -3.39 | 0.26 | -2.69..3.73 | -2.87..5.65 | -0.15 | -0.78..0.55 | 0.09 | 3.83 | 2.83 | -12.67 | -3.32 |
| P2 | fade | FILTERED: early footprint | 2 | 50 | 5.44 | -2.75 | 1.34 | -2.75..5.44 | -2.75..5.44 | 0.15 | -1.12..1.42 | 0.1 | 3.83 | 2.69 | -2.75 | -1.12 |
| P2 | fade | complement: no early footprint | 9 | 33 | 7.04 | -3.5 | 0.02 | -3.29..4.28 | -3.73..6.02 | -0.22 | -0.86..0.54 | 0.09 | 4.78 | 0.15 | -9.92 | -2.19 |
| P3 | cont | all | 15 | 60 | 15.62 | -4.31 | 7.64 | 2.04..13.46 | 4.38..10.96 | 0.46 | -0.13..1.05 | 0.05 | 7.76 | 114.67 | -6.67 | -1.24 |
| P3 | cont | FILTERED: early footprint | 9 | 67 | 16.82 | -4.61 | 9.68 | 2.22..17.02 | 3.53..15.34 | 0.66 | -0.04..1.28 | 0.03 | 12.37 | 87.11 | -8.04 | -1.16 |
| P3 | cont | complement: no early footprint | 6 | 50 | 13.21 | -4.02 | 4.59 | -2.96..13.5 | -3.22..13.39 | 0.17 | -0.7..1.04 | 0.08 | 6.38 | 27.57 | -9.71 | -2.16 |
| P3 | fade | all | 17 | 12 | 8.88 | -7.14 | -5.25 | -9.38..-1.51 | -8.95..-1.56 | -0.78 | -1.1..-0.33 | 0.09 | 4.37 | -89.32 | -94.55 | -14.64 |
| P3 | fade | FILTERED: early footprint | 9 | 11 | 12.54 | -10.25 | -7.72 | -14.07..-0.78 | -14.4..-0.47 | -0.78 | -1.08..-0.21 | 0.05 | 6.18 | -69.44 | -69.44 | -6.98 |
| P3 | fade | complement: no early footprint | 8 | 12 | 5.23 | -3.59 | -2.48 | -4.92..0.27 | -5.38..0.37 | -0.78 | -1.18..-0.1 | 0.13 | 3.48 | -19.88 | -25.11 | -7.67 |

Only one P3 trade changed (a 5m stop/target tie resolved as a stop on 1m: same P&L). No P2 trade changed. Expectancies are identical to 5m at two decimals.

## 4. Event behaviour

| Analysis | Period | Events | Linked groups | Closed back inside in 3 bars | Back inside at +60 | 95% CI share (linked) | Avg +60 pts | Early (PIT) | Early (legacy) | Early label changed |
|---|---|---|---|---|---|---|---|---|---|---|
| ORIGINAL | P1 | 216 | 207 | 150 | 104 | 0.41..0.55 | -1.91 | 95 | 84 | 11 |
| ORIGINAL | P2 | 16 | 16 | 12 | 11 | 0.44..0.88 | 2.32 | 5 | 3 | 2 |
| ORIGINAL | P3 | 30 | 28 | 20 | 9 | 0.14..0.46 | -11.0 | 19 | 16 | 3 |
| CORRECTED - PRIMARY | P1 | 178 | 171 | 133 | 95 | 0.46..0.61 | 0.43 | 77 | 70 | 7 |
| CORRECTED - PRIMARY | P2 | 11 | 11 | 11 | 7 | 0.36..0.91 | 1.43 | 2 | 1 | 1 |
| CORRECTED - PRIMARY | P3 | 24 | 23 | 18 | 9 | 0.20..0.57 | -9.27 | 14 | 12 | 2 |

## 5. Level completeness

| Period | Levels | Tested | Untested | Censored (fewer than 2 later sessions in window) | First crossed outside sessions |
|---|---|---|---|---|---|
| P1 | 360 | 216 | 142 | 2 | 38 |
| P2 | 30 | 16 | 11 | 3 | 5 |
| P3 | 60 | 30 | 27 | 3 | 6 |
