from strands import Agent
from my_env import model_id

agent = Agent(model=model_id)

# Send a message and get a response
agent("Hello!")

# Access the conversation history
print("\n")
print(agent.messages)  # Shows all messages exchanged so far
