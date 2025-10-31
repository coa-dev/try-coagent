import os

from dotenv import load_dotenv
from smolagents import CodeAgent, OpenAIModel, MemoryStep, MultiStepAgent, ActionStep
from Gradio_UI import GradioUI

from coa_dev_coagent import CoagentClient

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
            try:
                if step.model_output:
                    client.log_llm_response(
                        session_id=get_session_id(),
                        response=step.model_output,
                        prompt_number=get_prompt_number(True),
                        turn_number=get_turn_number(True),
                        total_tokens=step.token_usage.total_tokens,
                        input_tokens=step.token_usage.input_tokens,
                        output_tokens=step.token_usage.output_tokens,
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
