from my_env import model_id

from strands import Agent
from strands.session.file_session_manager import FileSessionManager

# Create a session manager with a unique session ID
session_manager = FileSessionManager(session_id="test-session")

# Create an agent with the session manager
agent = Agent(session_manager=session_manager, model=model_id)

# Use the agent - all messages and state are automatically persisted
agent("What is my name")  # This conversation is persisted