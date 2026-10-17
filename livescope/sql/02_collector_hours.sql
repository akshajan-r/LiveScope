-- Hours in which the collector produced a snapshot. Used to tell "creator was
-- offline" apart from "we did not look", and to flag incomplete weeks.
create or replace table collector_hours as
select distinct
    snapshot_hour,
    date_trunc('week', snapshot_hour)::date as week_start
from stg_streams;

-- Raw snapshots are kept for a limited window (see livescope/storage.py);
-- weekly summaries of older weeks live in the history_* tables. `first_full_week`
-- is the first week entirely covered by the raw data that is still on disk:
-- weeks before it come from history, weeks from it on are computed from raw.
create or replace table raw_bounds as
with b as (select min(snapshot_hour) as first_hour, max(snapshot_hour) as last_hour from collector_hours)
select
    first_hour,
    last_hour,
    case when first_hour = date_trunc('week', first_hour) then date_trunc('week', first_hour)::date
         else (date_trunc('week', first_hour) + interval 7 day)::date end as first_full_week
from b;

create or replace table collector_weeks as
with raw as (
    select week_start, count(*) as hours_observed from collector_hours group by week_start
),
merged as (
    select h.week_start, h.hours_observed
    from history_collector_weeks h, raw_bounds rb
    where h.week_start < rb.first_full_week
    union all
    select r.week_start, r.hours_observed
    from raw r, raw_bounds rb
    where r.week_start >= rb.first_full_week
       or r.week_start not in (select week_start from history_collector_weeks)
)
select
    week_start,
    hours_observed,
    hours_observed / 168.0                     as coverage,
    -- A week is usable for week-on-week metrics when it is over and at least
    -- 90% of its hours were captured.
    (hours_observed >= 0.9 * 168
     and week_start + interval 7 day <= (select last_hour + interval 1 hour from raw_bounds))
                                               as is_complete
from merged;
