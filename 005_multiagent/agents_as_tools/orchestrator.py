from strands import Agent
from tools import (
    research_assistant,
    product_recommendation_assistant,
    trip_planning_assistant,
)

from my_env import model_id

# Define the orchestrator system prompt with clear tool selection guidance
MAIN_SYSTEM_PROMPT = """
You are an assistant that routes queries to specialized agents:
- For research questions and factual information → Use the research_assistant tool
- For product recommendations and shopping advice → Use the product_recommendation_assistant tool
- For travel planning and itineraries → Use the trip_planning_assistant tool
- For simple questions not requiring specialized knowledge → Answer directly

Always select the most appropriate tool based on the user's query.
"""

# Strands Agents SDK allows easy integration of agent tools
orchestrator = Agent(
    system_prompt=MAIN_SYSTEM_PROMPT,
    callback_handler=None,
    tools=[research_assistant, product_recommendation_assistant, trip_planning_assistant],
    model=model_id
)

customer_query = "I'm looking for hiking boots for a trip to Patagonia next month"

# The orchestrator automatically determines that this requires multiple specialized agents
response = orchestrator(customer_query)