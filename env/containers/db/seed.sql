CREATE TABLE library_user (
    id SERIAL PRIMARY KEY,
    name VARCHAR(1024),
    created_at TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'UTC'),
    updated_at TIMESTAMP DEFAULT (NOW() AT TIME ZONE 'UTC')
);

INSERT INTO library_user(name) VALUES ('Test User');
