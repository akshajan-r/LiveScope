# Experiment plan: `<flag-key>`

Commit this file before the experiment starts. Do not edit the sections above "Results" after launch.

| | |
|---|---|
| Owner | |
| Client sign-off | (who, when) |
| Flag key | `<flag-key>` |
| Variants | `control` (current) / `test` (change) at 50/50 |
| Start (UTC) | YYYY-MM-DD |
| End (UTC, exclusive) | YYYY-MM-DD (whole weeks) |

## Hypothesis

Changing **X** to **Y** will increase **metric** because **reason**.

## Metrics

- **Primary:** event `...`, analysed as the share of exposed people who trigger it after first exposure.
- **Guardrails:** (e.g. a "contact form error" event must not rise by more than 1 pp).
- **Covariate for CUPED:** the same event in the 14 days before the start.

## Sample size

Output of `python -m livescope experiment-plan --baseline ... --mde ... --daily-users ...`:

```
(paste here)
```

Baseline and traffic come from: (PostHog insight, date range).

## Decision rule

Ship if the primary metric improves at p < 0.05, the sample-ratio check passes and every guardrail passes. Otherwise keep control. No early stopping.

## Results

(Paste `exports/experiments/<flag-key>/readout.md` here after the end date.)

## What we learned
