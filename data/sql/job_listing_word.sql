CREATE TABLE IF NOT EXISTS job_listing_skill(
    id INTEGER PRIMARY KEY NOT NULL,
    job_listing_id INTEGER NOT NULL,
    word TEXT NOT NULL,
    FOREIGN KEY(job_listing_id) REFERENCES job_listing(id)
);