#!/bin/bash
# Execute the SQL file
psql $DATABASE_URL -c \
"
CREATE TABLE IF NOT EXISTS anime (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS access_tokens (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    token TEXT,

    CONSTRAINT fk_user FOREIGN KEY (user_id)
    REFERENCES users (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);
CREATE TABLE IF NOT EXISTS openings (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    anime_id INTEGER,
    codename TEXT UNIQUE,
    youtube_embed_link TEXT,
    thumbnail_link TEXT,

    CONSTRAINT fk_anime FOREIGN KEY (anime_id)
    REFERENCES anime (id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);
"

# Check if the command was successful
if [ $? -eq 0 ]; then
    echo "Tables created successfully."
else
    echo "Failed to create tables."
fi
