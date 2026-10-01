-- One row per creator per observed hour. If a creator has two live streams in
-- the same hour (rare: restarts), keep the one with more viewers.
create or replace table creator_hour as
select
    user_id,
    user_login,
    snapshot_hour,
    date_trunc('week', snapshot_hour)::date as week_start,
    hour(snapshot_hour)                     as hour_utc,
    stream_id,
    game_name,
    language,
    viewer_count,
    source,
    rank
from stg_streams
qualify row_number() over (
    partition by user_id, snapshot_hour
    order by viewer_count desc, stream_id
) = 1;
