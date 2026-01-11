from datetime import datetime
from zoneinfo import ZoneInfo
from app.utils.logger import get_logger
import dateparser

logger = get_logger(__name__)
def convert_to_google_iso(dt_str: str, user_timezone: str) -> str:
    
    now = datetime.now(ZoneInfo(user_timezone))
    
    dt = dateparser.parse(
        dt_str,
        settings={
            "RELATIVE_BASE": now,                
            "TO_TIMEZONE": user_timezone,  
            "TIMEZONE": user_timezone,          
            "RETURN_AS_TIMEZONE_AWARE": True,   
            "PREFER_DATES_FROM": "future"       
        }
    )
   
    if not dt:
        raise ValueError(f"Could not parse date string: {dt_str}")
    
    return dt.isoformat()



def get_user_timezone(service) -> str:
    calendar = service.calendars().get(calendarId="primary").execute()
    return calendar["timeZone"]
