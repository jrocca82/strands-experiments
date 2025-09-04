from strands import Agent
from my_env import model_id

# Create an agent with initial messages
agent = Agent(messages=[
    {"role": "user", "content": [{"text": "Hello, my name is Jo and I'm a llama!"}]},
    {"role": "assistant", "content": [{"text": "Hi there! How can I help you today?"}]}
], model=model_id)

# Continue the conversation
agent("What's am I?")