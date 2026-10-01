---
title: Growth model
toc: false
---

```js
import {fmt, sourceBanner, skipped} from "./components/common.js";
const meta = FileAttachment("data/meta.json").json();
const results = FileAttachment("data/analyses.json").json();
```

# Who grows next week?

```js
display(sourceBanner(meta));
```

```js
const target = view(Inputs.radio(new Map([["Growth: hours watched up 10%+", "growth"], ["Drop-off: not live next week", "churn"]]), {value: "growth", label: "Predict"}));
```

```js
const info = meta.analyses[`predict_${target}`];
const metrics = results[`model_metrics_${target}`] ?? [];
const importance = results[`feature_importance_${target}`] ?? [];
const s = skipped(meta, `predict_${target}`);
if (s) display(s);
```

```js
const best = metrics.length ? metrics.filter((d) => !["base_rate", "momentum_rule"].includes(d.model)).sort((a, b) => b.roc_auc - a.roc_auc)[0] : null;
const momentum = metrics.find((d) => d.model === "momentum_rule");
```

```js
if (info?.status === "ok") display(html`<div class="grid grid-cols-4">
  <div class="card"><h2>Best ROC AUC (${best.model.replaceAll("_", " ")})</h2><span class="big">${fmt.num(best.roc_auc, 3)}</span></div>
  <div class="card"><h2>Momentum rule ROC AUC</h2><span class="big">${fmt.num(momentum.roc_auc, 3)}</span></div>
  <div class="card"><h2>Positive rate, test weeks</h2><span class="big">${fmt.pct(info.base_rate_test)}</span></div>
  <div class="card"><h2>Creator-weeks (train / test)</h2><span class="big">${fmt.compact(info.train_rows)} / ${fmt.compact(info.test_rows)}</span></div>
</div>
<p class="caption">Time-based split: trained on weeks starting ${info.train_weeks[0]} to ${info.train_weeks.at(-1)}, tested on ${info.test_weeks.join(" and ")}. The model never sees weeks after the ones it is scored on. An AUC below 0.5 for the momentum rule means last week's change tends to reverse.</p>`);
```

<div class="grid grid-cols-2">
<div class="card">
<h2>ROC AUC on held-out weeks</h2>
<h3>0.5 is a coin flip</h3>

```js
if (metrics.length) display(resize((width) => Plot.plot({
  width,
  height: 40 + metrics.length * 36,
  marginLeft: 150,
  marginRight: 48,
  x: {domain: [0, 1], grid: true, label: "ROC AUC", axis: "top"},
  y: {label: null, domain: metrics.map((d) => d.model), tickFormat: (d) => d.replaceAll("_", " ")},
  marks: [
    Plot.barX(metrics, {y: "model", x: "roc_auc", fill: (d) => (d === best ? "var(--series-1)" : "var(--muted-mark)"), rx: 2, insetTop: 7, insetBottom: 7,
      tip: true, title: (d) => `${d.model.replaceAll("_", " ")}\nROC AUC ${fmt.num(d.roc_auc)}\nPR AUC ${fmt.num(d.pr_auc)}`}),
    Plot.text(metrics, {y: "model", x: "roc_auc", text: (d) => fmt.num(d.roc_auc, 2), dx: 6, textAnchor: "start", fill: "var(--theme-foreground-muted)"}),
    Plot.ruleX([0.5], {stroke: "var(--theme-foreground-muted)", strokeDasharray: null}),
    Plot.ruleX([0], {stroke: "var(--baseline)"})
  ]
})));
```
</div>
<div class="card">
<h2>What drives the prediction</h2>
<h3>Drop in test ROC AUC when the feature is shuffled (gradient boosting)</h3>

```js
const topImp = importance.slice(0, 10);
if (topImp.length) display(resize((width) => Plot.plot({
  width,
  height: 40 + topImp.length * 26,
  marginLeft: 190,
  x: {grid: true, label: "AUC drop", axis: "top"},
  y: {label: null, domain: topImp.map((d) => d.feature), tickFormat: (d) => d.replaceAll("_", " ")},
  marks: [
    Plot.barX(topImp, {y: "feature", x: "permutation_auc_drop", fill: "var(--series-1)", rx: 2, insetTop: 5, insetBottom: 5,
      tip: true, title: (d) => `${d.feature.replaceAll("_", " ")}\nAUC drop ${fmt.num(d.permutation_auc_drop, 4)} ± ${fmt.num(d.permutation_std, 4)}\nlogistic coef ${fmt.num(d.logistic_coef, 3)}`}),
    Plot.ruleY(topImp, {y: "feature", x1: (d) => d.permutation_auc_drop - d.permutation_std, x2: (d) => d.permutation_auc_drop + d.permutation_std, stroke: "var(--theme-foreground-muted)"}),
    Plot.ruleX([0], {stroke: "var(--baseline)"})
  ]
})));
```
</div>
</div>

```js
if (metrics.length) display(Inputs.table(metrics, {
  layout: "auto",
  columns: ["model", "roc_auc", "pr_auc", "brier"],
  header: {model: "Model", roc_auc: "ROC AUC", pr_auc: "PR AUC (avg precision)", brier: "Brier score"},
  format: {model: (d) => d.replaceAll("_", " "), roc_auc: (d) => fmt.num(d), pr_auc: (d) => fmt.num(d), brier: (d) => (d == null ? "n/a" : fmt.num(d))},
  select: false
}));
```

<p class="caption">Unit: a creator live in a complete week. Growth means hours watched in the following week are at least 10% higher (a creator who goes dark counts as not growing). Features describe the current week and the creator's history only. PR AUC should be compared with the positive rate, which is what a random ranking scores.</p>
