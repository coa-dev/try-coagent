from turtledemo.chaos import N
import os

from dotenv import load_dotenv
from google.adk.agents import Agent

from .order_processing_tool import order_processing_tool

load_dotenv()

openai_api_key = os.environ.get("OPENAI_API_KEY")
openai_model = os.environ.get("MODEL_GPT_4O")

if openai_api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable not set")

root_agent = Agent(
    name='order_processing_agent',
    instruction="Help the user with creating orders, leverage the tools you have access to",
    tools=[order_processing_tool],
)
