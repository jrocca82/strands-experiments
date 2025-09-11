#!/usr/bin/env python3
from strands import Agent
from strands_tools import use_llm, memory
from mcp.client.sse import sse_client
from strands.tools.mcp import MCPClient
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

def extract_llm_text(llm_response):
    """Extract text content from agent/LLM response dict."""
    if isinstance(llm_response, dict) and llm_response.get("content"):
        return llm_response["content"][0]["text"].strip()
    return str(llm_response)

def run_dynamic_agent(query):
    with MCPClient(lambda: sse_client("http://localhost:8000/sse")) as sse_mcp_client:
        # Get MCP tools (calculator, etc.)
        mcp_tools = sse_mcp_client.list_tools_sync()
        
        # Single agent with all tools
        agent = Agent(tools=[memory, use_llm] + mcp_tools, model=model_id)
        
        # Let Strands route the query to the best tool automatically
        response = agent(query)
        text = extract_llm_text(response)
        print("\n[Agent Response]\n", text)

if __name__ == "__main__":
    print("\n🧠 Multi-Tool Agent 🧠")
    print("This agent uses KB, MCP tools (like calculator), then generic LLM fallback.\n")
    
    while True:
        user_input = input("> ").strip()
        if user_input.lower() in ["exit", "quit"]:
            break
        if not user_input:
            continue
        print("Processing...")
        run_dynamic_agent(user_input)
