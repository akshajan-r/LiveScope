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

## Running a real A/B test (PostHog)

Everything above is validated on simulations. The only honest way to say "ran an A/B test" is to run one. This is the runbook for a small feature-flag experiment on a client's website, analysed with this toolkit.

### 1. Agree the test with the client

Get written agreement on what changes, who sees it and how long it runs. Pick a change that could plausibly move a metric the client cares about (for example the wording or placement of a booking or contact button).

### 2. Pick a metric the site's traffic can actually test

Small sites have little traffic, so plan first:

```bash
# 150 visitors a day, 4% currently click "Book", hoping for +25%
python -m livescope experiment-plan --baseline 0.04 --mde 0.25 --daily-users 150
#   6,745 people per group, 90 days at 150 people/day -> run 13 full weeks
#   If capped at 4 weeks: smallest detectable change 1.87 pp (47% relative)
```

If the answer is months, choose a metric closer to the change with a higher baseline (a click on the changed element instead of a completed booking), accept that only a large effect is detectable and say so in the write-up, or run longer. Record the decision before starting.

### 3. Write the plan before starting

Copy [`experiment-template.md`](experiment-template.md) to `docs/experiments/<flag>.md` and fill it in: hypothesis, primary metric, guardrails, sample size, start and end dates. Commit it before launch; that commit is your pre-registration.

### 4. Set up PostHog

1. Create a PostHog project. Use **EU Cloud** (`eu.posthog.com`) for a European client's visitors, and check the consent setup with the client: under GDPR, analytics cookies need consent. Either show a consent banner or run posthog-js cookieless (`persistence: "memory"`); cookieless mode treats a returning visitor as new, so sessions rather than people are randomised.
2. Add posthog-js to the site and identify the conversion event, e.g. `posthog.capture("booking_clicked")` on the button.
3. Create a **multivariate feature flag**, key e.g. `cta-copy`, with variants `control` and `test` at 50/50.
4. Render the change from the flag. Calling the flag records the exposure event (`$feature_flag_called`) that the readout uses:

```js
posthog.onFeatureFlags(() => {
  if (posthog.getFeatureFlag("cta-copy") === "test") {
    document.querySelector("#book").textContent = "Check availability";
  }
});
```

5. Test both variants yourself (PostHog lets you override a flag per user), then launch.

### 5. Run it, then read it out once

Do not stop early because the numbers look good: these are fixed-horizon tests, and peeking inflates false positives. At the planned end:

```bash
export POSTHOG_HOST=https://eu.posthog.com POSTHOG_PROJECT_ID=12345 POSTHOG_API_KEY=phx_...   # personal API key, query:read
python -m livescope experiment-readout --flag cta-copy --event booking_clicked \
    --start 2026-10-12 --end 2026-11-09
```

The readout pulls exposures and events through PostHog's query API, keeps the first variant each person saw (people shown both are dropped and counted), and reports the sample-ratio check, the conversion difference with its 95% CI, a CUPED-adjusted estimate using each person's pre-period activity, guardrails, the effect size the sample could detect, and a decision. It is written to `exports/experiments/<flag>/readout.md`.

The person-level table is never saved, because it contains the client's visitors' ids. Commit only the readout and the plan. Without API access, export a CSV with `person_id, variant, converted, pre_count` and pass `--csv`.

### 6. Report honestly

State the result with its interval ("+1.1 pp, 95% CI −0.4 to +2.6 pp, inconclusive") and the detectable effect. An inconclusive result from a well-run test is still a real A/B test, and saying what the test could and could not detect is the part interviewers probe.
