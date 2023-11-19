CREATE TABLE IF NOT EXISTS economy (
    id        NUMERIC PRIMARY KEY
                      UNIQUE
                      NOT NULL,
    user_id   NUMERIC NOT NULL,
    server_id NUMERIC NOT NULL,
    money     NUMERIC NOT NULL
);
