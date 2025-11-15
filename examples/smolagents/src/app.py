import os
import json

from dotenv import load_dotenv
from smolagents import CodeAgent, OpenAIModel, MemoryStep, MultiStepAgent, ActionStep
from Gradio_UI import GradioUI

from coa_dev_coagent import CoagentClient
from coa_dev_coagent.logapi import create_tool_call_log, create_tool_response_log

from tools.flight_search import FlightSearchTool
from tools.final_answer import FinalAnswerTool

from counters import get_session_id, get_prompt_number, get_turn_number

load_dotenv()

llm_model = os.environ.get("LLM_MODEL")
llm_api_key = os.environ.get("LLM_API_KEY")
llm_api_base = os.environ.get("LLM_API_BASE")

if not llm_model or not llm_api_key:
    raise ValueError("LLM_MODEL and LLM_API_KEY must be set in the environment variables.")

client = CoagentClient()

# Callbacks used to log CoAgent
def logging_step_callback(
    step: MemoryStep,
    agent: MultiStepAgent
):
    match step:
        case ActionStep():
            # Log raw LLM call early (prompt + model output) if we have input messages
            if step.model_input_messages:
                try:
                    # Original simple join approach, but use render_as_markdown when available.
                    prompt = "\n".join(
                        (
                            msg.render_as_markdown()  # preferred rich text
                            if hasattr(msg, "render_as_markdown")
                            else str(getattr(msg, "content", ""))
                        )
                        for msg in step.model_input_messages
                        if hasattr(msg, "content") or hasattr(msg, "render_as_markdown")
                    )
                    client.log_llm_call(
                        run_id=get_session_id(),
                        context_name=agent.name,
                        prompt=prompt,
                        response=step.model_output if step.model_output else "",
                        purpose="step_generation",
                        meta={
                            "step_number": step.step_number,
                            "tool_calls": [tc.name for tc in step.tool_calls] if step.tool_calls else [],
                            "is_final_answer": step.is_final_answer,
                        },
                    )
                except Exception as e:
                    print(f"Failed to log LLM call: {e}")

            try:
                # Lock counters for this step so multiple logs share the same numbers
                pn = get_prompt_number(True)
                tn = get_turn_number(True)

                if step.error is not None:
                    client.log_error(
                        session_id=get_session_id(),
                        prompt_number=pn,
                        turn_number=tn,
                        error_message=str(step.error),
                    )

                if step.model_output:
                    input_tokens = getattr(step.token_usage, "input_tokens", None)
                    output_tokens = getattr(step.token_usage, "output_tokens", None)
                    total_tokens = getattr(step.token_usage, "total_tokens", None)
                    client.log_llm_response(
                        session_id=get_session_id(),
                        response=step.model_output,
                        prompt_number=pn,
                        turn_number=tn,
                        total_tokens=total_tokens,
                        input_tokens=input_tokens,
                        output_tokens=output_tokens,
                    )

                if step.tool_calls and create_tool_call_log is not None:
                    for tc in step.tool_calls:
                        try:
                            client.store_log(
                                create_tool_call_log(
                                    session_id=get_session_id(),
                                    prompt_number=pn,
                                    turn_number=tn,
                                    tool_name=tc.name,
                                    parameters=tc.arguments,
                                )
                            )
                        except Exception as e:
                            print(f"Failed to log tool call {getattr(tc, 'name', 'unknown')}: {e}")

                if (step.observations is not None or step.action_output is not None):
                    result_payload = {}
                    if step.action_output is not None:
                        result_payload["action_output"] = step.action_output
                    if step.observations is not None:
                        result_payload["observations"] = step.observations

                    first_tool_name = None
                    first_params = None
                    if step.tool_calls:
                        first_tool_name = step.tool_calls[0].name
                        first_params = step.tool_calls[0].arguments

                    exec_time_ms = None
                    try:
                        if step.timing is not None and getattr(step.timing, "duration", None) is not None:
                            exec_time_ms = int(step.timing.duration * 1000)
                    except Exception:
                        exec_time_ms = None

                    try:
                        client.store_log(
                            create_tool_response_log(
                                session_id=get_session_id(),
                                prompt_number=pn,
                                turn_number=tn,
                                tool_name=first_tool_name,
                                parameters=first_params,
                                result=result_payload,
                                success=step.error is None,
                                error_message=str(step.error) if step.error else None,
                                execution_time_ms=exec_time_ms,
                            )
                        )
                    except Exception as e:
                        print(f"Failed to log tool response: {e}")

                if step.is_final_answer:
                    final_elapsed_ms = None
                    try:
                        if step.timing is not None and getattr(step.timing, "duration", None) is not None:
                            final_elapsed_ms = int(step.timing.duration * 1000)
                    except Exception:
                        final_elapsed_ms = None

                    client.log_session_end(
                        session_id=get_session_id(),
                        response=step.model_output,
                        prompt_number=pn,
                        turn_number=tn,
                        elapsed_time_ms=final_elapsed_ms,
                    )
            except Exception as e:
                print(f"Failed to log action step: {e}")
            return
        case _:
            print(f"[{agent.name}] {step}")

model = OpenAIModel(
    model_id=llm_model,
    api_key=llm_api_key,
    api_base=llm_api_base
)

transportation_agent = CodeAgent(
    name="transportation_agent",
    description="You are a travel agent that specializes in booking transportation",
    model=model,
    tools=[
        FlightSearchTool(),
    ],
    step_callbacks=[
        logging_step_callback,
    ],
)

agent = CodeAgent(
    name="manager_agent",
    description="""You are a travel agent that manages a team of specialized travel agents to create comprehensive travel itineraries.
        Your responsibilities are:
            - Orchestrates other agents
            - Resolves conflicts between recommendations
            - Maintains conversation context
            - Learns user preferences
            - Generates final itinerary""",
    tools=[FinalAnswerTool()],
    model=model,
    managed_agents=[
        transportation_agent,
    ],
    step_callbacks=[
        logging_step_callback,
    ],
)

GradioUI(agent).launch(server_name="0.0.0.0")
