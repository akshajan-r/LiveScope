---
title: This week
toc: false
---

```js
import {fmt, sourceBanner, key, SLOTS, LANGUAGE_GROUPS} from "./components/common.js";
const meta = FileAttachment("data/meta.json").json();
const results = FileAttachment("data/analyses.json").json();
```

```js
const r = results.weekly_report ?? {status: "not built"};
const m = (x) => (x == null ? "–" : `${(x / 1e6).toFixed(1)}M`);
const vsLast = (t, l) => (!l || l < 0.05 * t ? "new" : fmt.signedPct(t / l - 1, 0));
```

# This week so far

```js
display(sourceBanner(meta));
```

```js
if (r.status !== "ok") display(html`<p class="skipped">Not available yet: ${r.status}.</p>`);
else display(html`<p class="caption">${r.this_start} to ${r.through} UTC, compared with the same hours last week (${r.last_start} to ${r.last_through}); ${r.hours_this} and ${r.hours_last} hourly snapshots captured. Weekly KPIs on the overview only count complete weeks; this page covers the week in progress. It uses top-list streams only (the top ${fmt.int(meta.max_streams_per_snapshot)} each hour), a fixed-size group, so growth in the tracking panel cannot inflate the comparison. Rebuilt every hour.</p>`);
```

```js
if (r.status === "ok") {
  const h = r.headline;
  display(html`<div class="grid grid-cols-3">
    <div class="card"><h2>Hours watched so far</h2><span class="big">${m(h.viewer_hours)}</span>
      <p class="caption">${fmt.signedPct(h.viewer_hours_change)} vs ${m(h.viewer_hours_last)} at this point last week</p></div>
    <div class="card"><h2>Average concurrent viewers (top list)</h2><span class="big">${fmt.compact(h.avg_concurrent)}</span>
      <p class="caption">${fmt.signedPct(h.avg_concurrent_change)} vs ${fmt.compact(h.avg_concurrent_last)}</p></div>
    <div class="card"><h2>EU/EEA share of hours watched</h2><span class="big">${fmt.pct(r.language_groups.find((d) => d.language_group === "EU/EEA languages")?.share_this, 1)}</span>
      <p class="caption">${fmt.pct(r.language_groups.find((d) => d.language_group === "EU/EEA languages")?.share_last, 1)} at this point last week</p></div>
  </div>`);
}
```

## Share of hours watched by language group

```js
if (r.status === "ok") {
  const rows = LANGUAGE_GROUPS.map((g) => r.language_groups.find((d) => d.language_group === g)).filter(Boolean);
  display(key([["This week", "var(--series-1)"], ["Same point last week", "var(--muted-mark)"]]));
  display(resize((width) => Plot.plot({
    width, height: 40 + rows.length * 40, marginLeft: 150, marginRight: 60,
    x: {label: "Share of top-list hours watched", tickFormat: "%", axis: "top", grid: true, domain: [0, Math.max(...rows.map((d) => Math.max(d.share_this, d.share_last))) * 1.1]},
    y: {label: null, domain: rows.map((d) => d.language_group)},
    marks: [
      Plot.link(rows, {y: "language_group", x1: "share_last", x2: "share_this", stroke: "var(--baseline)", strokeWidth: 2}),
      Plot.dot(rows, {y: "language_group", x: "share_last", r: 5, fill: "var(--muted-mark)", stroke: "var(--theme-background)", strokeWidth: 2}),
      Plot.dot(rows, {y: "language_group", x: "share_this", r: 6, fill: "var(--series-1)", stroke: "var(--theme-background)", strokeWidth: 2,
        tip: true, title: (d) => `${d.language_group}\n${fmt.pct(d.share_this, 1)} this week (${fmt.pct(d.share_last, 1)} last week)\nhours watched ${fmt.signedPct(d.change)}`}),
      Plot.text(rows, {y: "language_group", x: (d) => Math.max(d.share_this, d.share_last), text: (d) => fmt.signedPct(d.change, 0), dx: 12, textAnchor: "start", fill: "var(--theme-foreground-muted)"})
    ]
  })));
  display(html`<p class="caption">EU/EEA languages: ${r.eu_languages.slice(0, 6).map((d) => `${d.language_name} ${m(d.this_vh)} (${vsLast(d.this_vh, d.last_vh)})`).join(" · ")}.
    Biggest EU increases: ${r.eu_drivers.slice(0, 3).map((d) => `${d.language_name} ${d.game_name} ${m(d.last_vh)} → ${m(d.this_vh)}`).join(" · ")}.</p>`);
}
```

