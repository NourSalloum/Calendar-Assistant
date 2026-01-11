from app.schemas.event_schema import FindEventSchema
from app.services.event_services import FindEventService
from app.utils.dependencies import get_db
from langchain.tools import tool
from app.utils.logger import get_logger
from app.utils.exceptions import EventNotFoundError

logger = get_logger(__name__)

@tool
def find_event(start_time: str=None, end_time: str=None, summary: str=None, description: str=None, location: str=None) ->str:
    """Finds an event in the database based on start and end times.
    Args:
        summary (str): The summary of the event.
        start_time (str): Start time string (ISO-like).
        end_time (str): End time string (ISO-like).
    Returns:
        str: The Google Event ID of the found event.
        """
    db = next(get_db())
    try:
        event = FindEventService(
        db=db,
        data=FindEventSchema(start_time=start_time, end_time=end_time, summary=summary, description=description, location=location)
        )
        return event.google_event_id
    except EventNotFoundError as e:
        logger.error(f"Event not found: {e}")
        return "No event found matching the provided criteria."
