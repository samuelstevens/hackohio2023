CREATE TABLE IF NOT EXISTS post (
    raw TEXT UNIQUE NOT NULL,
    type TEXT NOT NULL,
    topic TEXT NOT NULL,
    facts TEXT NOT NULL, -- comma separated
    likes INTEGER NOT NULL
);
