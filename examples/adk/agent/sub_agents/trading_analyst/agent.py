"""Execution_analyst_agent for finding the ideal execution strategy"""

from google.adk import Agent

from . import prompt

MODEL="gemini-2.5-pro"

trading_analyst_agent = Agent(
    model=MODEL,
    name="trading_analyst_agent",
    instruction=prompt.TRADING_ANALYST_PROMPT,
    output_key="proposed_trading_strategies_output",
)
