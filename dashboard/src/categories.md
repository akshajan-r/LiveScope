---
title: Categories
toc: false
sql:
  category_opportunity: ./data/category_opportunity.arrow
---

```js
import {fmt, sourceBanner, key, SLOTS} from "./components/common.js";
const meta = FileAttachment("data/meta.json").json();
```

# Category opportunity

```js
display(sourceBanner(meta));
```

Where is there audience demand that too few creators are serving? For each category over the last 28 days, compare the typical creator's audience with how many creators stream it. A category where the **median** creator draws well above the platform median, with few creators, is a candidate for creator recruitment or for nudging existing creators into it.

```js
const days = meta.snapshot_hours / 24;
if (days < 7) display(html`<div class="banner">Only ${days.toFixed(1)} days of data so far. Category rankings from less than a week reflect whoever happened to be live, not lasting demand; treat them as a preview until at least 7 days are collected.</div>`);
```

```js
const scope = view(Inputs.select(["All", "EU/EEA languages", "English", "Spanish & Portuguese", "Other"], {label: "Creators streaming in", value: "All"}));
const minCreators = view(Inputs.range([1, 50], {value: 5, step: 1, label: "Min. creators"}));
```

```sql id=cats
select * from category_opportunity
where scope = ${scope} and creators >= ${minCreators}
order by opportunity_index desc
```

```js
const rows = [...cats].map((d) => ({...d, creators: Number(d.creators), creator_hours: Number(d.creator_hours), viewer_hours: Number(d.viewer_hours)}))
  .map((d) => ({...d, concentrated: d.top_creator_share >= 0.5}));
const candidates = rows.filter((d) => !d.concentrated && d.opportunity_index > 1).slice(0, 5);
const candidateNames = new Set(candidates.map((d) => d.game_name));
if (!rows.length) display(html`<p class="skipped">No categories with at least ${minCreators} creators in this scope yet.</p>`);
```

```js
if (rows.length) display(html`<div class="card"><h2>Audience per creator vs number of creators</h2>
  <h3>Each dot is a category. Up and to the left: strong audience per creator, few creators. The line is the median creator in this scope (index 1.0).</h3>
  ${key([["Top 5 candidates", SLOTS[0]], ["Other categories", "var(--muted-mark)"], ["One creator holds half the audience", "var(--theme-foreground-muted)", "hollow"]])}
  ${resize((width) => Plot.plot({
    width,
    height: 420,
    marginLeft: 52,
    marginRight: 20,
    x: {type: "log", label: "Creators streaming the category (log scale)", tickFormat: "~s"},
    y: {type: "log", label: "Median creator's average viewers (log scale)", grid: true, tickFormat: "~s"},
    marks: [
      Plot.ruleY([rows[0].median_creator_viewers / rows[0].opportunity_index], {stroke: "var(--theme-foreground-muted)"}),
      Plot.dot(rows.filter((d) => !candidateNames.has(d.game_name)), {
        x: "creators", y: (d) => Math.max(d.median_creator_viewers, 0.5), r: 4,
        fill: (d) => (d.concentrated ? "none" : "var(--muted-mark)"), stroke: (d) => (d.concentrated ? "var(--theme-foreground-muted)" : "var(--theme-background)"),
        strokeWidth: (d) => (d.concentrated ? 1.5 : 1),
        tip: true, title: (d) => `${d.game_name}\n${fmt.int(d.creators)} creators\nmedian creator: ${fmt.int(d.median_creator_viewers)} avg viewers (${d.opportunity_index.toFixed(2)}× scope median)\ntop creator holds ${fmt.pct(d.top_creator_share, 0)} of hours watched`}),
      Plot.dot(candidates, {x: "creators", y: "median_creator_viewers", r: 6, fill: SLOTS[0], stroke: "var(--theme-background)", strokeWidth: 2,
        tip: true, title: (d) => `${d.game_name}\n${fmt.int(d.creators)} creators\nmedian creator: ${fmt.int(d.median_creator_viewers)} avg viewers (${d.opportunity_index.toFixed(2)}× scope median)\ntop creator holds ${fmt.pct(d.top_creator_share, 0)} of hours watched`}),
      Plot.text(candidates, {x: "creators", y: "median_creator_viewers", text: "game_name", dx: 9, textAnchor: "start", fill: "var(--theme-foreground)", fontWeight: 500})
    ]
  }))}</div>`);
```

```js
if (rows.length) display(Inputs.table(rows, {
  layout: "auto",
  columns: ["game_name", "opportunity_index", "median_creator_viewers", "creators", "viewers_per_live_hour", "top_creator_share", "viewer_hours_growth"],
  header: {game_name: "Category", opportunity_index: "Opportunity index", median_creator_viewers: "Median creator avg viewers", creators: "Creators",
    viewers_per_live_hour: "Viewers per live hour", top_creator_share: "Top creator's share", viewer_hours_growth: "Hours watched, last 14d vs prior 14d"},
  format: {opportunity_index: (d) => `${d.toFixed(2)}×`, median_creator_viewers: fmt.int, viewers_per_live_hour: fmt.int,
    top_creator_share: (d) => `${fmt.pct(d, 0)}${d >= 0.5 ? " ⚠" : ""}`, viewer_hours_growth: (d) => (d == null ? "needs 28 days" : fmt.signedPct(d))},
  rows: 15, select: false
}));
```

## How to read this

- **Opportunity index** = the category's median creator audience ÷ the median creator audience across all categories in this scope. 2.0× means the typical creator in that category draws twice the typical audience.
- **Medians, not averages**, so one star streamer cannot make a category look under-served. ⚠ marks categories where one creator holds half or more of the hours watched; their "demand" may be that creator's fanbase, not open demand.
- **Growth** compares the last 14 days with the 14 before. A high index with falling hours may be a fading event or release; a high index with rising hours is the stronger signal.
- **This is a hypothesis generator, not proof.** The data covers creators who reached the top list, so the median creator here is already successful. The way to confirm a category opportunity is a test: invite a group of creators into the category and compare their growth with a matched group that was not invited.
