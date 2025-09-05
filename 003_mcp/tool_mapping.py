import base64
from mcp import stdio_client, StdioServerParameters
from mcp.client.sse import sse_client
from strands import Agent
from strands.tools.mcp import MCPClient
import mcp.types as types
from my_env import model_id

# ---------------------------
# Helper: map MIME type to image format
# ---------------------------
def map_mime_type_to_image_format(mime_type: str) -> str:
    """Map a MIME type to a simpler image format string."""
    mapping = {
        "image/png": "png",
        "image/jpeg": "jpeg",
        "image/jpg": "jpeg",
        "image/gif": "gif",
        "image/webp": "webp",
    }
    return mapping.get(mime_type, "unknown")

# ---------------------------
# Helper: convert MCP content
# ---------------------------
def _map_mcp_content_to_tool_result_content(content):
    if isinstance(content, types.TextContent):
        return {"text": content.text}
    elif isinstance(content, types.ImageContent):
        return {
            "image": {
                "format": map_mime_type_to_image_format(content.mimeType),
                "source": {"bytes": base64.b64decode(content.data)},
            }
        }
    else:
        # Unsupported content type
        return None

# ---------------------------
# Connect to multiple MCP servers
# ---------------------------
sse_mcp_client = MCPClient(lambda: sse_client("http://localhost:8000/sse"))
stdio_mcp_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(
        command="uvx",
        args=["awslabs.aws-documentation-mcp-server@latest"]
    )
))

# ---------------------------
# Combine tools and use agent
# ---------------------------
with sse_mcp_client, stdio_mcp_client:
    tools = sse_mcp_client.list_tools_sync() + stdio_mcp_client.list_tools_sync()

    agent = Agent(tools=tools, model=model_id)
    
    agent("Show me the image")
