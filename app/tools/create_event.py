from app.services.google_calendar import get_calendar_service
from app.utils.logger import get_logger
from app.utils.exceptions import CalendarEventCreationError
from app.utils.exceptions import EventConflictError
from googleapiclient.errors import HttpError
from app.services.event_services import create_event_service
from app.schemas.event_schema import CreateEventSchema
from sqlalchemy.orm import Session
from app.utils.dependencies import get_db
from langchain.tools import tool
from app.utils.datetime_helpers import convert_to_google_iso,get_user_timezone


logger = get_logger(__name__)

def check_event_conflict(service, start_time, end_time):
    """
    Checks for event conflicts in the user's Google Calendar.
    Args:
        service: The Google Calendar service object.
        start_time (str): Start time string (ISO-like).
        end_time (str): End time string (ISO-like).
    Returns:
        dict: The conflicting event details if a conflict exists, None otherwise.
    """    
    try:
        events_result = service.events().list(
            calendarId="primary",
            timeMin=start_time,
            timeMax=end_time,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        
        events = events_result.get("items", [])
        for event in events:
            return {
                "summary": event.get("summary"),
                "start_time": event["start"].get("dateTime"),
                "end_time": event["end"].get("dateTime"),
                "location": event.get("location"),
            }

        return None

    except HttpError as error:
        logger.error(f"An error occurred while checking for event conflicts: {error}")
        raise EventConflictError("Failed to check for event conflicts") from error
    except Exception as ex:
        logger.error(f"An unexpected error occurred: {ex}")
        raise EventConflictError("An unexpected error occurred during conflict check") from ex
@tool
def create_event(summary:str, start_time:str, end_time:str, description:str=None, location:str=None)->dict:
    """
    Creates an event in the user's Google Calendar.
    Args:
        summary (str): The title of the event.
        start_time (str): Start time string (ISO-like).
        end_time (str): End time string (ISO-like).
        description (str, optional): The description of the event.
        location (str, optional): The location of the event.
    Returns:
        dict: The created event object.
            
    """

    service = get_calendar_service()
    user_timezone = get_user_timezone(service)
    try:
        start_time = convert_to_google_iso(start_time,user_timezone)
        end_time = convert_to_google_iso(end_time,user_timezone)
        event = {
            "summary": summary,
            "start": {"dateTime": start_time,"timeZone": user_timezone},
            "end": {"dateTime": end_time,"timeZone": user_timezone},
        }

        if description:
            event["description"] = description
        if location:
            event["location"] = location
        conflict_event = check_event_conflict(service, start_time, end_time)
        if conflict_event:
            return {
                "status": "conflict",
                "message": "You already have a conflicting event.",
                "conflict_event": conflict_event
            }
        created_event = service.events().insert(calendarId="primary", body=event).execute()
        # Create the event in the database
        db = next(get_db())
        create_event_service(
            db=db,
            event=CreateEventSchema(
                google_event_id=created_event.get("id"),
                summary=summary,
                start_time=start_time,
                end_time=end_time,
                description=description,
                location=location
            )
        )
        return created_event
    except HttpError as error:
        logger.error(f"An error occurred while creating the event: {error}")
        raise CalendarEventCreationError("Failed to create calendar event") from error