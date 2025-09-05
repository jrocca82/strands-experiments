import asyncio
from strands import Agent
from strands_tools import calculator
from my_env import model_id

# Initialize our agent without a callback handler
agent = Agent(
    tools=[calculator],
    callback_handler=None,
    model=model_id
)

# Async function that iterators over streamed agent events
async def process_streaming_response():
    agent_stream = agent.stream_async("Calculate 2+2")
    async for event in agent_stream:
        print(event)

# Run the agent
asyncio.run(process_streaming_response())