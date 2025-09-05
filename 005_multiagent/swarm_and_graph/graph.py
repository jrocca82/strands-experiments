import logging
from strands import Agent
from strands.multiagent import GraphBuilder
from my_env import model_id

# Enable debug logs and print them to stderr
logging.getLogger("strands.multiagent").setLevel(logging.DEBUG)
logging.basicConfig(
    format="%(levelname)s | %(name)s | %(message)s",
    handlers=[logging.StreamHandler()]
)

# Create specialized agents
researcher = Agent(name="researcher", system_prompt="You are a research specialist...", model=model_id)
analyst = Agent(name="analyst", system_prompt="You are a data analysis specialist...", model=model_id)
fact_checker = Agent(name="fact_checker", system_prompt="You are a fact checking specialist...", model=model_id)
report_writer = Agent(name="report_writer", system_prompt="You are a report writing specialist...", model=model_id)

# Build the graph
builder = GraphBuilder()

# Add nodes
builder.add_node(researcher, "research")
builder.add_node(analyst, "analysis")
builder.add_node(fact_checker, "fact_check")
builder.add_node(report_writer, "report")

# Add edges (dependencies)
builder.add_edge("research", "analysis")
builder.add_edge("research", "fact_check")
builder.add_edge("analysis", "report")
builder.add_edge("fact_check", "report")

# Set entry points (optional - will be auto-detected if not specified)
builder.set_entry_point("research")

# Build the graph
graph = builder.build()

# Execute the graph on a task
result = graph("Research the impact of AI on healthcare and create a comprehensive report")

# Access the results
print(f"\nStatus: {result.status}")
print(f"Execution order: {[node.node_id for node in result.execution_order]}")