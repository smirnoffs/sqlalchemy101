from sqlalchemy.sql.expression import insert
from fastapi import FastAPI, Depends
from pydantic import BaseModel
import time

from sqlalchemy import create_engine, Column, Integer, String, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DB_PATH = "tickets.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///./{DB_PATH}"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # SQLite specific
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


Base = declarative_base()


class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String(length=255), nullable=False)
    title = Column(String(length=255), nullable=False)
    status = Column(String(length=255), nullable=False)
    created_at = Column(BigInteger, nullable=False)


Base.metadata.create_all(bind=engine)


class TicketBase(BaseModel):
    ticket_id: str
    title: str
    status: str


app = FastAPI()


@app.post("/tickets")
def create_ticket(ticket: TicketBase, db=Depends(get_db)):
    created_at = int(time.time() * 1000)  # precision in milliseconds
    ticket_inst = Ticket(
        ticket_id=ticket.ticket_id,
        title=ticket.title,
        status=ticket.status,
        created_at=created_at,
    )
    db.add(ticket_inst)
    db.commit()
    return db.query(Ticket).all()


@app.get("/tickets")
def list_tickets(db=Depends(get_db)):
    """
    Returns list of tickets with latest statuses.
    """
    return db.query(Ticket)
    return [
        {
            "ticket_id": ticket_id,
            "title": title,
            "status": status,
            "created_at": created_at / 1000,
        }
        for ticket_id, title, status, created_at in db.fetchall()
    ]
