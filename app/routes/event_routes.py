from fastapi import APIRouter, Depends
from app.schemas.event_schema import CreateEventSchema, UpdateEventSchema, EventRead
from app.services.event_services import create_event_service, get_event_by_google_id, update_event_service,delete_event_service,get_all_events_service
from app.utils.dependencies import get_db
from sqlalchemy.orm import Session
from app.utils.logger import get_logger
from app.utils.exceptions import EventNotFoundError
from app.models.events_model import Event

logger = get_logger(__name__)
router = APIRouter(
    prefix="/events",
    tags=["events"]
)

@router.post("/", response_model=EventRead)
def create_new_event(event: CreateEventSchema, db: Session = Depends(get_db)):
    return create_event_service(db, event)

@router.get("/{google_event_id}", response_model=EventRead)
def read_event(google_event_id: str, db: Session = Depends(get_db)):
    db_event = get_event_by_google_id(db, google_event_id)
    if db_event is None:
        logger.error(f"Event with Google ID {google_event_id} not found.")
        raise EventNotFoundError(status_code=404, detail="Event not found")
    return db_event

@router.put("/{google_event_id}", response_model=EventRead)
def update_existing_event(event: UpdateEventSchema, db: Session = Depends(get_db)):
    return update_event_service(db, event)

@router.delete("/{google_event_id}")
def delete_existing_event(google_event_id: str, db: Session = Depends(get_db)):
    return delete_event_service(db, google_event_id)
@router.get("/", response_model=list[EventRead])
def read_all_events(db: Session = Depends(get_db)):
    return get_all_events_service(db)