## Categories moving the most

```js
if (r.status === "ok") {
  const rows = [...r.categories_up.slice(0, 8), ...r.categories_down].map((d) => ({...d, up: d.delta >= 0}));
  display(key([["Gained hours watched", "var(--series-1)"], ["Lost hours watched", "var(--critical)"]]));
  display(resize((width) => Plot.plot({
    width, height: 40 + rows.length * 26, marginLeft: 190, marginRight: 70,
    x: {label: "Change in hours watched vs same point last week", tickFormat: "s", axis: "top", grid: true},
    y: {label: null, domain: rows.map((d) => d.game_name)},
    marks: [
      Plot.barX(rows, {y: "game_name", x: "delta", fill: (d) => (d.up ? "var(--series-1)" : "var(--critical)"), rx: 2, insetTop: 4, insetBottom: 4,
        tip: true, title: (d) => `${d.game_name}\n${m(d.this_vh)} this week vs ${m(d.last_vh)}\n${d.creators_this} creators (${d.creators_last} last week)`}),
      Plot.text(rows.filter((d) => d.up), {y: "game_name", x: "delta", text: (d) => vsLast(d.this_vh, d.last_vh), dx: 6, textAnchor: "start", fill: "var(--theme-foreground-muted)"}),
      // Falling bars run toward the axis labels, so their labels sit right of zero.
      Plot.text(rows.filter((d) => !d.up), {y: "game_name", x: 0, text: (d) => vsLast(d.this_vh, d.last_vh), dx: 6, textAnchor: "start", fill: "var(--theme-foreground-muted)"}),
      Plot.ruleX([0], {stroke: "var(--baseline)"})
    ]
  })));
}
```

## Creators gaining the most

```js
if (r.status === "ok") display(Inputs.table(r.creators_up, {
  layout: "auto",
  columns: ["user_login", "language_name", "main_category", "this_vh", "last_vh"],
  header: {user_login: "Creator", language_name: "Language", main_category: "Main category this week", this_vh: "Hours watched this week", last_vh: "Same point last week"},
  format: {this_vh: fmt.int, last_vh: fmt.int},
  select: false
}));
```

## Are last week's creators back?

```js
if (r.status === "ok" && r.returns) {
  const t = r.returns_test;
  if (t) display(html`<p>Of <b>newcomers</b> who were live last week, <b>${fmt.pct(t.english, 1)}</b> of English-language creators (n = ${fmt.int(t.n_english)}) and <b>${fmt.pct(t.eu, 1)}</b> of EU/EEA-language creators (n = ${fmt.int(t.n_eu)}) have streamed again this week so far. EU minus English: ${(t.diff * 100).toFixed(1)} pp (95% CI ${(t.ci_low * 100).toFixed(1)} to ${(t.ci_high * 100).toFixed(1)} pp, two-proportion z-test p = ${t.p_value.toPrecision(2)}).</p>`);
  display(Inputs.table(r.returns, {
    layout: "auto",
    columns: ["cohort", "language_group", "live_last_week", "live_again", "return_rate"],
    header: {cohort: "Cohort", language_group: "Language group", live_last_week: "Live last week", live_again: "Live again this week", return_rate: "Return rate so far"},
    format: {live_last_week: fmt.int, live_again: fmt.int, return_rate: (d) => fmt.pct(d, 1)},
    select: false
  }));
  display(html`<p class="caption">Panel creators only. Newcomers first entered the top list after collection began; the founding cohort was already established. Rates rise as the week goes on, so compare groups with each other, not with full-week figures.</p>`);
}
```
