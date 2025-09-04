from strands import Agent
from strands.session.s3_session_manager import S3SessionManager
import boto3
from my_env import model_id

# Optional: Create a custom boto3 session
boto_session = boto3.Session(region_name="ap-southeast-2")

# Create a session manager that stores data in S3
session_manager = S3SessionManager(
    session_id="user-456",
    bucket="test-agent-storage",
    prefix="production/",  # Optional key prefix
    boto_session=boto_session,  # Optional boto3 session
    region_name="ap-southeast-2"  # Optional AWS region (if boto_session not provided)
)

# Create an agent with the session manager
agent = Agent(session_manager=session_manager, model=model_id)

# Use the agent normally - state and messages will be persisted to S3
agent("My name is Jo and I am a llama")
agent("I am a llama and I like drama")