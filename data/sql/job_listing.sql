CREATE TABLE IF NOT EXISTS job_listing(
    id INTEGER PRIMARY KEY NOT NULL,
    search_rank INTEGER NOT NULL,
    job_title TEXT NOT NULL,
    region TEXT NOT NULL,
    applicant_count INTEGER,
    salary TEXT,
    employment_type TEXT NOT NULL,
    career_level TEXT,
    description TEXT,
    company_id INTEGER NOT NULL,
    date_queried TEXT,
    date_posted TEXT,
    FOREIGN KEY(company_id) REFERENCES company(id)
);