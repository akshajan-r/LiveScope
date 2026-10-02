---
title: Creators & segments
toc: false
sql:
  creator_week: ./data/creator_week.arrow
  creator_summary: ./data/creator_summary.arrow
---

```js
import {fmt, sourceBanner, skipped, key, toDate} from "./components/common.js";
const meta = FileAttachment("data/meta.json").json();
const results = FileAttachment("data/analyses.json").json();
```

# Creators & segments

```js
display(sourceBanner(meta));
```

## Who moved last week

```js
const direction = view(Inputs.radio(["Fastest growing", "Fastest declining"], {value: "Fastest growing", label: "Show"}));
const minViewers = view(Inputs.range([0, 1000], {value: 20, step: 5, label: "Min. avg viewers"}));
```

```sql id=movers
with w as (select max(week_start) as wk from creator_week where is_complete_week)
select user_login, main_category, language, avg_viewers, wow_avg_viewers_growth, hours_live, streak_weeks
from creator_week, w
where week_start = w.wk
  and wow_avg_viewers_growth is not null
  and avg_viewers >= ${minViewers}
order by case when ${direction} = 'Fastest growing' then -wow_avg_viewers_growth else wow_avg_viewers_growth end
limit 25
```

```js
display(Inputs.table(movers, {
  layout: "auto",
  columns: ["user_login", "main_category", "language", "avg_viewers", "wow_avg_viewers_growth", "hours_live", "streak_weeks"],
  header: {user_login: "Creator", main_category: "Main category", language: "Lang.", avg_viewers: "Avg viewers",
    wow_avg_viewers_growth: "Week-on-week", hours_live: "Hours live", streak_weeks: "Streak (weeks)"},
  format: {avg_viewers: fmt.int, wow_avg_viewers_growth: (d) => fmt.signedPct(d), hours_live: fmt.int},
  rows: 12
}));
```

<p class="caption">Latest complete week compared with the week before, for creators live in both. Growth in average concurrent viewers. Creators with small audiences swing a lot week to week; raise the minimum to focus on established channels.</p>

## Segments

```js
const segSkipped = skipped(meta, "segmentation");
if (segSkipped) display(segSkipped);
```

```js
const profiles = results.segment_profiles ?? [];
const segments = results.segments ?? [];
const kSel = results.segment_k_selection ?? [];
const segNames = profiles.map((d) => d.segment);
```

```js
if (profiles.length) display(html`<p class="caption">k-means on ${fmt.int(segments.length)} creators with at least two active weeks in the last four complete weeks. k = ${meta.analyses.segmentation.k} was chosen by silhouette score. Segment names come from rules on the cluster centres; read the profile before trusting a name.</p>`);
```

<div class="grid grid-cols-2">
<div class="card">
<h2>Creators per segment</h2>

```js
if (profiles.length) display(resize((width) => Plot.plot({
  width,
  height: 40 + profiles.length * 32,
  marginLeft: 150,
  marginRight: 48,
  x: {axis: null},
  y: {label: null, domain: profiles.map((d) => d.segment)},
  marks: [
    Plot.barX(profiles, {y: "segment", x: "creators", fill: "var(--series-1)", rx: 2, insetTop: 6, insetBottom: 6,
      tip: true, title: (d) => `${d.segment}\n${fmt.int(d.creators)} creators (${fmt.pct(d.share)})`}),
    Plot.text(profiles, {y: "segment", x: "creators", text: (d) => `${fmt.int(d.creators)} · ${fmt.pct(d.share, 0)}`, dx: 6, textAnchor: "start", fill: "var(--theme-foreground-muted)"}),
    Plot.ruleX([0], {stroke: "var(--baseline)"})
  ]
})));
```
</div>
<div class="card">
<h2>Choosing k</h2>
<h3>Silhouette score by number of clusters (higher is better separated)</h3>

```js
if (kSel.length) display(resize((width) => Plot.plot({
  width,
  height: 200,
  x: {label: "k", ticks: kSel.map((d) => d.k), tickFormat: "d"},
  y: {grid: true, label: "Silhouette"},
  marks: [
    Plot.lineY(kSel, {x: "k", y: "silhouette", stroke: "var(--series-1)", strokeWidth: 2}),
    Plot.dot(kSel, {x: "k", y: "silhouette", fill: (d) => (d.k === meta.analyses.segmentation.k ? "var(--series-1)" : "var(--theme-background)"),
      stroke: "var(--series-1)", strokeWidth: 2, r: 4, tip: true, title: (d) => `k = ${d.k}\nsilhouette ${fmt.num(d.silhouette)}\nGMM BIC ${fmt.int(d.gmm_bic)}`})
  ]
})));
```
</div>
</div>

