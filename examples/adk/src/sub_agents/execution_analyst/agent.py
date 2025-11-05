"""Execution_analyst_agent for finding the ideal execution strategy"""

from google.adk import Agent

from . import prompt
from src.config import get_litellm_model

execution_analyst_agent = Agent(
    model=get_litellm_model(),
    name="execution_analyst_agent",
    instruction=prompt.EXECUTION_ANALYST_PROMPT,
    output_key="execution_plan_output",
)
