# Metric design

The business question: **which creators are growing, which are at risk of dropping off, and what helps them grow?** This page defines the metrics used to answer it. A metric only belongs here if it can be computed from the data this project collects (see [data.md](data.md) for what that data can and cannot see).

Targets in the OKR tree are left as `[baseline + x]` until a baseline has been measured. Numbers are filled in from the dashboard, never estimated.

## North-star metric

**Weekly LIVE hours watched on tracked creators** (`sum(viewer_hours)` per complete week, from `creator_week`).

Why this one:

- It moves only when both sides of the marketplace move: creators have to go live (supply) and viewers have to watch (demand). Hours streamed alone rewards streaming to empty rooms; viewers alone rewards a few mega-streams.
- It is additive, so it can be broken down by creator, segment, category or language without changing definitions.
- It responds within a week, so it can be tracked against interventions.

What it misses: it does not say whether growth is broad or concentrated in a few channels. The concentration guardrail below covers that.

## OKR tree: "Grow creator adoption of LIVE"

```
Objective: Grow creator adoption of LIVE
│
├── KR1  Weekly active LIVE creators: [baseline] → [baseline + x%]
│        ├── New creators entering the panel per week
│        ├── Second-week return rate (activation)
│        └── Reactivated creators (live again after 2+ weeks off)
│
├── KR2  4-week creator retention: [baseline] → [baseline + x pp]
│        ├── Weekly drop-off rate (active in t, not in t+1)
│        ├── Median streak length
│        └── Share of creators in the "At risk" segment
│
└── KR3  Median weekly hours watched per active creator: [baseline] → [baseline + x%]
         ├── Hours live per creator per week
         ├── Average concurrent viewers per live hour
         └── Peak-hour share of live hours
```

Guardrails (should not get worse while the KRs move):

- **Audience concentration**: share of weekly hours watched going to the top 1% of creators.
- **Viewers per live hour across the platform**: growth in creators should not come from splitting the same audience across more streams.
- **Data coverage**: share of hourly snapshots captured in the week (a metric that "moves" because collection broke is not a result).

## Definitions

The platform-level weekly values (north star, KRs, guardrails) are in the `platform_week` table and on the dashboard's overview page. All weekly metrics use ISO weeks starting Monday 00:00 UTC and only **complete weeks**: the week has ended and at least 90% of its 168 hourly snapshots succeeded (`collector_weeks.is_complete`).

| Metric | Definition | Grain | Source |
|---|---|---|---|
| Hours live | Number of hourly snapshots in which the creator had a live stream. An hourly sample, not exact minutes. | creator-week | `creator_week.hours_live` |
| Live share | Hours live ÷ hours captured that week. Corrects for collection gaps. | creator-week | `creator_week.live_share` |
| Average viewers | Mean concurrent viewer count across the creator's live snapshots. | creator-week | `creator_week.avg_viewers` |
| Peak viewers | Highest concurrent viewer count in the week. | creator-week | `creator_week.peak_viewers` |
| Hours watched (viewer-hours) | Sum of concurrent viewers across live snapshots; each snapshot stands for one hour. | creator-week | `creator_week.viewer_hours` |
| Week-on-week growth | `x(t) / x(t−1) − 1`, only when the creator was live in both calendar weeks; otherwise null. Computed for average viewers, hours live and hours watched. | creator-week | `creator_week.wow_*_growth` |
| Streak | Consecutive calendar weeks live, ending this week (gaps-and-islands). | creator-week | `creator_week.streak_weeks` |
| Peak hours | The 6 UTC hours of the day with the highest average total concurrent viewers in the data. | platform | `peak_hours` |
| Peak-hour share | Share of the creator's live hours that fall in peak hours. | creator-week | `creator_week.peak_hour_share` |
| Weekly active LIVE creator | A tracked creator with hours live ≥ 1 in the week. | week | count of `creator_week` rows |
| New creators | Creators whose first observed week is t. In the first week of collection everyone is "new", so ignore that week. | week | `platform_week.new_creators` |
| Activation (second-week return) | Of creators whose first observed week is t, the share also live in t+1. | week | `platform_week.activation_rate` |
| Drop-off | Live in week t, not live in t+1. Reliable for panel creators, who are looked up whether or not they rank; a non-panel creator who drops out of the top list looks like a drop-off. | creator-week / week | `predict.build_dataset(...).churn`, `platform_week.drop_off_rate` |
| 4-week retention | Of creators live in week t, share live in week t+4. | week | `platform_week.retention_4w` |
| Growth (model target) | Hours watched in t+1 ≥ 1.1 × hours watched in t. Going dark counts as not growing. | creator-week | `predict.build_dataset(...).growth` |
| Audience concentration | Share of weekly hours watched going to the top 1% of creators by hours watched. | week | `platform_week.top1pct_share` |
| Viewers per live hour | Hours watched ÷ creator hours live, across all tracked creators. | week | `platform_week.viewers_per_live_hour` |

