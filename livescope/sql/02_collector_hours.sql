-- Hours in which the collector produced a snapshot. Used to tell "creator was
-- offline" apart from "we did not look", and to flag incomplete weeks.
create or replace table collector_hours as
select distinct
    snapshot_hour,
    date_trunc('week', snapshot_hour)::date as week_start
from stg_streams;

create or replace table collector_weeks as
select
    week_start,
    count(*)                                   as hours_observed,
    count(*) / 168.0                           as coverage,
    -- A week is usable for week-on-week metrics when it is over and at least
    -- 90% of its hours were captured.
    (count(*) >= 0.9 * 168
     and week_start + interval 7 day <= (select max(snapshot_hour) + interval 1 hour from collector_hours))
                                               as is_complete
from collector_hours
group by week_start;
