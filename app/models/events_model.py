import uuid
from app.database import Base
from sqlalchemy import Column, Integer, String, DateTime

class Event(Base):
    __tablename__ = 'events'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    google_event_id = Column(String, unique=True, nullable=False)
    summary = Column(String, index=True)
    description = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
