"""Execution_analyst_agent for finding the ideal execution strategy"""

from google.adk import Agent

from agent.config import get_gemini_model

from . import prompt

execution_analyst_agent = Agent(
    model=get_gemini_model(),
    name="execution_analyst_agent",
    instruction=prompt.EXECUTION_ANALYST_PROMPT,
    output_key="execution_plan_output",
)
