---
title: Retention
toc: false
sql:
  cohort_retention: ./data/cohort_retention.arrow
---

```js
import {fmt, sourceBanner, skipped, key, kmPlot, SLOTS, toDate, sequentialRange} from "./components/common.js";
const meta = FileAttachment("data/meta.json").json();
const results = FileAttachment("data/analyses.json").json();
```

# Creator retention

```js
display(sourceBanner(meta));
```

Once a creator breaks into the top ${fmt.int(meta.max_streams_per_snapshot)}, do they keep streaming? Every creator who enters the top list joins the tracking panel and is checked every hour from then on, whatever their audience, so "not seen" means "not live". A creator counts as having stopped after **two complete weeks without going live**.

```js
const surv = skipped(meta, "survival");
if (surv) display(surv);
const curves = results.survival_curves ?? [];
const milestones = results.survival_milestones ?? [];
const groupNames = [...new Set(curves.map((d) => d.group))];
const m = (group, weeks) => milestones.find((d) => d.group === group && d.weeks === String(weeks));
```

```js
const all = (w) => m("All newcomers", w);
if (curves.length && all(1)) display(html`<div class="grid grid-cols-4">
  <div class="card"><h2>Newcomers tracked</h2><span class="big">${fmt.int(all(1).creators)}</span></div>
  ${[1, 4, 8].map((w) => html`<div class="card"><h2>Still streaming after ${w} week${w > 1 ? "s" : ""}</h2>
    <span class="big">${all(w)?.survival == null ? "–" : fmt.pct(all(w).survival, 0)}</span>
    <p class="caption">${all(w)?.survival == null ? "Not enough follow-up yet" : `95% CI ${fmt.pct(all(w).ci_low, 0)}–${fmt.pct(all(w).ci_high, 0)} · ${fmt.int(all(w).at_risk)} still followed`}</p></div>`)}
</div>`);
```

```js
const kmGroups = ["All newcomers", "Founding cohort"].filter((g) => groupNames.includes(g));
if (kmGroups.length) {
  display(html`<div class="card"><h2>Kaplan–Meier survival</h2><h3>Share of creators still streaming, by weeks since they entered the top list. Shaded bands are 95% confidence intervals.</h3>
    ${key(kmGroups.map((g, i) => [g, SLOTS[i]]))}
    ${resize((width) => kmPlot(curves, kmGroups, SLOTS.slice(0, kmGroups.length), {width}))}</div>`);
}
```

<p class="caption">Newcomers are creators who first entered the top list after collection began. The founding cohort entered in the first collection week; most of them were already established, so their curve shows how long existing creators keep going, not how new ones fare. Kaplan–Meier keeps creators who are still streaming (censored) in the estimate up to the point they have been followed, so recent cohorts contribute without biasing the curve.</p>

## Cohorts

```sql id=cohorts
select cohort_week, founding_cohort, weeks_since, cohort_size, active, retention
from cohort_retention
order by cohort_week, weeks_since
```

```js
const cohortRows = [...cohorts].map((d) => ({...d, cohort_week: fmt.date(toDate(d.cohort_week)), weeks_since: Number(d.weeks_since),
  cohort_size: Number(d.cohort_size), active: Number(d.active), retention: Number(d.retention)}))
  .map((d) => ({...d, cohort: `${d.cohort_week}${d.founding_cohort ? " (founding)" : ""}`}));
const cohortNames = [...new Set(cohortRows.map((d) => d.cohort))];
if (cohortRows.length) display(html`<div class="card"><h2>Share of each cohort live in each later week</h2>
  <h3>Rows are the week creators first entered the top list; columns count weeks since then. Stronger colour is higher.</h3>
  ${resize((width) => Plot.plot({
    width,
    height: 50 + cohortNames.length * 28,
    marginLeft: 140,
    padding: 0.06,
    x: {label: "Weeks since entering the top list", axis: "top", tickFormat: "d"},
    y: {label: null, domain: cohortNames},
    color: {type: "linear", domain: [0, 1], range: sequentialRange(), legend: true, label: "Share live", tickFormat: "%"},
    marks: [
      Plot.cell(cohortRows, {x: "weeks_since", y: "cohort", fill: "retention", rx: 2,
        tip: true, title: (d) => `Cohort ${d.cohort}\nweek ${d.weeks_since}: ${fmt.pct(d.retention, 0)} live\n${fmt.int(d.active)} of ${fmt.int(d.cohort_size)} creators`})
    ]
  }))}</div>`);
```

<p class="caption">Unlike the survival curve, this counts a creator as retained in a week only if they went live that week, so a creator who skips a week and comes back dips and recovers. Week 0 is always 100%.</p>

```js
if (milestones.length) display(Inputs.table(milestones.filter((d) => d.weeks !== "median"), {
  layout: "auto",
  columns: ["group", "weeks", "survival", "ci_low", "ci_high", "at_risk", "creators"],
  header: {group: "Group", weeks: "Weeks", survival: "Still streaming", ci_low: "95% CI low", ci_high: "95% CI high", at_risk: "Still followed", creators: "Creators"},
  format: {survival: (d) => (d == null ? "–" : fmt.pct(d, 0)), ci_low: (d) => (d == null ? "–" : fmt.pct(d, 0)), ci_high: (d) => (d == null ? "–" : fmt.pct(d, 0)), at_risk: fmt.int},
  select: false
}));
```
