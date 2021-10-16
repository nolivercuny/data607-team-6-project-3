CREATE TABLE job_listing(
    id INTEGER PRIMARY KEY NOT NULL,
    search_rank INTEGER NOT NULL,
    job_title TEXT NOT NULL,
    region TEXT NOT NULL,
    applicant_count INTEGER,
    salary TEXT,
    employment_type TEXT NOT NULL,
    career_level TEXT,
    description TEXT,
    date_queried TEXT NOT NULL,
    date_posted TEXT NOT NULL,
    FOREIGN KEY(company_id) REFERENCES company(id)
);