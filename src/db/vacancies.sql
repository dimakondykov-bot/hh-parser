CREATE TABLE IF NOT EXISTS employers (
    employer_id TEXT PRIMARY KEY,
    name TEXT,
    trusted BOOLEAN
);


DROP TABLE IF EXISTS vacancies;

CREATE TABLE vacancies (
    id                 serial PRIMARY KEY,
    hh_id              bigint UNIQUE,
    employer_id        text REFERENCES employers(employer_id),
    name               text,
    description        text,
    salary_min         numeric,
    salary_max         numeric,
    currency           text,
    employment         text,
    experience         text,
    published_at       timestamp
);