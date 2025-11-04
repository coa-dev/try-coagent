"""Execution_analyst_agent for finding the ideal execution strategy"""

from google.adk import Agent

from . import prompt

MODEL = "gemini-2.5-pro"

execution_analyst_agent = Agent(
    model=MODEL,
    name="execution_analyst_agent",
    instruction=prompt.EXECUTION_ANALYST_PROMPT,
    output_key="execution_plan_output",
)
