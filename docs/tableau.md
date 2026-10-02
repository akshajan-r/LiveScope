# Tableau Public / Power BI

Every publish writes the analysis tables as CSV to the dashboard site, so the latest extracts are always at:

```
https://<user>.github.io/LiveScope/downloads/<table>.csv
```

(They are also attached to each publish run as the `tableau-extracts` artifact.)

| File | Grain | Use it for |
|---|---|---|
| `platform_week.csv` | week | north star, KRs and guardrails over time |
| `creator_week.csv` | creator × week | growth, streaks, hours, peak-hour share |
| `creator_summary.csv` | creator | leaderboards, lifetime totals |
| `segments.csv` | creator | segment assignment and features (join to `creator_summary` on `user_id`) |
| `segment_profiles.csv` | segment | segment sizes and medians |
| `category_week.csv` | category × week | category trends |
| `platform_hour.csv` | hour | daily and weekly cycles |
| `cohort_retention.csv` | cohort × weeks since | cohort retention heat map |
| `creator_lifetime.csv` | creator | survival inputs (duration, churned, language group) |
| `survival_curves.csv`, `survival_milestones.csv` | group × week | Kaplan–Meier curves and 1/2/4/8-week survival |
| `language_week.csv` | language × week | EU vs English comparisons |
| `category_opportunity.csv` | category × scope | opportunity scatter and table |
| `peak_hours.csv` | hour of day | peak-hour definition |
| `model_metrics_growth.csv`, `feature_importance_growth.csv` | model / feature | model comparison |
| `did_summary.csv`, `did_event_study.csv` | estimate / week | natural experiment |

## Suggested workbook (three dashboards)

1. **Platform health**: north-star line (`platform_week.viewer_hours`), KPI tiles for active creators, drop-off and top-1% share; a calendar heat map of `platform_hour.total_viewers` by weekday × hour.
2. **Creators**: relationship `creator_summary` ↔ `segments` on `user_id`. Scatter of average viewers (log axis) vs `viewer_trend` coloured by segment, a segment filter, and a leaderboard of `latest_wow_growth` with a minimum-viewers parameter.
3. **What helps creators grow**: feature importance bar chart, the event-study chart from `did_event_study` (estimate with `ci_low`/`ci_high` as error bars), and a text box with the recommendation.

Tableau Public cannot schedule refreshes from a web CSV, so refresh by downloading the latest files and republishing. Link the published workbook from the README.

## Power BI Desktop

**Get data → Web**, paste the CSV URL for each table, then **Model view**: relate `segments[user_id]` and `creator_week[user_id]` to `creator_summary[user_id]` (one-to-many). Power BI Desktop can refresh from the web URLs; publishing to the Power BI service needs a work account, so screenshots in the README are the usual way to show it.
