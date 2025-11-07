import time

from typing import Any

from coa_dev_coagent import CoagentClient
from google.adk.agents.base_agent import BaseAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.plugins.base_plugin import BasePlugin
from google.adk.models import LlmResponse

class CoaPlugin(BasePlugin):
    """CoAgent + ADK Agent Lifecycle Callback Integration."""

    def __init__(self, coa: CoagentClient) -> None:
        """Initialize the plugin with counters."""
        print("Initializing CoaPlugin...")
        super().__init__(name="coa_plugin")
        self.coa = coa

        # Counters
        self.agent_count: int = 0
        self.llm_request_count: int = 0
        self.llm_response_count: int = 0
        self.error_count: int = 0

        # Session tracking
        self.prompt_number: int = 0
        self.turn_number: int = 0

    async def before_agent_callback(
        self, *, agent: BaseAgent, callback_context: CallbackContext
    ) -> None:
        try:
            self.agent_count += 1
            print(f"[Plugin] Before agent callback #{self.agent_count} for agent: {agent.name}")

            # Increment turn number for new agent interaction
            self._get_turn_number(increment=True)

        except Exception as e:
            print(f"[Plugin] Error in before_agent_callback: {e}")
            await self._log_error(f"before_agent_callback error: {e}")

    async def before_model_callback(
        self, *, callback_context: CallbackContext, llm_request: LlmRequest
    ) -> None:
        try:
            self.llm_request_count += 1
            request_id = f"req_{self.llm_request_count}"
            self.request_start_times[request_id] = time.time()
            print(f"[Plugin] Before model callback #{self.llm_request_count} for model: {llm_request.model}")

            if hasattr(callback_context, 'metadata'):
                callback_context.metadata = callback_context.metadata or {}
                callback_context.metadata['request_id'] = request_id

        except Exception as e:
            print(f"[Plugin] Error in before_model_callback: {e}")
            await self._log_error(f"before_model_callback error: {e}")

    async def after_model_callback(
        self, *, callback_context: CallbackContext, llm_response: LlmResponse
    ) -> None:
        try:
            self.llm_response_count += 1

            request_id = None
            if hasattr(callback_context, 'metadata') and callback_context.metadata:
                request_id = callback_context.metadata.get('request_id')

            duration_ms = 0
            if request_id and request_id in self.request_start_times:
                duration_ms = int((time.time() - self.request_start_times[request_id]) * 1000)
                del self.request_start_times[request_id]

            print(f"[Plugin] After model callback #{self.llm_response_count}")
            await self._log_llm_response(llm_response, duration_ms)

        except Exception as e:
            print(f"[Plugin] Error in after_model_callback: {e}")
            await self._log_error(f"after_model_callback error: {e}")

    async def on_error_callback(
        self, *, callback_context: CallbackContext, error: Exception
    ) -> None:
        """Handle errors during agent execution."""
        try:
            print(f"[Plugin] Error callback triggered: {error}")
            await self._log_error(str(error))

        except Exception as e:
            print(f"[Plugin] Error in on_error_callback: {e}")

    async def after_agent_callback(
        self, *, agent: BaseAgent, callback_context: CallbackContext
    ) -> None:
        """Handle agent completion - potential run end."""
        try:
            print(f"[Plugin] After agent callback for agent: {agent.name}")
            result = getattr(callback_context, 'result', None)

            if self._is_final_answer(result, callback_context):
                await self._log_run_end(result, agent.name)

        except Exception as e:
            print(f"[Plugin] Error in after_agent_callback: {e}")
            await self._log_error(f"after_agent_callback error: {e}")

    def _is_final_answer(self, result: Any, callback_context: CallbackContext) -> bool:
        """Determine if this is a final answer."""

        if hasattr(result, 'is_final'):
            return result.is_final

        if hasattr(callback_context, 'is_final_response'):
            return callback_context.is_final_response

        return False

    async def _log_error(self, error_message: str) -> None:
        """Log error to CoAgent."""
        try:
            self.error_count += 1
            self.client.log_error(
                session_id=self._get_session_id(),
                prompt_number=self._get_prompt_number(True),
                turn_number=self._get_turn_number(True),
                error_message=error_message,
            )
            print(f"[Plugin] Logged error #{self.error_count}: {error_message}")
        except Exception as e:
            print(f"[Plugin] Failed to log error: {e}")

    async def _log_llm_response(self, llm_response: LlmResponse, duration_ms: int = 0) -> None:
        """Log LLM response to CoAgent."""
        try:
            total_tokens = getattr(llm_response, 'total_tokens', 0)
            input_tokens = getattr(llm_response, 'input_tokens', 0)
            output_tokens = getattr(llm_response, 'output_tokens', 0)

            response_text = ""
            if hasattr(llm_response, 'text'):
                response_text = llm_response.text
            elif hasattr(llm_response, 'content'):
                response_text = str(llm_response.content)

            self.client.log_llm_response(
                session_id=self._get_session_id(),
                response=response_text,
                prompt_number=self._get_prompt_number(True),
                turn_number=self._get_turn_number(True),
                total_tokens=total_tokens,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
            )
            print(f"[Plugin] Logged LLM response #{self.llm_response_count}")
        except Exception as e:
            print(f"[Plugin] Failed to log LLM response: {e}")

    async def _log_run_end(self, result: Any, agent_name: str) -> None:
        """Log run end to CoAgent."""
        try:
            final_response = ""
            if hasattr(result, 'text'):
                final_response = result.text
            elif hasattr(result, 'content'):
                final_response = str(result.content)
            else:
                final_response = str(result)

            run_id = f'run-{self._get_session_id()}-{self.agent_count}'

            # TODO(leoborai) - Calculate actual elapsed time, we should decide
            # wether to track per agent or overall
            self.client.log_run_end(
                run_id=run_id,
                response=final_response,
                elapsed_msec=1000,
            )
            print(f"[Plugin] Logged run end for agent: {agent_name}")
        except Exception as e:
            print(f"[Plugin] Failed to log run end: {e}")
