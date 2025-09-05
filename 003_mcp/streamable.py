from mcp.client.streamable_http import streamablehttp_client
from strands import Agent
from strands.tools.mcp.mcp_client import MCPClient
from my_env import model_id

BASE_URL = "http://127.0.0.1:8000/mcp"

streamable_http_mcp_client = MCPClient(lambda: streamablehttp_client(BASE_URL))


# Create an agent with MCP tools
with streamable_http_mcp_client:
    # Get the tools from the MCP server
    tools = streamable_http_mcp_client.list_tools_sync()

    # Create an agent with these tools
    agent = Agent(tools=tools, model=model_id)
    
    agent("Hello, what is 2.54344343 + 5.6546423432")