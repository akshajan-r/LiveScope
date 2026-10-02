---
title: Europe
toc: false
sql:
  language_week: ./data/language_week.arrow
---

```js
import {fmt, sourceBanner, skipped, key, kmPlot, SLOTS, segmentColors, LANGUAGE_GROUPS, languageColor, toDate} from "./components/common.js";
const meta = FileAttachment("data/meta.json").json();
const results = FileAttachment("data/analyses.json").json();
```

# EU LIVE ecosystem

```js
display(sourceBanner(meta));
```

How do creators streaming in EU/EEA languages compare with English-language creators on audience, growth and retention?

<p class="caption">Twitch records the broadcast language, not the creator's country, so language stands in for market. German, French, Italian, Polish, Dutch, the Nordic and Central/Eastern European languages are grouped as <b>EU/EEA languages</b>. Spanish and Portuguese are kept separate because most of their audience is in Latin America and Brazil. English mixes the US, UK and international audiences.</p>

```sql id=byLanguage
with latest as (select max(week_start) as w from language_week),
recent as (
  select * from language_week, latest
  where week_start > latest.w - interval 28 day
),
total as (select sum(viewer_hours) as vh from recent)
select
  language, language_name, language_group,
  round(avg(active_creators)) as creators_per_week,
  sum(viewer_hours) as viewer_hours,
  sum(viewer_hours) / (select vh from total) as share_of_hours,
  sum(viewer_hours) / sum(creator_hours) as viewers_per_live_hour,
  median(median_wow_growth) as median_wow_growth,
  avg(drop_off_rate) as drop_off_rate
from recent
group by all
order by viewer_hours desc
```

```js
const langRows = [...byLanguage].map((d) => ({...d, viewer_hours: Number(d.viewer_hours), creators_per_week: Number(d.creators_per_week)}));
const focusLangs = langRows.filter((d) => ["English", "EU/EEA languages", "Spanish & Portuguese"].includes(d.language_group));
const english = langRows.find((d) => d.language === "en");
if (!langRows.length) display(html`<p class="skipped">Language comparisons appear once the first week is complete.</p>`);
```

```js
if (focusLangs.length) display(html`<div class="card"><h2>Viewers per live hour, last 4 complete weeks</h2>
  <h3>Hours watched divided by hours streamed: how much audience each hour of LIVE gets. The line marks English.</h3>
  ${key([["English", SLOTS[0]], ["EU/EEA languages", SLOTS[1]], ["Spanish & Portuguese", SLOTS[2]]])}
  ${resize((width) => Plot.plot({
    width,
    height: 40 + focusLangs.length * 26,
    marginLeft: 110,
    marginRight: 48,
    x: {grid: true, label: "Viewers per live hour", axis: "top"},
    y: {label: null, domain: focusLangs.slice().sort((a, b) => b.viewers_per_live_hour - a.viewers_per_live_hour).map((d) => d.language_name)},
    color: languageColor,
    marks: [
      Plot.barX(focusLangs, {y: "language_name", x: "viewers_per_live_hour", fill: "language_group", rx: 2, insetTop: 4, insetBottom: 4,
        tip: true, title: (d) => `${d.language_name} (${d.language})\n${fmt.int(d.viewers_per_live_hour)} viewers per live hour\n${fmt.int(d.creators_per_week)} creators a week\n${fmt.pct(d.share_of_hours, 1)} of hours watched`}),
      Plot.text(focusLangs, {y: "language_name", x: "viewers_per_live_hour", text: (d) => fmt.int(d.viewers_per_live_hour), dx: 6, textAnchor: "start", fill: "var(--theme-foreground-muted)"}),
      english ? Plot.ruleX([english.viewers_per_live_hour], {stroke: "var(--theme-foreground-muted)"}) : null,
      Plot.ruleX([0], {stroke: "var(--baseline)"})
    ]
  }))}</div>`);
```

```js
if (langRows.length) display(Inputs.table(langRows, {
  layout: "auto",
  columns: ["language_name", "language_group", "creators_per_week", "share_of_hours", "viewers_per_live_hour", "median_wow_growth", "drop_off_rate"],
  header: {language_name: "Language", language_group: "Group", creators_per_week: "Creators / week", share_of_hours: "Share of hours watched",
    viewers_per_live_hour: "Viewers per live hour", median_wow_growth: "Median week-on-week growth", drop_off_rate: "Weekly drop-off"},
  format: {creators_per_week: fmt.int, share_of_hours: (d) => fmt.pct(d, 1), viewers_per_live_hour: fmt.int,
    median_wow_growth: (d) => fmt.signedPct(d), drop_off_rate: (d) => (d == null ? "–" : fmt.pct(d, 0))},
  rows: 14, select: false
}));
```

