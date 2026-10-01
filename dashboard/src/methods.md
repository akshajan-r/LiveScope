---
title: Data & methods
toc: true
---

```js
import {fmt, sourceBanner} from "./components/common.js";
const meta = FileAttachment("data/meta.json").json();
```

# Data & methods

```js
display(sourceBanner(meta));
```

## Collection

A GitHub Actions job calls the Twitch Helix [Get Streams](https://dev.twitch.tv/docs/api/reference/#get-streams) endpoint every hour. Each run stores the top ${fmt.int(meta.max_streams_per_snapshot)} live streams by concurrent viewers, plus every live stream from a panel of up to ${fmt.int(meta.panel_max)} creators (the first creators ever seen in a top list). Tracking the panel outside the top list is what makes declines and drop-off visible. Snapshots pass data-quality checks (schema, null IDs, duplicate streams, negative counts, minimum row count) before they are written as Parquet.

## Known biases

- **Selection.** Creators enter the data by appearing in the top list, so small creators are under-represented and "creators" here means the most-watched part of Twitch.
- **Hourly sampling.** Hours live and hours watched are counted from hourly snapshots: a 30-minute stream may be missed, and a stream that spans three snapshots counts as three hours.
- **Viewer counts** are Twitch's concurrent viewer numbers, which include embeds and are not unique viewers.
- **Gaps.** Scheduled GitHub Actions can be delayed or skipped. Weeks with under 90% of hours captured are excluded from weekly comparisons.

## Metric definitions

See [`docs/metrics.md`](https://github.com/akshajan-r/LiveScope/blob/main/docs/metrics.md) for the north-star metric, the OKR tree and the definition of every metric used here.

## Models

SQL models (DuckDB) turn snapshots into a creator-hour table, then a creator-week table with hours live, average and peak viewers, hours watched, week-on-week growth and streak length (gaps-and-islands). Segmentation is k-means on standardised creator features with k chosen by silhouette score (a Gaussian mixture with BIC is fit as a check). The growth model compares a base-rate baseline, a momentum rule, logistic regression and LightGBM on a time-based split.
