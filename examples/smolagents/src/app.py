import os

from dotenv import load_dotenv
from smolagents import CodeAgent, OpenAIModel
from Gradio_UI import GradioUI

from tools.flight_search import FlightSearchTool
from tools.final_answer import FinalAnswerTool

load_dotenv()

llm_model = os.environ.get("LLM_MODEL")
llm_api_key = os.environ.get("LLM_API_KEY")
llm_api_base = os.environ.get("LLM_API_BASE")

# Callbacks used to log CoAgent
def logging_step_callback(*args, **kwargs):
    print(f"Logging Step: {args} -- {kwargs}")

def final_answer_checks(*args, **kwargs):
    print(f"Final Answer: {args} -- {kwargs}")

def success_callback(*args, **kwargs):
    print(f"Success CB: {args} -- {kwargs}")

def failure_callback(*args, **kwargs):
    print(f"Failure CB: {args} -- {kwargs}")

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
        success_callback,
        failure_callback,
        final_answer_checks,
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
        success_callback,
        failure_callback,
        final_answer_checks,
    ],
)

GradioUI(agent).launch(server_name="0.0.0.0")
