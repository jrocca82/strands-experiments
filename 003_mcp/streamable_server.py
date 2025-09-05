from mcp.server import FastMCP

# Create an MCP server
mcp = FastMCP("Calculator Server")

@mcp.tool(description="Calculator tool which performs calculations")
def calculator(x: int, y: int) -> int:
    return x + y

# Change depending on file running
mcp.run(transport="streamable-http")