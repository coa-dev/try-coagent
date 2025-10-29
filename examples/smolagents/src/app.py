from dotenv import load_dotenv
from smolagents import CodeAgent, InferenceClientModel, DuckDuckGoSearchTool
from Gradio_UI import GradioUI

load_dotenv()

model = InferenceClientModel()
agent = CodeAgent(
    tools=[],
    model=model,
)

GradioUI(agent).launch(server_name="0.0.0.0")
