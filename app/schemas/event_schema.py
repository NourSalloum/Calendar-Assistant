from pydantic import BaseModel
from typing import Optional

from datetime import datetime

class CreateEventSchema(BaseModel):
    google_event_id: str
    summary: str
    start_time: datetime  
    end_time: datetime 
    description: Optional[str] = None
    location: Optional[str] = None
    end_time: datetime 
    description: Optional[str] = None
    location: Optional[str] = None


class UpdateEventSchema(BaseModel):
    google_event_id: str
    summary: Optional[str] = None
    start_time: Optional[datetime] = None  
    end_time: Optional[datetime] = None  
    description: Optional[str] = None
    location: Optional[str] = None

class EventRead(BaseModel):
    google_event_id: str
    summary: str
    start_time: datetime
    end_time: datetime
    description: Optional[str] = None
    location: Optional[str] = None

    class Config:
        from_attributes = True

class FindEventSchema(BaseModel):
    summary: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    description: Optional[str] = None
    location: Optional[str] = None


    class Config:
        from_attributes = True
