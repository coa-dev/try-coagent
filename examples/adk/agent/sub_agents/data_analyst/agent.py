"""data_analyst_agent for finding information using google search"""

from google.adk import Agent
from google.adk.tools import google_search

from agent.config import get_gemini_model

from . import prompt

data_analyst_agent = Agent(
    model=get_gemini_model(),
    name="data_analyst_agent",
    instruction=prompt.DATA_ANALYST_PROMPT,
    output_key="market_data_analysis_output",
    tools=[google_search],
)
