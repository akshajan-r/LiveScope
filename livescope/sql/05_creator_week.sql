-- Creator-week table: the core model for segmentation, prediction and the
-- dashboard. Hours are counted from hourly snapshots, so `hours_live` is the
-- number of snapshot hours the creator was live (an hourly sample, not exact
-- minutes) and `viewer_hours` is the matching estimate of hours watched.
create or replace table creator_week as
with weekly as (
    select
        ch.user_id,
        week_start,
        any_value(ch.user_login order by snapshot_hour desc) as user_login,
        count(*)                                  as hours_live,
        count(distinct stream_id)                 as streams,
        count(distinct snapshot_hour::date)       as days_live,
        avg(viewer_count)                         as avg_viewers,
        max(viewer_count)                         as peak_viewers,
        median(viewer_count)                      as median_viewers,
        sum(viewer_count)                         as viewer_hours,
        count(distinct game_name)                 as categories,
        mode(game_name)                           as main_category,
        mode(language)                            as language,
        avg(case when ph.is_peak then 1.0 else 0.0 end) as peak_hour_share,
        avg(case when source = 'top' then 1.0 else 0.0 end) as top_list_share,
        min(rank)                                 as best_rank
    from creator_hour ch
    left join peak_hours ph using (hour_utc)
    group by ch.user_id, week_start
),
with_lags as (
    select
        w.*,
        cw.hours_observed,
        cw.is_complete                                         as is_complete_week,
        datediff('week', date '2020-01-06', w.week_start)      as week_index,
        lag(w.week_start)   over by_user                       as prev_week_start,
        lag(w.avg_viewers)  over by_user                       as prev_avg_viewers,
        lag(w.hours_live)   over by_user                       as prev_hours_live,
        lag(w.viewer_hours) over by_user                       as prev_viewer_hours
    from weekly w
    join collector_weeks cw using (week_start)
    window by_user as (partition by w.user_id order by w.week_start)
),
islands as (
    select
        *,
        -- Gaps-and-islands: consecutive weeks share the same (week_index - row_number).
        week_index - row_number() over (partition by user_id order by week_start) as island
    from with_lags
)
select
    user_id,
    user_login,
    week_start,
    week_index,
    is_complete_week,
    hours_observed,
    hours_live,
    hours_live / hours_observed                  as live_share,
    streams,
    days_live,
    avg_viewers,
    median_viewers,
    peak_viewers,
    viewer_hours,
    categories,
    main_category,
    language,
    peak_hour_share,
    top_list_share,
    best_rank,
    -- Week-on-week growth only when the previous calendar week was also active.
    case when prev_week_start = week_start - interval 7 day
         then avg_viewers / nullif(prev_avg_viewers, 0) - 1 end   as wow_avg_viewers_growth,
    case when prev_week_start = week_start - interval 7 day
         then hours_live / nullif(prev_hours_live, 0) - 1 end     as wow_hours_growth,
    case when prev_week_start = week_start - interval 7 day
         then viewer_hours / nullif(prev_viewer_hours, 0) - 1 end as wow_viewer_hours_growth,
    row_number() over (partition by user_id, island order by week_start) as streak_weeks,
    row_number() over (partition by user_id order by week_start)         as weeks_active_to_date
from islands;
