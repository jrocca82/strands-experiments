from strands import Agent
from strands.multiagent import GraphBuilder, Swarm
from my_env import model_id

# Create a swarm of research agents
research_agents = [
    Agent(name="medical_researcher", system_prompt="You are a medical research specialist...", model=model_id),
    Agent(name="technology_researcher", system_prompt="You are a technology research specialist...", model=model_id),
    Agent(name="economic_researcher", system_prompt="You are an economic research specialist...", model=model_id)
]
research_swarm = Swarm(research_agents)

# Create a single agent node too
analyst = Agent(system_prompt="Analyze the provided research.", model=model_id)

# Create a graph with the swarm as a node
builder = GraphBuilder()
builder.add_node(research_swarm, "research_team")
builder.add_node(analyst, "analysis")
builder.add_edge("research_team", "analysis")

graph = builder.build()

result = graph("Research the impact of AI on healthcare and create a comprehensive report")

# Access the results
print(f"\n{result}")