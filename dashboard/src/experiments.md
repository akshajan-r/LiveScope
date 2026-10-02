---
title: Experiments
toc: false
---

```js
import {fmt, sourceBanner, skipped, key} from "./components/common.js";
const meta = FileAttachment("data/meta.json").json();
const results = FileAttachment("data/analyses.json").json();
```

# Experiments

```js
display(sourceBanner(meta));
```

## Natural experiment: moving into peak hours

Does a creator's audience change when they move more of their streaming into the platform's peak hours? Treated creators raised the share of their live hours that fall in peak hours by at least 25 points between the three weeks before and the three weeks after the split week; control creators changed it by less than 5 points. Difference-in-differences on log average viewers, standard errors clustered by creator.

```js
const didSkip = skipped(meta, "did_peak_hours");
if (didSkip) display(didSkip);
const did = results.did_summary?.[0];
const es = results.did_event_study ?? [];
```

```js
if (did) display(html`<div class="grid grid-cols-4">
  <div class="card"><h2>Estimated effect on avg viewers</h2><span class="big">${fmt.signedPct(did.pct_effect)}</span></div>
  <div class="card"><h2>95% CI</h2><span class="big">${fmt.signedPct(Math.expm1(did.ci_low), 0)} to ${fmt.signedPct(Math.expm1(did.ci_high), 0)}</span></div>
  <div class="card"><h2>Creators (treated / control)</h2><span class="big">${fmt.int(did.n_treated)} / ${fmt.int(did.n_control)}</span></div>
  <div class="card"><h2>Pre-trend test p-value</h2><span class="big">${fmt.num(did.pretrend_p_value, 2)}</span></div>
</div>`);
```

```js
if (es.length) display(html`<div class="card"><h2>Event study</h2><h3>Treated minus control, log average viewers, relative to the week before the move (week −1). Bars are 95% CIs.</h3>${resize((width) => Plot.plot({
  width,
  height: 300,
  x: {label: "Weeks relative to the split week", ticks: es.map((d) => d.rel_week), tickFormat: (d) => (d > 0 ? `+${d}` : `${d}`)},
  y: {grid: true, label: "Effect on avg viewers", tickFormat: (d) => fmt.signedPct(Math.expm1(d), 0)},
  marks: [
    Plot.ruleY([0], {stroke: "var(--baseline)"}),
    Plot.ruleX([-0.5], {stroke: "var(--theme-foreground-muted)"}),
    Plot.text([{x: -0.5}], {x: "x", frameAnchor: "top", text: () => "move", dx: 4, textAnchor: "start", fill: "var(--theme-foreground-muted)"}),
    Plot.ruleX(es, {x: "rel_week", y1: "ci_low", y2: "ci_high", stroke: "var(--series-1)", strokeWidth: 2}),
    Plot.dot(es, {x: "rel_week", y: "estimate", r: 5, fill: "var(--series-1)", stroke: "var(--theme-background)", strokeWidth: 2,
      tip: true, title: (d) => `Week ${d.rel_week}\n${fmt.signedPct(Math.expm1(d.estimate))} (${fmt.signedPct(Math.expm1(d.ci_low))} to ${fmt.signedPct(Math.expm1(d.ci_high))})`})
  ]
}))}</div>`);
```

<p class="caption">This is observational. Creators choose when to stream, so the estimate is only credible if treated and control creators were on parallel trends before the move: the pre-period points should sit near zero and the pre-trend test should not reject. Other things that change at the same time (a new game, a collaboration) would also be picked up. Peak hours are defined from the same data (top six UTC hours by total viewers).</p>

## A/B testing toolkit, validated by simulation

```js
const val = results.abtest_validation ?? [];
```

The toolkit (`livescope.experiments`) covers sample-size and power calculations, the two-proportion z-test, Welch's t-test, CUPED variance reduction, a sample-ratio-mismatch check and non-inferiority guardrails. Each test is checked on ${fmt.int(meta.analyses.abtest_validation?.simulations)} simulated A/A tests (no true effect, so about 5% should come out significant) and A/B tests sized for 80% power.

```js
const valRows = val.filter((d) => d.nominal != null && d.test !== "CUPED variance reduction").map((d) => ({...d, label: `${d.test} · ${d.scenario}`}));
if (valRows.length) {
  display(key([["Empirical rate", "var(--series-1)"], ["Target", "var(--theme-foreground-muted)"]]));
  display(resize((width) => Plot.plot({
    width,
    height: 40 + valRows.length * 34,
    marginLeft: 230,
    x: {domain: [0, 1], grid: true, label: "Share of simulated experiments significant", tickFormat: "%", axis: "top"},
    y: {label: null, domain: valRows.map((d) => d.label)},
    marks: [
      Plot.tickX(valRows, {y: "label", x: "nominal", stroke: "var(--theme-foreground-muted)", strokeWidth: 2}),
      Plot.dot(valRows, {y: "label", x: "empirical", r: 5, fill: "var(--series-1)", stroke: "var(--theme-background)", strokeWidth: 2,
        tip: true, title: (d) => `${d.label}\nempirical ${fmt.pct(d.empirical)}\ntarget ${fmt.pct(d.nominal)}\nn per group ${fmt.int(d.n_per_group)}`})
    ]
  })));
}
```

```js
const cupedPower = val.find((d) => d.test === "CUPED t-test" && d.scenario === "A/B");
const rawPower = val.find((d) => d.test === "welch t-test" && d.scenario === "A/B");
const vr = val.find((d) => d.test === "CUPED variance reduction");
if (cupedPower && rawPower && vr) display(html`<p class="caption">With a pre-period covariate correlated at ρ = 0.6, CUPED removed ${fmt.pct(vr.empirical, 0)} of the variance (theory: ρ² = ${fmt.pct(vr.nominal, 0)}) and raised power from ${fmt.pct(rawPower.empirical, 0)} to ${fmt.pct(cupedPower.empirical, 0)} at the same sample size, while keeping the A/A false-positive rate near 5%.</p>`);
```
