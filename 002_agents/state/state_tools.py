from strands import Agent, tool
from my_env import model_id

@tool
def track_user_action(action: str, agent: Agent):
    """Track user actions in agent state."""
    # Get current action count
    action_count = agent.state.get("action_count") or 0

    # Update state
    agent.state.set("action_count", action_count + 1)
    agent.state.set("last_action", action)

    return f"Action '{action}' recorded. Total actions: {action_count + 1}"

@tool
def get_user_stats(agent: Agent):
    """Get user statistics from agent state."""
    action_count = agent.state.get("action_count") or 0
    last_action = agent.state.get("last_action") or "none"

    return f"Actions performed: {action_count}, Last action: {last_action}"

# Create agent with tools
agent = Agent(tools=[track_user_action, get_user_stats], model=model_id)

# Use tools that modify and read state
agent("Track that I logged in")
agent("Track that I viewed my profile")
print("\n")
print(f"Actions taken: {agent.state.get('action_count')}")
print(f"Last action: {agent.state.get('last_action')}")