```js
if (profiles.length) display(Inputs.table(profiles, {
  layout: "auto",
  columns: ["segment", "creators", "avg_viewers", "weekly_growth", "active_share", "hours_per_week", "peak_hour_share", "categories"],
  header: {segment: "Segment", creators: "Creators", avg_viewers: "Viewers", weekly_growth: "Growth / wk",
    active_share: "Weeks active", hours_per_week: "Hours / wk", peak_hour_share: "In peak hours", categories: "Categories"},
  format: {avg_viewers: fmt.int, weekly_growth: (d) => fmt.signedPct(Math.expm1(d)), active_share: (d) => fmt.pct(d, 0),
    hours_per_week: (d) => d.toFixed(1), peak_hour_share: (d) => fmt.pct(d, 0), categories: (d) => d.toFixed(1)},
  select: false
}));
```

<p class="caption">Viewers, growth and hours are medians within the segment; weekly growth is the slope of log viewers over the last four complete weeks.</p>

```js
const focus = profiles.length ? view(Inputs.select(segNames, {label: "Highlight segment", value: segNames[0]})) : null;
```

<div class="card">
<h2>Audience size vs trend</h2>
<h3>Each dot is a creator; the highlighted segment is coloured, the rest are grey</h3>

```js
if (segments.length) {
  display(key([[focus, "var(--series-1)"], ["Other segments", "var(--muted-mark)"]]));
  const ordered = [...segments].sort((a, b) => (a.segment === focus) - (b.segment === focus));
  display(resize((width) => Plot.plot({
    width,
    height: 380,
    x: {type: "log", label: "Average viewers (log scale)", ticks: 5, tickFormat: "~s"},
    y: {label: "Weekly growth in viewers", tickFormat: (d) => fmt.signedPct(Math.expm1(d), 0), grid: true},
    marks: [
      Plot.ruleY([0], {stroke: "var(--baseline)"}),
      Plot.dot(ordered, {
        x: (d) => Math.max(1, Math.expm1(d.log_avg_viewers)),
        y: "viewer_trend",
        r: 4,
        fill: (d) => (d.segment === focus ? "var(--series-1)" : "var(--muted-mark)"),
        stroke: "var(--theme-background)",
        strokeWidth: 1,
        tip: true,
        title: (d) => `${d.user_login}\n${d.segment}\n${fmt.int(Math.expm1(d.log_avg_viewers))} avg viewers\n${fmt.signedPct(Math.expm1(d.viewer_trend))} per week`
      })
    ]
  })));
}
```
</div>

## Look up a creator

```sql id=creatorList
select user_login, main_category, language, weeks_active, avg_viewers, peak_viewers, latest_wow_growth, current_streak
from creator_summary
order by avg_viewers desc
```

```js
const search = view(Inputs.search([...creatorList], {placeholder: "Search creator login…", columns: ["user_login"]}));
```

```js
const picked = view(Inputs.table(search, {
  layout: "auto",
  columns: ["user_login", "main_category", "language", "weeks_active", "avg_viewers", "peak_viewers", "latest_wow_growth", "current_streak"],
  header: {user_login: "Creator", main_category: "Main category", language: "Lang.", weeks_active: "Weeks active", avg_viewers: "Avg viewers",
    peak_viewers: "Peak viewers", latest_wow_growth: "Last week", current_streak: "Streak"},
  format: {avg_viewers: fmt.int, peak_viewers: fmt.int, latest_wow_growth: (d) => fmt.signedPct(d)},
  sort: "avg_viewers", reverse: true, rows: 8, multiple: false, required: false
}));
```

```js
const login = picked?.user_login ?? null;
```

```sql id=history
select week_start, avg_viewers, hours_live, is_complete_week
from creator_week
where user_login = ${login}
order by week_start
```

```js
if (!login) {
  display(html`<p class="caption">Select a row above to see that creator's weekly history.</p>`);
} else {
  const rows = [...history].map((d) => ({...d, week_start: toDate(d.week_start), avg_viewers: Number(d.avg_viewers), hours_live: Number(d.hours_live)}));
  const chart = (y, label, fmtY) => resize((width) => Plot.plot({
    width, height: 200, marginLeft: 48,
    x: {label: null, type: "utc"},
    y: {grid: true, label, tickFormat: "s"},
    marks: [
      Plot.lineY(rows, {x: "week_start", y, stroke: "var(--series-1)", strokeWidth: 2}),
      Plot.dot(rows, {x: "week_start", y, fill: "var(--series-1)", stroke: "var(--theme-background)", strokeWidth: 2, r: 4,
        tip: true, title: (d) => `Week of ${fmt.date(d.week_start)}\n${fmtY(d[y])} ${label.toLowerCase()}${d.is_complete_week ? "" : "\n(incomplete week)"}`}),
      Plot.ruleY([0], {stroke: "var(--baseline)"})
    ]
  }));
  display(html`<div class="grid grid-cols-2">
    <div class="card"><h2>${login}: average viewers per week</h2>${chart("avg_viewers", "Avg viewers", fmt.int)}</div>
    <div class="card"><h2>${login}: hours live per week</h2>${chart("hours_live", "Hours live", fmt.int)}</div>
  </div>`);
}
```
