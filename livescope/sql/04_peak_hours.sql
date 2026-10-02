-- Platform peak hours: the 6 UTC hours of the day with the highest average
-- total concurrent viewers across the creators we observe.
create or replace table platform_hour as
select
    snapshot_hour,
    count(*)                         as live_creators,
    sum(viewer_count)                as total_viewers,
    sum(viewer_count) filter (where source = 'top') as top_viewers,
    count(distinct game_name)        as categories
from creator_hour
group by snapshot_hour;

create or replace table peak_hours as
with by_hour as (
    select hour(snapshot_hour) as hour_utc, avg(total_viewers) as avg_total_viewers
    from platform_hour
    group by 1
)
select
    hour_utc,
    avg_total_viewers,
    row_number() over (order by avg_total_viewers desc, hour_utc) <= 6 as is_peak
from by_hour;
