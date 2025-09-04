from strands import Agent
from strands_tools import calculator

# Initialize the agent with tools, model, and configuration
agent = Agent(
    tools=[calculator],
    system_prompt="You are a helpful assistant."
)