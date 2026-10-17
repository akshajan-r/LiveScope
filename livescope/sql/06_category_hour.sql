create or replace table category_hour as
select
    snapshot_hour,
    game_name,
    count(*)          as live_creators,
    sum(viewer_count) as total_viewers
from creator_hour
group by snapshot_hour, game_name;

create or replace table category_week as
with raw as (
    select
        week_start,
        game_name,
        count(distinct user_id) as creators,
        count(*)                as creator_hours,
        sum(viewer_count)       as viewer_hours,
        sum(viewer_count) / count(*) as viewers_per_live_hour
    from creator_hour
    group by week_start, game_name
)
select h.* from history_category_week h, raw_bounds rb
where h.week_start < rb.first_full_week
union all by name
select r.* from raw r, raw_bounds rb
where r.week_start >= rb.first_full_week
   or r.week_start not in (select distinct week_start from history_category_week);
