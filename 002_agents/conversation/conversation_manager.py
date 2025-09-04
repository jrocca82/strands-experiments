from strands import Agent
from strands.agent.conversation_manager import SlidingWindowConversationManager
from my_env import model_id

# Create a conversation manager with custom window size
# By default, SlidingWindowConversationManager is used even if not specified
conversation_manager = SlidingWindowConversationManager(
    window_size=3,  # Maximum number of message pairs to keep
)

# Use the conversation manager with your agent
agent = Agent(conversation_manager=conversation_manager, model=model_id)

user_turns = [
    "Hey, I'm overwhelmed prepping a presentation for execs tomorrow.",
    "I'ts about our chatbot app—I'm worried the story isn't clear.",
    "The CTO wants architecture details, but the COO cares about business impact.",
]

# Simulate a multi-turn conversation
for i in range(0, len(user_turns)):
    user_message = f"{user_turns[i]}"
    print(f"\n🧑 You: {user_message}")
    response = agent(user_message)
    print(f"🤖 Agent: {response}")

    # Show the conversation window after each turn
    print("\n--- Conversation Window ---")
    for msg in agent.messages:
        print(f"{msg['role']}: {msg['content']}")