from mcp.client.sse import sse_client
from strands import Agent
from strands.tools.mcp import MCPClient
from my_env import model_id

# Connect to an MCP server using SSE transport
sse_mcp_client = MCPClient(lambda: sse_client("http://localhost:8000/sse"))

# Create an agent with MCP tools
with sse_mcp_client:
    # Get the tools from the MCP server
    tools = sse_mcp_client.list_tools_sync()

    # Create an agent with these tools
    agent = Agent(tools=tools, model=model_id)
    
    # Must be called inside with statement
    agent("Hello, what is 7 + 8?")
    
