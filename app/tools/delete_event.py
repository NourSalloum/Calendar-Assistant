from app.services.google_calendar import get_calendar_service
from app.utils.dependencies import get_db
from app.utils.exceptions import CalendarEventDeletionError
from app.utils.logger import get_logger
from googleapiclient.errors import HttpError
from app.services.event_services import delete_event_service
from langchain.tools import tool


logger = get_logger(__name__)


@tool
def delete_event(google_event_id:str)->bool:
    """
    Deletes an event from the user's Google Calendar.
    Args:
        google_event_id (str): The Google Event ID of the event to be deleted .
    Returns:
        bool: True if the event was deleted successfully, False otherwise.
    """
    service = get_calendar_service()
    db = next(get_db())
    
    try:
        service.events().delete(calendarId="primary", eventId=google_event_id).execute()
        delete_event_service(db, google_event_id)
        return True
    except HttpError as error:
        logger.error(f"An error occurred while deleting the event: {error}")
        raise CalendarEventDeletionError("Failed to delete calendar event") from error
    except Exception as ex:
        logger.error(f"An unexpected error occurred: {ex}")
        raise CalendarEventDeletionError("An unexpected error occurred during event deletion") from ex