import sqlite3

create_statement = """
CREATE TABLE tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id   varchar(255) NOT NULL,
    title       varchar(500) NOT NULL,
    status      varchar(100) NOT NULL,
    created_at  BIGINT
);"""

DB_PATH = "tickets.db"
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.execute(create_statement)
