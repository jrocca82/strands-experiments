import asyncio
from strands import Agent
from strands_tools import use_agent, memory
from mcp.client.streamable_http import streamablehttp_client
from my_env import model_id
import os

# KB setup
os.environ["STRANDS_KNOWLEDGE_BASE_ID"] = "OZKALKOPD6"

# Prompts
ACTION_SYSTEM_PROMPT = """
You are a knowledge base assistant focusing ONLY on classifying user queries.
Reply with EXACTLY ONE WORD - either "store" or "retrieve".
"""

ANSWER_SYSTEM_PROMPT = """
You are a helpful knowledge assistant that provides clear answers 
based on information retrieved from a knowledge base.
"""

def extract_agent_text(agent_response):
    """Extract text content from agent/use_agent response dict."""
    if isinstance(agent_response, dict) and agent_response.get("content"):
        return agent_response["content"][0]["text"].strip()
    return str(agent_response)

async def run_dynamic_agent(query):
    """Run a single agent that can use KB/memory, MCP tools, and LLM fallback."""
    BASE_URL = "http://localhost:8000/stream"

    # Open async transport directly
    async with streamablehttp_client(BASE_URL) as (read_stream, write_stream, _):
        print("[MCP] Session initialized!")

        agent = Agent(tools=[memory, use_agent], model=model_id)

        response = agent(query)  # synchronous call
        text = extract_agent_text(response)
        print("\n[Agent Response]\n", text)

async def main():
    print("\n🧠 Multi-Tool Agent 🧠")
    print("This agent uses KB/memory, MCP tools (via streamable_http), then generic LLM fallback.\n")

    while True:
        user_input = input("> ").strip()
        if user_input.lower() in ["exit", "quit"]:
            break
        if not user_input:
            continue

        print("Processing...")
        await run_dynamic_agent(user_input)


if __name__ == "__main__":
    asyncio.run(main())
