import os

from dotenv import load_dotenv
from smolagents import CodeAgent, OpenAIModel
from Gradio_UI import GradioUI

from tools.flight_search import FlightSearchTool

load_dotenv()

llm_model = os.environ.get("LLM_MODEL")
llm_api_key = os.environ.get("LLM_API_KEY")

model = OpenAIModel(
    model_id=llm_model,
    api_key=llm_api_key,
)

transportation_agent = CodeAgent(
    model=model,
    tools=[],
    name="Transportation Agent",
    system_prompt="""You are a travel agent that specializes in booking transportation for trips.
    Your responsibilities are:
        - Flight search and price comparison
        - Route optimization (multi-city trips)
        - Transportation between cities/airports
        - Ground transportation recommendations
        - Travel time calculations"""
)

agent = CodeAgent(
    tools=[FlightSearchTool()],
    model=model,
    managed_agents=[
        transportation_agent,
    ],
    system_prompt="""You are a travel agent that manages a team of specialized travel agents to create comprehensive travel itineraries.
       Your responsibilities are:
           - Orchestrates other agents
           - Resolves conflicts between recommendations
           - Maintains conversation context
           - Learns user preferences
           - Generates final itinerary"""
)

GradioUI(agent).launch(server_name="0.0.0.0")
