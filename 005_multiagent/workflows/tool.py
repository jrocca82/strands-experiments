# NOTE: BROKEN AF, models dead

from strands import Agent
from strands_tools import workflow
from my_env import model_id  # "amazon.nova-lite-v1:0"

agent = Agent(tools=[workflow], model=model_id)

# clean slate (optional but recommended)
agent.tool.workflow(action="status", workflow_id="data_analysis")

nova_cfg = {
    "provider": "bedrock",
    "model_id": model_id,          # "amazon.nova-lite-v1:0"
    "region": "ap-southeast-2"               # "ap-southeast-2"
}

print(agent.model)

agent.tool.workflow(
    action="create",
    workflow_id="data_analysis",
    tasks=[
        {
            "task_id": "data_extraction",
            "description": "Extract key financial data from the quarterly report",
            "system_prompt": "You extract and structure financial data from reports.",
            "priority": 5,
            "model": nova_cfg,          # <-- use model_id
        },
        {
            "task_id": "trend_analysis",
            "description": "Analyze trends in the data compared to previous quarters",
            "dependencies": ["data_extraction"],
            "system_prompt": "You identify trends in financial time series.",
            "priority": 3,
            "model": nova_cfg,          # <-- use model_id
        },
        {
            "task_id": "report_generation",
            "description": "Generate a comprehensive analysis report",
            "dependencies": ["trend_analysis"],
            "system_prompt": "You create clear financial analysis reports.",
            "priority": 2,
            "model": nova_cfg,          # <-- use model_id
        },
    ],
)
agent.tool.workflow(action="start", workflow_id="data_analysis")
print(agent.tool.workflow(action="status", workflow_id="data_analysis"))
