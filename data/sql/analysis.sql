-- inspect tables
select * from company;
select * from job_listing order by search_rank;
select * from job_listing_skill;
select * from job_listing_word;


-- snippet: basic fact table
select
	s.job_listing_id,
	j.company_id,
	c.company_name,
	c.industry,
	c.company_size,f
	j.career_level,
	s.skill
from job_listing_skill as s
left join job_listing as j
	on s.job_listing_id = j.id
left join company as c
	on j.company_id = c.id;
	
-- snippet: skill count
select
	skill,
	count() as f
from job_listing_skill as s
group by 1
order by 2 desc;


-- snipppet: job listings per industry
select
	c.industry,
	count() as n
from job_listing as j
left join company as c
	on j.company_id = c.id
where c.industry is not null
group by 1
order by 1;


-- snippet: job listings per company
select
	c.company_name,
	count() as n
from job_listing as j
left join company as c
	on j.company_id = c.id
where c.industry is not null
group by 1
order by 1;


-- snippet: job listings per career level
select
	career_level,
	count() as n
from job_listing as j
where career_level is not null
group by 1
order by 2 desc;


-- snippet: job listings per employment type
select
	employment_type,
	count() as n
from job_listing as j
where employment_type is not null
group by 1
order by 2 desc;



-- fact table: top skills by industry (count and frequency)
with facts as (
	select
		c.industry,
		s.skill
	from job_listing_skill as s
	left join job_listing as j
		on s.job_listing_id = j.id
	left join company as c
		on j.company_id = c.id
		),
industry_listings as (
	select
		c.industry,
		count() as n
	from job_listing as j
	left join company as c
		on j.company_id = c.id
	where c.industry is not null
	group by 1
	)
select
	f.industry,
	f.skill,
	count() as n,
	cast(count() as float) / l.n as freq
from facts as f
left join industry_listings as l
 on f.industry = l.industry
where f.industry is not null
group by f.industry, f.skill
order by f.industry, n desc;


-- fact table: top skills by company (count and frequency)
with facts as (
	select
		c.company_name,
		s.skill
	from job_listing_skill as s
	left join job_listing as j
		on s.job_listing_id = j.id
	left join company as c
		on j.company_id = c.id
	),
company_listings as (
	select
		c.company_name,
		count() as n
	from job_listing as j
	left join company as c
		on j.company_id = c.id
	where c.industry is not null
	group by 1
	)
select
	f.company_name,
	f.skill,
	count() as n,
	cast(count() as float) / l.n as freq
from facts as f
left join company_listings as l
 on f.company_name = l.company_name
where f.company_name is not null
group by f.company_name, f.skill
having freq is not null
order by f.company_name, n desc;


-- fact table: top skills by career level (count and frequency)
with facts as (
	select
		j.career_level,
		s.skill
	from job_listing_skill as s
	left join job_listing as j
		on s.job_listing_id = j.id
		),
level_listings as (
	select
		career_level,
		count() as n
	from job_listing as j
	where career_level is not null
	group by 1
	)
select
	f.career_level,
	f.skill,
	count() as n,
	cast(count() as float) / l.n as freq
from facts as f
left join level_listings as l
 on f.career_level = l.career_level
where f.career_level is not null
group by f.career_level, f.skill
order by f.career_level, n desc;


-- fact table: top skills by employment type (count and frequency)
with facts as (
	select
		j.employment_type,
		s.skill
	from job_listing_skill as s
	left join job_listing as j
		on s.job_listing_id = j.id
		),
type_listings as (
	select
		employment_type,
		count() as n
	from job_listing as j
	where employment_type is not null
	group by 1
	)
select
	f.employment_type,
	f.skill,
	count() as n,
	cast(count() as float) / l.n as freq
from facts as f
left join type_listings as l
 on f.employment_type = l.employment_type
where f.employment_type is not null
group by f.employment_type, f.skill
order by f.employment_type, n desc;

	