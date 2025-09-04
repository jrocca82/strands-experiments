from strands.hooks import BeforeInvocationEvent
from strands.agent import Agent
from my_env import model_id

agent = Agent(model=model_id)

# Register individual callbacks
def my_callback(event: BeforeInvocationEvent) -> None:
    print("Custom callback triggered")

agent.hooks.add_callback(BeforeInvocationEvent, my_callback)

# Trigger it
agent("Hello!")  # or any non-empty text
