-- Language groups. Twitch reports the broadcast language, not the country, so
-- these are proxies: "es" covers Spain and Latin America, "pt" mostly Brazil,
-- "en" the US, UK and everyone streaming in English. Spanish and Portuguese are
-- kept apart from the other European languages for that reason.
create or replace table language_groups as
select * from (values
    ('en', 'English',    'English'),
    ('de', 'German',     'EU/EEA languages'),
    ('fr', 'French',     'EU/EEA languages'),
    ('it', 'Italian',    'EU/EEA languages'),
    ('pl', 'Polish',     'EU/EEA languages'),
    ('nl', 'Dutch',      'EU/EEA languages'),
    ('sv', 'Swedish',    'EU/EEA languages'),
    ('da', 'Danish',     'EU/EEA languages'),
    ('fi', 'Finnish',    'EU/EEA languages'),
    ('no', 'Norwegian',  'EU/EEA languages'),
    ('cs', 'Czech',      'EU/EEA languages'),
    ('sk', 'Slovak',     'EU/EEA languages'),
    ('hu', 'Hungarian',  'EU/EEA languages'),
    ('ro', 'Romanian',   'EU/EEA languages'),
    ('bg', 'Bulgarian',  'EU/EEA languages'),
    ('el', 'Greek',      'EU/EEA languages'),
    ('hr', 'Croatian',   'EU/EEA languages'),
    ('sl', 'Slovenian',  'EU/EEA languages'),
    ('et', 'Estonian',   'EU/EEA languages'),
    ('lv', 'Latvian',    'EU/EEA languages'),
    ('lt', 'Lithuanian', 'EU/EEA languages'),
    ('ca', 'Catalan',    'EU/EEA languages'),
    ('es', 'Spanish',    'Spanish & Portuguese'),
    ('pt', 'Portuguese', 'Spanish & Portuguese'),
    ('ja', 'Japanese',   'Other'),
    ('ko', 'Korean',     'Other'),
    ('zh', 'Chinese',    'Other'),
    ('zh-hk', 'Chinese (Hong Kong)', 'Other'),
    ('ru', 'Russian',    'Other'),
    ('uk', 'Ukrainian',  'Other'),
    ('tr', 'Turkish',    'Other'),
    ('ar', 'Arabic',     'Other'),
    ('th', 'Thai',       'Other'),
    ('vi', 'Vietnamese', 'Other'),
    ('id', 'Indonesian', 'Other'),
    ('ms', 'Malay',      'Other'),
    ('tl', 'Tagalog',    'Other'),
    ('hi', 'Hindi',      'Other'),
    ('other', 'Other',   'Other'),
    ('asl', 'Sign language', 'Other')
) t(language, language_name, language_group);

-- Each creator's main broadcast language over everything observed.
create or replace table creator_language as
select
    cs.user_id,
    cs.language,
    coalesce(lg.language_name, cs.language)  as language_name,
    coalesce(lg.language_group, 'Other')     as language_group
from creator_summary cs
left join language_groups lg using (language);

create or replace table language_week as
select
    cw.week_start,
    cl.language,
    cl.language_name,
    cl.language_group,
    count(*)                                  as active_creators,
    sum(cw.viewer_hours)                      as viewer_hours,
    sum(cw.hours_live)                        as creator_hours,
    sum(cw.viewer_hours) / sum(cw.hours_live) as viewers_per_live_hour,
    median(cw.wow_avg_viewers_growth)         as median_wow_growth,
    -- Share of this week's creators not live the following week. Null until
    -- that week is complete.
    case when bool_or(nxt.is_complete) then
        avg(case when n1.user_id is null then 1.0 else 0.0 end) end as drop_off_rate
from creator_week cw
join creator_language cl using (user_id)
left join collector_weeks nxt on nxt.week_start = cw.week_start + interval 7 day
left join creator_week n1 on n1.user_id = cw.user_id and n1.week_start = cw.week_start + interval 7 day
where cw.is_complete_week
group by all;