## Retention and survival

Computed for **panel creators** only (see [data.md](data.md)): they are looked up every hour whatever their rank, so a week without them in the data really is a week without going live.

| Term | Definition | Source |
|---|---|---|
| Cohort | The week a creator first entered the top list (joined the panel). | `panel_creators.cohort_week` |
| Founding cohort | Creators who joined in the first collection week. Most were already established, so they are reported separately from newcomers. | `panel_creators.founding_cohort` |
| Cohort retention, week k | Share of a cohort live in the k-th week after its cohort week. Counts week-by-week activity, so a skipped week dips and recovers. | `cohort_retention` |
| Churn | No live week in the two most recent complete weeks. Creators who come back after a longer gap are counted by their last live week. | `creator_lifetime.churned` |
| Lifetime | Weeks from cohort week to last live week (churned), or weeks followed so far (censored). | `creator_lifetime.duration_weeks` |
| Survival S(t) | Kaplan–Meier estimate of the share still streaming more than t weeks after their cohort week, with Greenwood/log-log 95% CIs. Reported at 1, 2, 4 and 8 weeks. | `livescope/survival.py` |
| Survival difference | Log-rank test between groups (EU/EEA vs English newcomers; all language groups). | `livescope/survival.py` |

## Language groups

Twitch's broadcast language stands in for market. **EU/EEA languages** are German, French, Italian, Polish, Dutch, Swedish, Danish, Finnish, Norwegian, Czech, Slovak, Hungarian, Romanian, Bulgarian, Greek, Croatian, Slovenian, Estonian, Latvian, Lithuanian and Catalan. **Spanish & Portuguese** are a separate group because most of those audiences are in Latin America and Brazil. A creator's language is the most frequent language across their streams (`creator_language`).

## Category opportunity

Over the last 28 days, for all creators and for each language group (`category_opportunity`):

| Metric | Definition |
|---|---|
| Median creator viewers | Median, across the category's creators, of each creator's average concurrent viewers while streaming that category. |
| Opportunity index | Median creator viewers ÷ the median across all creator-category pairs in the same scope. 2.0 = the typical creator in this category draws twice the typical audience. |
| Top creator share | Share of the category's hours watched that come from its biggest creator. ≥ 50% means the "demand" is mostly one creator's fanbase. |
| Viewer-hours growth | Hours watched in the last 14 days ÷ the previous 14 days − 1 (null until 28 days are collected). |

Candidates are categories with an index above 1, at least 5 creators and a top creator share below 50%. Rankings wait for 7 days of data. They are hypotheses to test, not conclusions.

## Segment definitions

Segments come from k-means on six creator features over the last four complete weeks (log average viewers, viewer trend, share of weeks active, hours live per week, peak-hour share, categories per week), k chosen by silhouette score. Names are assigned by rules on the standardised cluster centres, in this order:

| Name | Rule on the cluster centre (z-scores) |
|---|---|
| At risk | lowest `viewer_trend + active_share`, and that sum < −0.5 |
| Rising stars | highest `viewer_trend` of the rest, if > 0.5 |
| Established | highest `log_avg_viewers` of the rest, if > 0.5 |
| Prime-time streamers | `peak_hour_share` > 1.0 |
| High-volume streamers | `mean_hours_live` > 0.5 |
| Steady niche | `active_share` ≥ 0 |
| Occasional | everything else |

Clusters are re-fit on every build, so a creator's segment can change week to week. Check the profile table before reading a name.
