from mcp import stdio_client, StdioServerParameters
# from mcp.client.sse import sse_client
from mcp.client.streamable_http import streamablehttp_client
from strands import Agent
from strands.tools.mcp import MCPClient
from my_env import model_id

# Connect to multiple MCP servers
# sse_mcp_client = MCPClient(lambda: sse_client("http://localhost:8000/sse"))


BASE_URL = "http://127.0.0.1:8000/mcp"

streamable_http_mcp_client = MCPClient(lambda: streamablehttp_client(BASE_URL))


stdio_mcp_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(
        command="uvx", 
        args=["awslabs.aws-documentation-mcp-server@latest"]
    )
))

# Use servers together
with streamable_http_mcp_client, stdio_mcp_client:
    # Combine tools from both servers
    tools = streamable_http_mcp_client.list_tools_sync() + stdio_mcp_client.list_tools_sync()

    # Create an agent with all tools
    agent = Agent(tools=tools, model=model_id)
    
    agent("What is AWS Lambda and also tell me the answer to 12 + 56")