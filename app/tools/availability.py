from app.services.google_calendar import get_calendar_service
from googleapiclient.errors import HttpError
from app.utils.exceptions import CalendarAvailabilityError
from app.utils.datetime_helpers import convert_to_google_iso,get_user_timezone
from app.utils.logger import get_logger
from langchain.tools import tool


logger = get_logger(__name__)
@tool
def check_availability(start_time:str, end_time:str)->bool:
    """
    Checks the availability of the user's calendar between the specified start and end times.
    Args:
        start_time (str): The start time in RFC3339 format.
        end_time (str): The end time in RFC3339 format.
    Returns:
        bool: True if the user is available, False otherwise.   
    """
    service = get_calendar_service()
    user_timezone=get_user_timezone(service)
    try:
        start_time = convert_to_google_iso(start_time,user_timezone)
        end_time = convert_to_google_iso(end_time,user_timezone)
        events_result = service.events().list(
            calendarId="primary",
            timeMin=start_time,
            timeMax=end_time,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        events = events_result.get("items", [])
        return len(events) == 0
    except HttpError as error:
        logger.error(f"An error occurred while checking availability: {error}")
        raise CalendarAvailabilityError("Failed to check calendar availability") from error
    except Exception as ex:
        logger.error(f"An unexpected error occurred: {ex}")
        raise CalendarAvailabilityError("An unexpected error occurred during availability check") from ex