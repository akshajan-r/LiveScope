---
title: Findings
toc: false
---

```js
import {fmt, sourceBanner} from "./components/common.js";
const meta = FileAttachment("data/meta.json").json();
const results = FileAttachment("data/analyses.json").json();
```

# Findings

```js
display(sourceBanner(meta));
```

What the data shows as of the latest build (${fmt.date(meta.last_snapshot)}, ${fmt.int(meta.complete_weeks)} complete weeks). These sentences are generated from the numbers on the other pages and update with every build. They state measurements only; the recommendations for a creator-success team are in the [README](https://github.com/akshajan-r/LiveScope#findings), written once there is enough data to support them.

```js
const facts = results.findings ?? [];
display(html`<ul class="facts">${facts.map((f) => html`<li>
  <span class="topic">${f.topic}${f.status === "pending" ? html`<span class="tag">pending</span>` : ""}</span>
  <span class=${f.status === "pending" ? "pending" : ""}>${f.text}</span>
  ${f.status === "measured" ? html` <a href=${`.${f.page}`}>See chart →</a>` : ""}
</li>`)}</ul>`);
```
