-- Weekly KPI table for the north-star metric, the OKR key results and the
-- guardrails defined in docs/metrics.md. Only complete weeks.
create or replace table platform_week as
with cw as (
    select * from creator_week where is_complete_week
),
weeks as (
    select week_start, hours_observed from collector_weeks where is_complete
),
firsts as (
    select user_id, min(week_start) as first_week from creator_week group by user_id
),
ranked as (
    select
        week_start,
        viewer_hours,
        row_number() over (partition by week_start order by viewer_hours desc) as rnk,
        count(*) over (partition by week_start) as n
    from cw
),
concentration as (
    select week_start,
           sum(viewer_hours) filter (where rnk <= greatest(1, ceil(n * 0.01))) / sum(viewer_hours) as top1pct_share
    from ranked group by week_start
),
base as (
    select
        week_start,
        count(*)                          as active_creators,
        sum(viewer_hours)                 as viewer_hours,
        median(viewer_hours)              as median_viewer_hours_per_creator,
        sum(hours_live)                   as creator_hours,
        sum(viewer_hours) / sum(hours_live) as viewers_per_live_hour,
        median(streak_weeks)              as median_streak
    from cw group by week_start
),
transitions as (
    -- For creators live in week t: are they live in t+1, and in t+4?
    select
        cw.week_start,
        avg(case when n1.user_id is null then 1.0 else 0.0 end) as drop_off_rate,
        avg(case when n4.user_id is null then 0.0 else 1.0 end) as retention_4w,
        count(*) filter (where f.first_week = cw.week_start)   as new_creators,
        avg(case when n1.user_id is null then 0.0 else 1.0 end)
            filter (where f.first_week = cw.week_start)        as activation_rate
    from cw
    join firsts f using (user_id)
    left join creator_week n1 on n1.user_id = cw.user_id and n1.week_start = cw.week_start + interval 7 day
    left join creator_week n4 on n4.user_id = cw.user_id and n4.week_start = cw.week_start + interval 28 day
    group by cw.week_start
)
select
    b.week_start,
    w.hours_observed,
    b.active_creators,
    b.viewer_hours,
    case when lag(b.week_start) over (order by b.week_start) = b.week_start - interval 7 day
         then b.viewer_hours / lag(b.viewer_hours) over (order by b.week_start) - 1 end as viewer_hours_wow,
    b.median_viewer_hours_per_creator,
    b.creator_hours,
    b.viewers_per_live_hour,
    b.median_streak,
    t.new_creators,
    -- Rates that need a following week are null until that week is complete.
    case when exists (select 1 from weeks w1 where w1.week_start = b.week_start + interval 7 day)
         then t.drop_off_rate end   as drop_off_rate,
    case when exists (select 1 from weeks w1 where w1.week_start = b.week_start + interval 7 day)
         then t.activation_rate end as activation_rate,
    case when exists (select 1 from weeks w4 where w4.week_start = b.week_start + interval 28 day)
         then t.retention_4w end    as retention_4w,
    c.top1pct_share
from base b
join weeks w using (week_start)
join transitions t using (week_start)
join concentration c using (week_start)
order by b.week_start;
