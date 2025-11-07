from google.adk.agents.base_agent import BaseAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.plugins.base_plugin import BasePlugin

class CoaPlugin(BasePlugin):
    """CoAgent + ADK Agent Lifecycle Callback Integration."""

    def __init__(self) -> None:
        """Initialize the plugin with counters."""
        print("Initializing CoaPlugin...")
        super().__init__(name="coa_plugin")
        self.agent_count: int = 0
        self.tool_count: int = 0
        self.llm_request_count: int = 0

    async def before_agent_callback(
        self, *, agent: BaseAgent, callback_context: CallbackContext
    ) -> None:
        self.agent_count += 1
        print(f"[Plugin] Before agent callback for agent: {agent.name}")

    async def before_model_callback(
        self, *, callback_context: CallbackContext, llm_request: LlmRequest
    ) -> None:
        self.llm_request_count += 1
        print(f"[Plugin] Before model callback for model: {llm_request.model}")
