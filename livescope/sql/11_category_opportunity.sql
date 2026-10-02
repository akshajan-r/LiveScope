-- Category opportunity over the last 28 days: where is audience per creator
-- high relative to the number of creators serving it?
-- Medians across creators are used, so one star streamer cannot make a
-- category look under-served; `top_creator_share` flags categories that are
-- one creator's audience rather than open demand. Computed for all creators
-- and separately for each language group.
create or replace table category_opportunity as
with bounds as (
    select max(snapshot_hour) as last_hour, min(snapshot_hour) as first_hour from creator_hour
),
ch as (
    select ch.*, coalesce(cl.language_group, 'Other') as language_group,
           ch.snapshot_hour > b.last_hour - interval 14 day as recent
    from creator_hour ch
    cross join bounds b
    left join creator_language cl using (user_id)
    where ch.snapshot_hour > b.last_hour - interval 28 day
),
scoped as (
    select *, 'All' as scope from ch
    union all
    select *, language_group as scope from ch
),
creator_cat as (
    select scope, game_name, user_id,
           count(*) as hours, avg(viewer_count) as avg_viewers, sum(viewer_count) as viewer_hours,
           sum(viewer_count) filter (where recent)     as vh_recent,
           sum(viewer_count) filter (where not recent) as vh_prior
    from scoped group by all
),
scope_median as (
    select scope, median(avg_viewers) as median_viewers from creator_cat group by scope
),
cats as (
    select
        scope, game_name,
        count(*)                                as creators,
        sum(hours)                              as creator_hours,
        sum(viewer_hours)                       as viewer_hours,
        sum(viewer_hours) / sum(hours)          as viewers_per_live_hour,
        median(avg_viewers)                     as median_creator_viewers,
        max(viewer_hours) / sum(viewer_hours)   as top_creator_share,
        sum(vh_recent)                          as vh_recent,
        sum(vh_prior)                           as vh_prior
    from creator_cat group by all
)
select
    c.scope,
    c.game_name,
    c.creators,
    c.creator_hours,
    c.viewer_hours,
    c.viewers_per_live_hour,
    c.median_creator_viewers,
    c.median_creator_viewers / nullif(m.median_viewers, 0) as opportunity_index,
    c.top_creator_share,
    -- Last 14 days vs the 14 before; null until 28 days have been collected.
    case when (select last_hour - first_hour from bounds) >= interval 27 day
         then c.vh_recent / nullif(c.vh_prior, 0) - 1 end   as viewer_hours_growth,
    c.creators >= 5                                          as enough_creators
from cats c
join scope_median m using (scope)
order by c.scope, opportunity_index desc;
