"""Risk Analysis Agent for providing the final risk evaluation"""

from google.adk import Agent

from agent.config import get_gemini_model

from . import prompt

MODEL="gemini-2.5-pro"

risk_analyst_agent = Agent(
    model=get_gemini_model(),
    name="risk_analyst_agent",
    instruction=prompt.RISK_ANALYST_PROMPT,
    output_key="final_risk_assessment_output",
)
