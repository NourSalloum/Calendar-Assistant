from app.tools.create_event import create_event
from app.tools.delete_event import delete_event
from app.tools.availability import check_availability
from app.tools.update_event import update_event
from app.tools.daily_report import daily_report
from app.tools.find_event import find_event
from langchain_openai import ChatOpenAI
from app.agent.prompts import CALENDAR_AGENT_PROMPT
from langchain.agents import create_agent
from datetime import datetime

from dotenv import load_dotenv
import os

load_dotenv()

tools = [
    create_event,
    delete_event,
    check_availability,
    update_event,
    find_event,
    daily_report
]

llm = ChatOpenAI(
    model_name="gpt-4o-mini",  
    temperature=0,
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base=os.getenv("OPENAI_API_BASE"),  
)

# Dynamically inject today's date and day of week into the prompt
today_date = datetime.now().strftime("%B %d, %Y")
day_of_week = datetime.now().strftime("%A")
system_prompt = CALENDAR_AGENT_PROMPT.format(current_date=today_date, day_of_week=day_of_week)

calendar_agent = create_agent(llm, tools=tools, system_prompt=system_prompt)
