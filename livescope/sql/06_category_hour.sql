create or replace table category_hour as
select
    snapshot_hour,
    game_name,
    count(*)          as live_creators,
    sum(viewer_count) as total_viewers
from creator_hour
group by snapshot_hour, game_name;

create or replace table category_week as
select
    week_start,
    game_name,
    count(distinct user_id) as creators,
    count(*)                as creator_hours,
    sum(viewer_count)       as viewer_hours,
    sum(viewer_count) / count(*) as viewers_per_live_hour
from creator_hour
group by week_start, game_name;
