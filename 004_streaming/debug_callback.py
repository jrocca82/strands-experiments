from strands import Agent
from strands_tools import calculator
from my_env import model_id

def debugger_callback_handler(**kwargs):
    # Print the values in kwargs so that we can see everything
    print(kwargs)

agent = Agent(
    tools=[calculator],
    callback_handler=debugger_callback_handler,
    model=model_id
)

agent("What is 922 + 5321")