CREATE TABLE IF NOT EXISTS economy (
    id        INTEGER PRIMARY KEY AUTOINCREMENT
                      UNIQUE
                      NOT NULL,
    server_id NUMERIC NOT NULL,
    user_id   NUMERIC NOT NULL,
    money     NUMERIC NOT NULL
);