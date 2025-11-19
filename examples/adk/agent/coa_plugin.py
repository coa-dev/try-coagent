import time

from typing import Any

from coa_dev_coagent import CoagentClient
from google.adk.agents.base_agent import BaseAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.invocation_context import InvocationContext
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
        # Keep backward-compatible alias used by logging helpers
        self.client = coa

        # Counters
        self.agent_count: int = 0
        self.llm_request_count: int = 0
        self.llm_response_count: int = 0
        self.error_count: int = 0
        self.turn_number: dict[str, int] = {}
        self.prompt_number: dict[str, int] = {}

        # Track request start times to compute durations
        self.request_start_times: dict[str, float] = {}

    async def before_agent_callback(
        self, *, agent: BaseAgent, callback_context: CallbackContext
    ) -> None:
        session = callback_context.session.id
        try:
            self.agent_count += 1
            print(f"[Plugin] Before agent callback #{self.agent_count} for agent: {agent.name}")

            # Increment turn number for new agent interaction
            self._get_turn_number(session, increment=True)
        except Exception as e:
            print(f"[Plugin] Error in before_agent_callback: {e}")
            await self._log_error(session, f"before_agent_callback error: {e}")

    async def before_model_callback(
        self, *, callback_context: CallbackContext, llm_request: LlmRequest
    ) -> None:
        session = callback_context.session.id
        try:
            self.llm_request_count += 1
            request_id = f"req_{self.llm_request_count}"
            self.request_start_times[request_id] = time.time()
            print(f"[Plugin] Before model callback #{self.llm_request_count} for model: {llm_request.model}")

            if hasattr(callback_context, 'metadata'):
                callback_context.metadata = callback_context.metadata or {}
                callback_context.metadata['request_id'] = request_id

            # Extract prompt primarily from LlmRequest.contents (list[types.Content])
            prompt = ""
            try:
                contents = getattr(llm_request, "contents", None)
                prompt = self._extract_text_from_contents(contents)
                if not prompt:
                    # Secondary fallbacks if some other field is used
                    if hasattr(llm_request, "prompt") and llm_request.prompt:
                        prompt = str(llm_request.prompt)
                    elif hasattr(llm_request, "input") and llm_request.input:
                        prompt = str(llm_request.input)
            except Exception:
                # Fall back to stringifying the request
                try:
                    prompt = str(llm_request)
                except Exception:
                    prompt = ""

            agent_name = callback_context.agent_name
            # Mirror smolagents: log raw LLM call details early
            try:
                self.client.log_llm_call_new(
                    session_id=session,
                    issuer=agent_name or "unknown-agent",
                    prompt=prompt,
                    prompt_number=self._get_prompt_number(session),
                    turn_number=self._get_turn_number(session),
                )
            except Exception as e:
                print(f"[Plugin] Failed to log LLM call: {e}")

        except Exception as e:
            print(f"[Plugin] Error in before_model_callback: {e}")
            await self._log_error(session, f"before_model_callback error: {e}")

    async def after_model_callback(
        self, *, callback_context: CallbackContext, llm_response: LlmResponse
    ) -> None:
        session = callback_context.session.id
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
            await self._log_llm_response(session,llm_response, duration_ms)

        except Exception as e:
            print(f"[Plugin] Error in after_model_callback: {e}")
            await self._log_error(session, f"after_model_callback error: {e}")

    async def on_error_callback(
        self, *, callback_context: CallbackContext, error: Exception
    ) -> None:
        """Handle errors during agent execution."""
        try:
            session = callback_context.session.id 
            print(f"[Plugin] Error callback triggered: {error}")
            await self._log_error(session, str(error))

        except Exception as e:
            print(f"[Plugin] Error in on_error_callback: {e}")

    async def after_agent_callback(
        self, *, agent: BaseAgent, callback_context: CallbackContext
    ) -> None:
        """Handle agent completion - potential run end."""
        session_id = callback_context.session.id
        try:
            print(f"[Plugin] After agent callback for agent: {agent.name}")
            result = getattr(callback_context, 'result', None)

            if self._is_final_answer(result, callback_context):
                await self._log_run_end(session_id, result, agent.name)

        except Exception as e:
            print(f"[Plugin] Error in after_agent_callback: {e}")
            await self._log_error(session_id, f"after_agent_callback error: {e}")

    async def on_user_message_callback(
        self,
        *,
        invocation_context: InvocationContext,
        user_message: Any,
    ) -> None:
        try:
            session_id = invocation_context.session.id

            # Extract plain text from the Content parts
            prompt_text = ""
            try:
                if hasattr(user_message, "parts"):
                    prompt_text = "\n".join(
                        [
                            getattr(p, "text", "")
                            for p in user_message.parts
                            if hasattr(p, "text") and getattr(p, "text")
                        ]
                    )
                if not prompt_text:
                    prompt_text = str(user_message)
            except Exception:
                prompt_text = str(user_message)

            # Determine if this is the very first prompt/turn for the session
            current_prompt = self._get_prompt_number(session_id, True)
            current_turn = self._get_turn_number(session_id)

            if current_prompt <= 1 and current_turn == 0:
                self.client.log_session_start(
                    session_id=session_id,
                    prompt=prompt_text,
                    prompt_number=current_prompt,
                    turn_number=current_turn,
                )
                print(f"[Plugin] Logged session start for {session_id}")
            try:
                self.client.log_user_input(
                session_id=session_id,
                prompt=prompt_text,
                prompt_number=current_prompt,
                turn_number=current_turn,
                )
                print(f"[Plugin] Logged user input (prompt #{current_prompt})")
            except Exception as e:
                print(f"[Plugin] Failed to log user input: {e}")

        except Exception as e:
            # Ensure errors here don't break the agent flow
            print(f"[Plugin] Error in on_user_message_callback: {e}")
            try:
                await self._log_error(invocation_context.session.id, f"on_user_message_callback error: {e}")
            except Exception:
                pass

        # No modification of the user message
        return None
    def _is_final_answer(self, result: Any, callback_context: CallbackContext) -> bool:
        """Determine if this is a final answer."""

        if hasattr(result, 'is_final'):
            return result.is_final

        if hasattr(callback_context, 'is_final_response'):
            return callback_context.is_final_response

        return False

    def _get_turn_number(self, session_id: str, increment: bool = False) -> int:
        """Get the current turn number, optionally incrementing it.

        Args:
            increment: When True, increments the internal counter before returning.

        Returns:
            The current turn number after optional increment.
        """
        if self.turn_number.get(session_id) is None:
            self.turn_number[session_id] = 0
        if increment:
            self.turn_number[session_id] += 1
        return self.turn_number[session_id]

    def _get_prompt_number(self, session_id: str, increment: bool = False) -> int:
        """Get the current prompt number, optionally incrementing it."""
        if self.prompt_number.get(session_id) is None:
            self.prompt_number[session_id] = 0
        if increment:
            self.prompt_number[session_id] += 1
        return self.prompt_number[session_id]

    async def _log_error(self, session_id: str, error_message: str) -> None:
        """Log error to CoAgent."""
        try:
            self.error_count += 1
            self.client.log_error(
                session_id=session_id,
                prompt_number=self._get_prompt_number(session_id),
                turn_number=self._get_turn_number(session_id, True),
                error_message=error_message,
            )
            print(f"[Plugin] Logged error #{self.error_count}: {error_message}")
        except Exception as e:
            print(f"[Plugin] Failed to log error: {e}")

    async def _log_llm_response(self, session_id: str, llm_response: LlmResponse, duration_ms: int = 0) -> None:
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
                session_id=session_id,
                response=response_text,
                prompt_number=self._get_prompt_number(session_id),
                turn_number=self._get_turn_number(session_id, True),
                total_tokens=total_tokens,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
            )
            print(f"[Plugin] Logged LLM response #{self.llm_response_count}")
        except Exception as e:
            print(f"[Plugin] Failed to log LLM response: {e}")

    async def _log_run_end(self, session_id: str, result: Any, agent_name: str) -> None:
        """Log run end to CoAgent."""
        try:
            final_response = ""
            if hasattr(result, 'text'):
                final_response = result.text
            elif hasattr(result, 'content'):
                final_response = str(result.content)
            else:
                final_response = str(result)

            # TODO(leoborai) - Calculate actual elapsed time, we should decide
            # wether to track per agent or overall
            self.client.log_session_end(
                session_id=session_id,
                response=final_response,
                prompt_number=self._get_prompt_number(session_id),
                turn_number=self._get_turn_number(session_id,True),
                elapsed_time_ms=1000,
            )

            print(f"[Plugin] Logged run end for agent: {agent_name}")
        except Exception as e:
            print(f"[Plugin] Failed to log run end: {e}")

    def _extract_text_from_contents(self, contents: Any) -> str:
        """Extract joined text from a list of google.genai types.Content-like objects.

        Handles shapes where each content has a `.parts` iterable of objects that may
        include a `.text` attribute. Falls back gracefully.
        """
        try:
            if not contents:
                return ""
            collected: list[str] = []
            for c in contents:
                # Prefer render_as_markdown if available for richer prompts
                if hasattr(c, "render_as_markdown"):
                    try:
                        collected.append(c.render_as_markdown())
                        continue
                    except Exception:
                        pass

                parts = getattr(c, "parts", None)
                if parts:
                    for p in parts:
                        t = getattr(p, "text", None)
                        if t:
                            collected.append(str(t))
            if collected:
                return "\n".join(collected)
        except Exception:
            pass
        try:
            # Last resort
            return "\n".join(str(c) for c in (contents or []))
        except Exception:
            return ""
