import sqlite3
from fastapi import FastAPI, Depends
from pydantic import BaseModel
import time

app = FastAPI()
DB_PATH = "tickets.db"


def get_db_cursor():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    try:
        yield cur
    finally:
        conn.commit()
        conn.close()


class TicketBase(BaseModel):
    ticket_id: str
    title: str
    status: str


@app.post("/tickets")
def create_ticket(ticket: TicketBase, cursor=Depends(get_db_cursor)):
    created_at = int(time.time() * 1000)  # precision in milliseconds
    try:
        cursor.execute(
            "INSERT INTO tickets (ticket_id, title, status, created_at) VALUES (?, ?, ?, ?)",
            (ticket.ticket_id, ticket.title, ticket.status, created_at),
        )
        print(cursor.fetchone())
    except Exception as e:
        return {"error": str(e)}
    cursor.execute("select * from tickets;")
    return cursor.fetchall()


@app.get("/tickets")
def list_tickets(cursor=Depends(get_db_cursor)):
    """
    Returns list of tickets with latest statuses.
    """
    cursor.execute(
        """
    SELECT t.ticket_id, t.title, t.status, t.created_at from tickets t 
    JOIN
    (SELECT ticket_id, MAX(created_at) as latest 
        FROM tickets GROUP BY ticket_id) tm
    ON t.ticket_id = tm.ticket_id
    WHERE t.created_at=latest    
    """
    )
    return [
        {
            "ticket_id": ticket_id,
            "title": title,
            "status": status,
            "created_at": created_at / 1000,
        }
        for ticket_id, title, status, created_at in cursor.fetchall()
    ]
