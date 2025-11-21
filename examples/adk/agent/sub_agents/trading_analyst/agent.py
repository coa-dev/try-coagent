"""Execution_analyst_agent for finding the ideal execution strategy"""

from google.adk import Agent

from . import prompt

from agent.config import get_gemini_model

trading_analyst_agent = Agent(
    model=get_gemini_model(),
    name="trading_analyst_agent",
    instruction=prompt.TRADING_ANALYST_PROMPT,
    output_key="proposed_trading_strategies_output",
)
