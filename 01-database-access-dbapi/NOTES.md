### DB API

First we need a table.
```python
import sqlite3

conn = sqlite3.connect("tickets.db")
cur = conn.cursor()
cur.execute("""
CREATE TABLE tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id varchar(255),
    ticket_title varchar(500)
);
""")
conn.commit()
conn.close()
```

Now let's insert a new row into the table.
```python
import sqlite3

conn = sqlite3.connect("tickets.db")
cur = conn.cursor()
cur.execute("INSERT INTO tickets (ticket_id, ticket_title) VALUES (, ?)")
conn.commit()
conn.close()
```

### Potential problems
1. We need to make sure that all tables that the application uses already exist.
2. It's easy to forget to commit the transaction.