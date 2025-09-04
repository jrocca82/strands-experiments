from strands import Agent
from strands.agent.conversation_manager import SummarizingConversationManager
from strands.models import BedrockModel
from my_env import model_id

# Create a cheaper, faster model for summarization tasks
summarization_model = BedrockModel(
    model_id="claude-3-5-haiku-20241022",  # More cost-effective for summarization
    max_tokens=1000,
    params={"temperature": 0.1}  # Low temperature for consistent summaries
)
custom_summarization_agent = Agent(model=summarization_model)

conversation_manager = SummarizingConversationManager(
    summary_ratio=0.4,
    preserve_recent_messages=3,
    summarization_agent=custom_summarization_agent
)

agent = Agent(
    conversation_manager=conversation_manager,
    model=model_id
)

# Example script to demo summarization
messages = [
    "Hey, can you help me plan my week?",
    "I need to finish a report, go to two doctor appointments, and prep for a meeting.",
    "I also want to find time for the gym three times this week.",
    "That works! Let's put them on Monday, Wednesday, and Friday.",
    "Yes, I also want to cook at home at least twice.",
]

# Send each message to the agent
for msg in messages:
    response = agent(msg)
    print(f"User: {msg}")
    print(f"Assistant: {response}\n")

print("==== Conversation Summary ====")
print(agent.messages)  # Shows all messages exchanged so far
