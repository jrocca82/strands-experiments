from strands import Agent
from my_env import model_id

# Create specialized agents
researcher = Agent(system_prompt="You are a research specialist. Find key information.", callback_handler=None, model=model_id)
analyst = Agent(system_prompt="You analyze research data and extract insights.", callback_handler=None, model=model_id)
writer = Agent(system_prompt="You create polished reports based on analysis.", model=model_id)

# Sequential workflow processing
def process_workflow(topic):
    # Step 1: Research
    research_results = researcher(f"Research the latest developments in {topic}")

    # Step 2: Analysis
    analysis = analyst(f"Analyze these research findings: {research_results}")

    # Step 3: Report writing
    final_report = writer(f"Create a report based on this analysis: {analysis}")

    return final_report

process_workflow("endometriosis")