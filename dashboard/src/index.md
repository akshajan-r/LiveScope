---
title: Overview
toc: false
sql:
  platform_hour: ./data/platform_hour.arrow
  peak_hours: ./data/peak_hours.arrow
  category_week: ./data/category_week.arrow
  collector_weeks: ./data/collector_weeks.arrow
  platform_week: ./data/platform_week.arrow
  collection_runs: ./data/collection_runs.arrow
---

```js
import {fmt, sourceBanner, key, toDate} from "./components/common.js";
const meta = FileAttachment("data/meta.json").json();
```

# LiveScope

Which creators are growing, which are at risk of dropping off, and what helps them grow? This dashboard is rebuilt by GitHub Actions after every hourly snapshot.

```js
display(sourceBanner(meta));
```

<div class="grid grid-cols-4">
  <div class="card"><h2>Snapshot rows</h2><span class="big">${fmt.compact(meta.snapshot_rows)}</span></div>
  <div class="card"><h2>Creators observed</h2><span class="big">${fmt.compact(meta.creators)}</span></div>
  <div class="card"><h2>Hourly snapshots</h2><span class="big">${fmt.int(meta.snapshot_hours)}</span></div>
  <div class="card"><h2>Complete weeks</h2><span class="big">${fmt.int(meta.complete_weeks)}</span></div>
</div>

<p class="caption">Data from ${fmt.date(meta.first_snapshot)} to ${fmt.date(meta.last_snapshot)} (UTC). Each snapshot holds the top ${fmt.int(meta.max_streams_per_snapshot)} live streams by viewers plus every live stream of the ${fmt.int(meta.panel_max)}-creator tracking panel. Last built ${meta.generated_at}.</p>

## Collection log

```sql id=runs
select snapshot_at, status, top_rows, panel_rows, panel_size, issues from collection_runs order by snapshot_at
```

```js
const runRows = [...runs].map((d) => ({...d, snapshot_at: toDate(d.snapshot_at), top_rows: Number(d.top_rows),
  panel_rows: Number(d.panel_rows), panel_size: Number(d.panel_size), issues: Number(d.issues)}));
const okRuns = runRows.filter((d) => d.status === "ok");
const lastRun = okRuns.at(-1);
const perDay = d3.rollups(okRuns, (v) => new Set(v.map((d) => d.snapshot_at.toISOString().slice(0, 13))).size,
  (d) => d.snapshot_at.toISOString().slice(0, 10)).map(([day, hours]) => ({day, hours}));
```

```js
if (!runRows.length) {
  display(html`<p class="caption">No collector runs recorded (synthetic data has none).</p>`);
} else {
  display(html`<div class="grid grid-cols-3">
    <div class="card"><h2>Snapshots collected</h2><span class="big">${fmt.int(okRuns.length)}</span>
      <p class="caption">${runRows.length - okRuns.length ? `${runRows.length - okRuns.length} failed runs` : "No failed runs"}</p></div>
    <div class="card"><h2>Latest snapshot (UTC)</h2><span class="big">${lastRun ? lastRun.snapshot_at.toISOString().slice(11, 16) : "–"}</span>
      <p class="caption">${lastRun ? fmt.date(lastRun.snapshot_at) : ""}</p></div>
    <div class="card"><h2>Creators in the tracking panel</h2><span class="big">${lastRun ? fmt.int(lastRun.panel_size) : "–"}</span></div>
  </div>`);
  display(html`<div class="card"><h2>Hours captured per day</h2><h3>One snapshot an hour means 24 a day; the line marks 24. Today is still filling in.</h3>
    ${resize((width) => Plot.plot({
      width, height: 200, marginLeft: 40,
      x: {label: null, type: "point", tickFormat: (d) => d.slice(5), padding: 0.6},
      y: {grid: true, label: "Hours captured", domain: [0, 24], ticks: [0, 6, 12, 18, 24]},
      marks: [
        // A fixed-width rule instead of a band bar, so one day does not fill the chart.
        Plot.ruleX(perDay, {x: "day", y1: 0, y2: "hours", stroke: "var(--series-1)", strokeWidth: Math.min(20, (width - 60) / perDay.length * 0.6),
          tip: true, title: (d) => `${d.day}\n${d.hours} of 24 hours captured`}),
        Plot.ruleY([24], {stroke: "var(--theme-foreground-muted)"}),
        Plot.ruleY([0], {stroke: "var(--baseline)"})
      ]
    }))}</div>`);
  display(Inputs.table(runRows.slice().reverse(), {
    layout: "auto",
    columns: ["snapshot_at", "status", "top_rows", "panel_rows", "panel_size", "issues"],
    header: {snapshot_at: "Run (UTC)", status: "Status", top_rows: "Top-list streams", panel_rows: "Panel-only streams", panel_size: "Panel size", issues: "Quality notes"},
    format: {snapshot_at: (d) => d.toISOString().slice(0, 16).replace("T", " "), top_rows: fmt.int, panel_rows: fmt.int, panel_size: fmt.int},
    rows: 6, select: false
  }));
}
```

