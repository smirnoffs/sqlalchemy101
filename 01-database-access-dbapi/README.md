# DB API

Let's run the application 
```sh
uvicorn app:app --reload
```

and make a POST requests to `/tickets`
```sh
curl --request POST \
  --url http://localhost:8000/tickets \
  --header 'content-type: application/json' \
  --data '{"ticket_id": "LOL-808", "ticket_title": "Important ticket."}'
```

## Problem # 1
```
{"error":"no such table: tickets"}
```
The table tickets doesn't exist. Before running the application we need to 
create required tables.
```python
import sqlite3

create_statement = """
CREATE TABLE tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id varchar(255),
    ticket_title varchar(500)
);"""

DB_PATH = "tickets.db"
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.execute(create_statement)
```

Now POST to `/tickets` works.