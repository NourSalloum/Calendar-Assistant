from app.models.events_model import Event
from sqlalchemy.orm import Session
from app.utils.exceptions import EventNotFoundError
from app.schemas.event_schema import CreateEventSchema, UpdateEventSchema, EventRead,FindEventSchema
from app.utils.logger import get_logger

logger = get_logger(__name__)



def create_event_service(db: Session, event: CreateEventSchema) -> Event:
    new_event = Event(
        google_event_id=event.google_event_id,
        summary=event.summary,
        description=event.description,
        start_time=event.start_time,
        end_time=event.end_time
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event

def FindEventService(db: Session, data: FindEventSchema) -> Event:
    query = db.query(Event)
    if data.start_time and data.end_time:
        query = query.filter(
            Event.start_time <= data.end_time,
            Event.end_time >= data.start_time
        )
    elif data.start_time:
        query = query.filter(Event.end_time >= data.start_time)
    elif data.end_time:
        query = query.filter(Event.start_time <= data.end_time)
    if data.summary:
        query = query.filter(Event.summary.ilike(f"%{data.summary}%"))
    if data.description:
        query = query.filter(Event.description.ilike(f"%{data.description}%"))
    if data.location:
        query = query.filter(Event.location.ilike(f"%{data.location}%"))

    event = query.first()  

    if not event:
        raise EventNotFoundError("No event found matching the provided criteria.")

    return event

def get_event_by_google_id(db: Session, google_event_id: str) -> Event:
    return db.query(Event).filter(Event.google_event_id == google_event_id).first()

def delete_event_service(db: Session, google_event_id: str) -> None:
    event = db.query(Event).filter(Event.google_event_id == google_event_id).first()
    if not event:
        logger.error(f"Event with Google ID {google_event_id} not found.")
        raise EventNotFoundError(f"Event with Google ID {google_event_id} not found.")
    
    db.delete(event)
    db.commit()

def update_event_service(db: Session, event: UpdateEventSchema) -> Event:
    db_event = db.query(Event).filter(Event.google_event_id == event.google_event_id).first()
    if not db_event:
        logger.error(f"Event with Google ID {event.google_event_id} not found.")
        raise EventNotFoundError(f"Event with Google ID {event.google_event_id} not found.")
    if event:
        if event.summary is not None:
            db_event.summary = event.summary
        if event.description is not None:
            db_event.description = event.description
        if event.start_time is not None:
            db_event.start_time = event.start_time
        if event.end_time is not None:
            db_event.end_time = event.end_time
        db.commit()
        db.refresh(db_event)
    return db_event

def delete_event_service(db: Session, google_event_id: str) -> None:
    event = db.query(Event).filter(Event.google_event_id == google_event_id).first()
    if not event:
        logger.error(f"Event with Google ID {google_event_id} not found.")
        raise EventNotFoundError(f"Event with Google ID {google_event_id} not found.")
    
    db.delete(event)
    db.commit()

def get_all_events_service(db: Session) -> list[Event]:
    return db.query(Event).all()
    