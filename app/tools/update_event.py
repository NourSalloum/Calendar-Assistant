from app.services.google_calendar import get_calendar_service
from app.utils.logger import get_logger
from app.utils.exceptions import CalendarEventUpdateError
from app.utils.exceptions import EventConflictError
from app.utils.datetime_helpers import convert_to_google_iso,get_user_timezone
from googleapiclient.errors import HttpError
from app.services.event_services import update_event_service,FindEventService
from app.schemas.event_schema import FindEventSchema, UpdateEventSchema
from sqlalchemy.orm import Session
from app.utils.dependencies import get_db
from langchain.tools import tool


logger = get_logger(__name__)

def check_events_conflict(service, start_time, end_time, exclude_event_id=None):
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
            if exclude_event_id and event["id"] == exclude_event_id:
                continue
            return event  

        return None
    except HttpError as error:
        logger.error(f"Conflict check error: {error}")
        raise EventConflictError("Failed to check for event conflicts") from error

@tool  
def update_event(google_event_id:str,summary:str=None, start_time:str=None, end_time:str=None, description:str=None, location:str=None)->dict:
    """
    Updates an existing event in the user's Google Calendar.
    Args:
        google_event_id (str): The Google Event ID of the event to be updated.
        summary (str, optional): The new title of the event.
        start_time (str, optional): The new start time of the event.
        end_time (str, optional): The new end time of the event.
        description (str, optional): The new description of the event.
        location (str, optional): The new location of the event.
    Returns:
        dict: The updated event object.
    """
    service = get_calendar_service()
    user_timezone=get_user_timezone(service)
    db=next(get_db())

    try:

        event = service.events().get(calendarId="primary", eventId=google_event_id).execute()
        current_start = event["start"]["dateTime"]
        current_end = event["end"]["dateTime"]
        new_start = convert_to_google_iso(start_time, user_timezone) if start_time else current_start
        new_end = convert_to_google_iso(end_time, user_timezone) if end_time else current_end
        if new_start!=current_start or new_end!=current_end:
            conflict_event = check_events_conflict(service, new_start, new_end, exclude_event_id=google_event_id)
            if conflict_event:
                logger.warning("Event conflict detected. Cannot update event.")
                raise EventConflictError({
                        "summary": conflict_event.get("summary"),
                        "start_time": conflict_event["start"].get("dateTime"),
                        "end_time": conflict_event["end"].get("dateTime"),
                        "description": conflict_event.get("description"),
                        "location": conflict_event.get("location"),
           })
            
       
        if summary:
            event["summary"] = summary
        if start_time:
            event["start"] = {"dateTime": new_start, "timeZone": user_timezone}
        if end_time:
            event["end"] = {"dateTime": new_end, "timeZone": user_timezone}
        if description:
            event["description"] = description
        if location:
            event["location"] = location
    
        updated_event = service.events().update(calendarId="primary", eventId=google_event_id, body=event).execute()
        update_event_service(db=db, event=UpdateEventSchema(
            google_event_id=google_event_id,
            summary=summary,
            start_time=new_start,
            end_time=new_end,
            description=description,
            location=location
        ))
        return updated_event
    except HttpError as error:
        logger.error(f"An error occurred while updating the event: {error}")
        raise CalendarEventUpdateError("Failed to update the calendar event") from error
    except Exception as ex:
        logger.error(f"An unexpected error occurred: {ex}")
        raise CalendarEventUpdateError("An unexpected error occurred while updating the event") from ex

    
