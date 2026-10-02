-- Retention and survival inputs, for panel creators only: they are looked up
-- every hour whatever their rank, so "not seen" really means "not live".
-- A creator's cohort is the week they first entered the top list (joined the
-- panel). Creators who joined in the first collection week were mostly
-- established already, so that cohort is flagged and kept apart.
create or replace table panel_creators as
with first_week as (
    select date_trunc('week', min(snapshot_hour))::date as w from collector_hours
)
select
    p.user_id,
    date_trunc('week', p.first_seen_at)::date                    as cohort_week,
    date_trunc('week', p.first_seen_at)::date = first_week.w     as founding_cohort,
    coalesce(cl.language_group, 'Other')                          as language_group,
    cl.language
from panel p
cross join first_week
left join creator_language cl using (user_id);

-- Share of each cohort live k weeks after its cohort week. Week 0 is the
-- cohort week itself; later weeks count only once they are complete.
create or replace table cohort_retention as
with cohorts as (
    select cohort_week, founding_cohort, count(*) as cohort_size
    from panel_creators group by all
),
grid as (
    select c.cohort_week, c.founding_cohort, c.cohort_size, w.week_start,
           datediff('week', c.cohort_week, w.week_start) as weeks_since
    from cohorts c
    join collector_weeks w
      on w.week_start >= c.cohort_week
     and (w.is_complete or w.week_start = c.cohort_week)
),
active as (
    select pc.cohort_week, cw.week_start, count(*) as active
    from panel_creators pc
    join creator_week cw using (user_id)
    group by all
)
select
    g.cohort_week,
    g.founding_cohort,
    g.weeks_since,
    g.cohort_size,
    coalesce(a.active, 0)                  as active,
    coalesce(a.active, 0) / g.cohort_size  as retention
from grid g
left join active a using (cohort_week, week_start)
where g.weeks_since <= 12
order by g.cohort_week, g.weeks_since;

-- One row per panel creator for Kaplan-Meier: weeks from cohort week to last
-- live week, and whether they have churned (no live week for the 2 most
-- recent complete weeks). Everyone else is censored at the weeks observed.
create or replace table creator_lifetime as
with last_complete as (
    select max(week_start) as w from collector_weeks where is_complete
),
last_live as (
    select user_id, max(week_start) as last_active_week from creator_week group by user_id
)
select
    pc.user_id,
    pc.cohort_week,
    pc.founding_cohort,
    pc.language_group,
    pc.language,
    ll.last_active_week,
    datediff('week', pc.cohort_week, lc.w) + 1                         as weeks_observed,
    datediff('week', ll.last_active_week, lc.w) >= 2                   as churned,
    case when datediff('week', ll.last_active_week, lc.w) >= 2
         then datediff('week', pc.cohort_week, ll.last_active_week) + 1
         else datediff('week', pc.cohort_week, lc.w) + 1 end           as duration_weeks
from panel_creators pc
join last_live ll using (user_id)
cross join last_complete lc
where lc.w is not null and lc.w >= pc.cohort_week;
