-- One row per stream per snapshot hour. Re-runs within the same hour are
-- deduplicated by keeping the latest capture. Timestamps are naive UTC.
create or replace table stg_streams as
select
    snapshot_at::timestamp                  as snapshot_at,
    snapshot_hour::timestamp                as snapshot_hour,
    stream_id,
    user_id,
    user_login,
    game_id,
    coalesce(nullif(game_name, ''), '(none)') as game_name,
    language,
    viewer_count,
    started_at::timestamp                   as started_at,
    source,
    rank
from raw_snapshots
qualify row_number() over (
    partition by stream_id, snapshot_hour::timestamp
    order by snapshot_at desc
) = 1;