<p class="caption">The dashboard rebuilds after each new snapshot. The same log, updated even when the dashboard is not, is on the <a href="https://github.com/akshajan-r/LiveScope/tree/data">data branch</a>.</p>

## Weekly KPIs

```sql id=kpis
select * from platform_week order by week_start
```

```js
const kpiRows = [...kpis].map((d) => ({...d, week_start: toDate(d.week_start), viewer_hours: Number(d.viewer_hours), active_creators: Number(d.active_creators)}));
const lastKpi = kpiRows.at(-1);
function kpiChart(y, label, tickFormat, format) {
  const rows = kpiRows.filter((d) => d[y] != null && !Number.isNaN(d[y]));
  if (!rows.length) return html`<p class="caption">Needs more complete weeks.</p>`;
  return resize((width) => Plot.plot({
    width, height: 170, marginLeft: 48,
    x: {type: "utc", label: null, ticks: 4},
    y: {grid: true, label: null, tickFormat, zero: true},
    marks: [
      Plot.lineY(rows, {x: "week_start", y, stroke: "var(--series-1)", strokeWidth: 2}),
      Plot.dot(rows, {x: "week_start", y, fill: "var(--series-1)", stroke: "var(--theme-background)", strokeWidth: 2, r: 4,
        tip: true, title: (d) => `Week of ${fmt.date(d.week_start)}\n${label}: ${format(d[y])}`}),
      Plot.ruleY([0], {stroke: "var(--baseline)"})
    ]
  }));
}
```

```js
if (!kpiRows.length) display(html`<p class="skipped">Weekly KPIs appear once the first week is complete.</p>`);
```

<div class="grid grid-cols-4">
  <div class="card"><h2>North star: hours watched, latest week</h2><span class="big">${lastKpi ? fmt.compact(lastKpi.viewer_hours) : "–"}</span>
    <p class="caption">${lastKpi?.viewer_hours_wow == null ? "No previous week to compare" : `${fmt.signedPct(lastKpi.viewer_hours_wow)} vs previous week`}</p></div>
  <div class="card"><h2>KR1: weekly active creators</h2><span class="big">${lastKpi ? fmt.int(lastKpi.active_creators) : "–"}</span></div>
  <div class="card"><h2>KR3: median hours watched per creator</h2><span class="big">${lastKpi ? fmt.compact(lastKpi.median_viewer_hours_per_creator) : "–"}</span></div>
  <div class="card"><h2>Guardrail: top 1% share of hours watched</h2><span class="big">${lastKpi ? fmt.pct(lastKpi.top1pct_share, 0) : "–"}</span></div>
</div>

<div class="grid grid-cols-2">
  <div class="card"><h2>Hours watched per week (north star)</h2>${kpiChart("viewer_hours", "Hours watched", "s", fmt.int)}</div>
  <div class="card"><h2>Weekly active creators (KR1)</h2>${kpiChart("active_creators", "Active creators", "s", fmt.int)}</div>
  <div class="card"><h2>Drop-off rate: live this week, not next (KR2)</h2>${kpiChart("drop_off_rate", "Drop-off", "%", (d) => fmt.pct(d))}</div>
  <div class="card"><h2>Top 1% share of hours watched (guardrail)</h2>${kpiChart("top1pct_share", "Top 1% share", "%", (d) => fmt.pct(d))}</div>
</div>

<p class="caption">Definitions and the OKR tree are in <a href="https://github.com/akshajan-r/LiveScope/blob/main/docs/metrics.md">docs/metrics.md</a>. Drop-off needs the following week and 4-week retention needs four more, so the latest points fill in later.</p>

## Activity by hour

```sql id=hourly
select snapshot_hour, total_viewers, live_creators from platform_hour order by snapshot_hour
```

<div class="card">
<h2>Concurrent viewers on observed streams</h2>
<h3>Sum of viewer counts across all captured streams, per hourly snapshot</h3>

