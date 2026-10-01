-- One row per creator: lifetime totals plus their latest complete week.
create or replace table creator_summary as
with life as (
    select
        user_id,
        any_value(user_login order by week_start desc) as user_login,
        min(week_start)       as first_week,
        max(week_start)       as last_week,
        count(*)              as weeks_active,
        sum(hours_live)       as hours_live,
        sum(viewer_hours)     as viewer_hours,
        sum(viewer_hours) / sum(hours_live) as avg_viewers,
        max(peak_viewers)     as peak_viewers,
        max(streak_weeks)     as longest_streak,
        mode(main_category)   as main_category,
        mode(language)        as language
    from creator_week
    group by user_id
),
latest as (
    select *
    from creator_week
    where is_complete_week
    qualify row_number() over (partition by user_id order by week_start desc) = 1
)
select
    life.*,
    latest.week_start               as latest_complete_week,
    latest.avg_viewers              as latest_avg_viewers,
    latest.hours_live               as latest_hours_live,
    latest.wow_avg_viewers_growth   as latest_wow_growth,
    latest.streak_weeks             as current_streak
from life
left join latest using (user_id);
