# Experiment analysis

## A/B testing toolkit (`livescope.experiments`)

| Module | Contents |
|---|---|
| `power` | sample size for proportions and means (with optional CUPED variance reduction), power, minimum detectable effect, test duration |
| `significance` | two-proportion z-test, Welch's t-test, sample-ratio-mismatch check, non-inferiority guardrail test |
| `cuped` | CUPED adjustment with a pooled theta |
| `analyze` | one call: SRM → primary metric (raw and CUPED) → guardrails → ship / don't ship / inconclusive |
| `simulate` | simulated A/A and A/B experiments that check the false-positive rate and power |

```python
from livescope.experiments.power import sample_size_proportions, mde_proportions, duration_days
from livescope.experiments.analyze import analyze_experiment, Guardrail

# 8% baseline conversion, detect a 10% relative lift at alpha 0.05, power 0.8
n_control, n_treatment = sample_size_proportions(p_control=0.08, mde=0.10, relative=True)
# -> 18,872 per group; at 2,000 eligible users a day that is 19 days (run 3 full weeks)
duration_days(n_control + n_treatment, daily_eligible_users=2000)

# Smallest lift detectable with 5,000 users per group: about 1.6 percentage points
mde_proportions(0.08, 5000)

# df: one row per user with columns group, post (metric), pre (same metric before the test), error (0/1)
result = analyze_experiment(
    df, primary="post", pre_period="pre",
    guardrails=[Guardrail("error", margin=0.005, higher_is_better=False)],
)
result["decision"]  # e.g. "ship: primary metric improved and guardrails held"
```

### Validation

`python -m livescope abtest-validate` runs 1,000 simulated A/A and A/B experiments per test. The published dashboard shows the latest run (500 simulations). Pass criteria, checked in `tests/test_experiments.py`:

- A/A tests come out significant about 5% of the time (the false-positive rate equals alpha);
- A/B tests sized with `power.py` come out significant about 80% of the time;
- CUPED removes about ρ² of the variance and raises power without raising the false-positive rate;
- the z-test, Welch's test and the power formulas agree with `statsmodels` and `scipy`.

### Conventions

- Decide the primary metric, guardrails, sample size and duration before the test starts; analyse once at the planned end (the tests here are fixed-horizon, not sequential, so peeking inflates false positives).
- Run whole weeks to average out day-of-week effects.
- Check SRM first. A mismatch means assignment or logging is broken and nothing else in the readout can be trusted.
- Guardrails use non-inferiority: "no worse than the margin", tested with the 95% CI, rather than "not significantly worse".

## Natural experiment: peak hours (`livescope.causal.did`)

Question: when a creator moves more of their streaming into platform peak hours, does their average audience change?

- **Split week**: the middle complete week (configurable).
- **Treated**: creators whose peak-hour share of live hours rose by ≥ 25 points from the 3 weeks before the split to the 3 weeks from it.
- **Control**: creators whose share moved by < 5 points. Everyone in between is dropped.
- **Outcome**: log(1 + average viewers), so the estimate reads as a percentage change.
- **Estimators**: 2×2 DiD on creator-period means with creator-clustered SEs; an event study with creator and week fixed effects (week −1 as reference); a pre-period test that the treated-control gap does not trend.

Read it as evidence, not proof: creators choose when to stream, and anything that changes at the same time as the schedule (a new game, a collaboration, a holiday) is attributed to the move. The event study's pre-period points and the pre-trend test are the minimum checks.

## Running a real A/B test

The toolkit is validated on simulations; it has not analysed a real experiment yet. To get one, run a small feature-flag experiment (for example with PostHog's free tier) on a site you control, export one row per user with group, outcome and a pre-period value, and pass it to `analyze_experiment`.
