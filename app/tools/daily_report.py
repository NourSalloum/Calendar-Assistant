from app.services.google_calendar import get_calendar_service
from googleapiclient.errors import HttpError
from app.utils.exceptions import CalendarDailyReportError
from app.utils.datetime_helpers import convert_to_google_iso,get_user_timezone
from app.utils.logger import get_logger
from langchain.tools import tool


logger = get_logger(__name__)

@tool
def daily_report(start_time:str, end_time:str)->list:
    """
    Generates a daily report of calendar events.
    Args:
        start_time (str): Start time string (ISO-like).
        end_time (str): End time string (ISO-like).
    Returns:
        list: A list of events for the day.
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
        return events
    except HttpError as error:
        logger.error(f"An error occurred while generating the daily report: {error}")
        raise CalendarDailyReportError("Failed to generate daily report") from error
    except Exception as ex:
        logger.error(f"An unexpected error occurred: {ex}")
        raise CalendarDailyReportError("An unexpected error occurred during daily report generation") from ex
