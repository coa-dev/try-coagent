import os

from dotenv import load_dotenv
from google.adk.agents import Agent

from .order_processing_tool import order_processing_tool

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
openai_model = os.environ.get("OPENAI_MODEL")

root_agent = Agent(
    model=openai_model,
    name='order_processing_agent',
    instruction="Help the user with creating orders, leverage the tools you have access to",
    tools=[order_processing_tool],
)
