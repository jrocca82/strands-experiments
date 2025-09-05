# 003_mcp/image_server.py
import mcp.types as types
from mcp.server import FastMCP

# 1x1 transparent PNG (base64). Keeps the demo dependency-free.
PNG_1x1_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAusB9y0y8b8AAAAASUVORK5CYII="
)

mcp = FastMCP("Image Demo Server")

@mcp.tool(description="Healthcheck")
def ping():
    # MCP tools return a list of Content items
    return [types.TextContent(type="text", text="pong")]

@mcp.tool(description="Return a tiny 1x1 PNG image")
def tiny_png():
    return [types.ImageContent(type="image", mimeType="image/png", data=PNG_1x1_B64)]

if __name__ == "__main__":
    mcp.run(transport="sse")