```js
const hourlyRows = [...hourly].map((d) => ({...d, snapshot_hour: toDate(d.snapshot_hour), total_viewers: Number(d.total_viewers)}));
display(resize((width) => Plot.plot({
  width,
  height: 280,
  marginLeft: 56,
  y: {grid: true, label: "Concurrent viewers", tickFormat: "s"},
  x: {label: null},
  marks: [
    Plot.areaY(hourlyRows, {x: "snapshot_hour", y: "total_viewers", fill: "var(--series-1)", fillOpacity: 0.1}),
    Plot.lineY(hourlyRows, {x: "snapshot_hour", y: "total_viewers", stroke: "var(--series-1)", strokeWidth: 2}),
    Plot.ruleX(hourlyRows, Plot.pointerX({x: "snapshot_hour", stroke: "var(--baseline)"})),
    Plot.dot(hourlyRows, Plot.pointerX({x: "snapshot_hour", y: "total_viewers", fill: "var(--series-1)", r: 4, stroke: "var(--theme-background)", strokeWidth: 2})),
    Plot.tip(hourlyRows, Plot.pointerX({x: "snapshot_hour", y: "total_viewers",
      title: (d) => `${d.snapshot_hour.toISOString().slice(0, 13).replace("T", " ")}:00 UTC\n${fmt.int(d.total_viewers)} viewers\n${fmt.int(d.live_creators)} live creators`})),
    Plot.ruleY([0], {stroke: "var(--baseline)"})
  ]
})));
```
</div>

```sql id=peaks
select hour_utc, avg_total_viewers, is_peak from peak_hours order by hour_utc
```

```sql id=cats
with latest as (select max(week_start) as w from category_week)
select game_name, viewer_hours, creators
from category_week, latest
where week_start = latest.w
order by viewer_hours desc
limit 12
```

<div class="grid grid-cols-2">
<div class="card">
<h2>Average audience by hour of day (UTC)</h2>
<h3>The six highest hours define "peak hours" used in the metrics and the natural experiment</h3>

```js
display(key([["Peak hour", "var(--series-1)"], ["Other hours", "var(--muted-mark)"]]));
const peakRows = [...peaks].map((d) => ({...d, avg_total_viewers: Number(d.avg_total_viewers)}));
display(resize((width) => Plot.plot({
  width,
  height: 260,
  marginLeft: 56,
  x: {label: "Hour (UTC)", tickFormat: (d) => (d % 3 === 0 ? String(d).padStart(2, "0") : ""), tickSize: 0, padding: 0.2},
  y: {grid: true, label: "Avg concurrent viewers", tickFormat: "s"},
  marks: [
    Plot.barY(peakRows, {x: "hour_utc", y: "avg_total_viewers", fill: (d) => (d.is_peak ? "var(--series-1)" : "var(--muted-mark)"), rx: 2, tip: {format: {fill: false}}}),
    Plot.ruleY([0], {stroke: "var(--baseline)"})
  ]
})));
```
</div>

<div class="card">
<h2>Top categories, latest week</h2>
<h3>Hours watched (estimated from hourly snapshots)</h3>

```js
const catRows = [...cats].map((d) => ({...d, viewer_hours: Number(d.viewer_hours), creators: Number(d.creators)}));
display(resize((width) => Plot.plot({
  width,
  height: 30 + catRows.length * 24,
  marginLeft: 150,
  marginRight: 56,
  x: {grid: true, label: "Hours watched", tickFormat: "s", axis: "top"},
  y: {label: null, domain: catRows.map((d) => d.game_name)},
  marks: [
    Plot.barX(catRows, {y: "game_name", x: "viewer_hours", fill: "var(--series-1)", rx: 2, insetTop: 4, insetBottom: 4,
      tip: true, title: (d) => `${d.game_name}\n${fmt.int(d.viewer_hours)} hours watched\n${fmt.int(d.creators)} creators`}),
    Plot.text(catRows, {y: "game_name", x: "viewer_hours", text: (d) => fmt.compact(d.viewer_hours), dx: 6, textAnchor: "start", fill: "var(--theme-foreground-muted)"}),
    Plot.ruleX([0], {stroke: "var(--baseline)"})
  ]
})));
```
</div>
</div>

## Collection coverage

```sql id=coverage
select week_start, hours_observed, coverage, is_complete from collector_weeks order by week_start desc
```

```js
display(Inputs.table(coverage, {
  layout: "auto",
  columns: ["week_start", "hours_observed", "coverage", "is_complete"],
  header: {week_start: "Week (Mon)", hours_observed: "Hours captured", coverage: "Coverage", is_complete: "Used for weekly metrics"},
  format: {week_start: fmt.date, coverage: (d) => fmt.pct(d, 0), is_complete: (d) => (d ? "yes" : "no")},
  rows: 8
}));
```

<p class="caption">A week counts as complete when it has ended and at least 90% of its 168 hourly snapshots succeeded. Week-on-week growth, segmentation and the model only use complete weeks.</p>
