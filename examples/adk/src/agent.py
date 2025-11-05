"""Financial coordinator: provide reasonable investment strategies."""

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import prompt
from .config import get_litellm_model
from .coa_plugin import CoaPlugin
from .sub_agents.data_analyst import data_analyst_agent
from .sub_agents.execution_analyst import execution_analyst_agent
from .sub_agents.risk_analyst import risk_analyst_agent
from .sub_agents.trading_analyst import trading_analyst_agent
from src import root_agent

load_dotenv()

def get_root_agent() -> LlmAgent:
    return LlmAgent(
        model=get_litellm_model(),
        name="financial_coordinator",
        description=(
            "guide users through a structured process to receive financial "
            "advice by orchestrating a series of expert subagents. help them "
            "analyze a market ticker, develop trading strategies, define "
            "execution plans, and evaluate the overall risk."
        ),
        instruction=prompt.FINANCIAL_COORDINATOR_PROMPT,
        output_key="financial_coordinator_output",
        tools=[
            AgentTool(agent=data_analyst_agent),
            AgentTool(agent=trading_analyst_agent),
            AgentTool(agent=execution_analyst_agent),
            AgentTool(agent=risk_analyst_agent),
        ],
    )

root_agent = get_root_agent()