## Weekly trend by language group

```sql id=groupWeeks
select week_start, language_group, sum(viewer_hours) as viewer_hours, sum(viewer_hours) / sum(creator_hours) as viewers_per_live_hour,
       sum(active_creators) as active_creators
from language_week group by all order by week_start
```

```js
const gw = [...groupWeeks].map((d) => ({...d, week_start: toDate(d.week_start), viewer_hours: Number(d.viewer_hours), active_creators: Number(d.active_creators)}));
const groupsPresent = LANGUAGE_GROUPS.filter((g) => gw.some((d) => d.language_group === g));
const trend = (y, label, tickFormat) => resize((width) => Plot.plot({
  width, height: 220, marginLeft: 52,
  x: {type: "utc", label: null, ticks: 5},
  y: {grid: true, label, tickFormat, zero: true},
  color: languageColor,
  marks: [
    Plot.lineY(gw, {x: "week_start", y, stroke: "language_group", strokeWidth: 2}),
    Plot.dot(gw, {x: "week_start", y, fill: "language_group", r: 4, stroke: "var(--theme-background)", strokeWidth: 2,
      tip: true, title: (d) => `${d.language_group}\nweek of ${fmt.date(d.week_start)}\n${label}: ${fmt.int(d[y])}`}),
    Plot.ruleY([0], {stroke: "var(--baseline)"})
  ]
}));
if (!gw.length) display(html`<p class="skipped">Weekly trends appear once the first week is complete.</p>`);
if (gw.length) display(html`${key(groupsPresent.map((g) => [g, SLOTS[LANGUAGE_GROUPS.indexOf(g)]]))}
<div class="grid grid-cols-2">
  <div class="card"><h2>Weekly active creators</h2>${trend("active_creators", "Creators", "s")}</div>
  <div class="card"><h2>Hours watched per week</h2>${trend("viewer_hours", "Hours watched", "s")}</div>
</div>`);
```

## Do EU newcomers keep streaming?

```js
const curves = results.survival_curves ?? [];
const tests = results.survival_tests ?? [];
const euGroups = ["Newcomers: English", "Newcomers: EU/EEA languages"].filter((g) => curves.some((d) => d.group === g));
const euTest = tests.find((d) => d.comparison.includes("EU/EEA languages vs English"));
if (euGroups.length === 2) {
  display(html`<div class="card"><h2>Kaplan–Meier survival of newcomers: EU/EEA languages vs English</h2>
    <h3>Share still streaming by weeks since entering the top list${euTest ? `. Log-rank test p = ${fmt.num(euTest.p_value, 3)}` : ""}</h3>
    ${key([["English", SLOTS[0]], ["EU/EEA languages", SLOTS[1]]])}
    ${resize((width) => kmPlot(curves, euGroups, [SLOTS[0], SLOTS[1]], {width}))}</div>`);
  display(html`<p class="caption">The log-rank test asks whether the two curves differ by more than chance. A large p-value means the data cannot tell the groups apart yet, not that they are the same. See the <a href="./retention">retention page</a> for definitions.</p>`);
} else {
  display(html`<p class="skipped">Needs at least 20 newcomers in each group with a complete week of follow-up.</p>`);
}
```

## Segment mix

```js
const mix = results.segment_language_mix ?? [];
const segSkip = skipped(meta, "segmentation");
if (segSkip) display(segSkip);
const segNames = [...new Set(mix.map((d) => d.segment))];
const segCol = segmentColors(segNames);
const mixGroups = LANGUAGE_GROUPS.filter((g) => mix.some((d) => d.language_group === g));
if (mix.length) display(html`<div class="card"><h2>Creator segments within each language group</h2>
  <h3>Share of each group's creators in each segment (segments from the <a href="./creators">creators page</a>)</h3>
  ${key(segCol.domain.map((s, i) => [s, segCol.range[i]]))}
  ${resize((width) => Plot.plot({
    width,
    height: 40 + mixGroups.length * 44,
    marginLeft: 150,
    x: {label: "Share of creators", tickFormat: "%", axis: "top", domain: [0, 1]},
    y: {label: null, domain: mixGroups},
    color: segCol,
    marks: [
      Plot.barX(mix, Plot.stackX({y: "language_group", x: "share", fill: "segment", order: segCol.domain, insetTop: 8, insetBottom: 8,
        insetLeft: 1, insetRight: 1, tip: true, title: (d) => `${d.language_group}\n${d.segment}: ${fmt.pct(d.share, 0)} (${fmt.int(d.creators)} creators)`}))
    ]
  }))}</div>`);
```

<p class="caption">For category-level opportunities within EU languages, switch the <a href="./categories">categories page</a> to "EU/EEA languages".</p>
