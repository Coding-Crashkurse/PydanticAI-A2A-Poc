import uvicorn
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP

MCP_SERVER_URL = "http://localhost:8001/mcp"

mcp_connector = MCPServerStreamableHTTP(url=MCP_SERVER_URL, tool_prefix="menu")

load_dotenv()

agent = Agent(
    "openai:gpt-4o-mini",
    instructions=(
        "You are a friendly and helpful restaurant assistant. "
        "Your main job is to answer questions about the menu by using your available tools. "
        "For example, to search for appetizers, you would call the tool 'menu_get_menu_items' with category 'Appetizer'. "
        "You can also tell a short, witty joke if the user asks for one."
    ),
    mcp_servers=[mcp_connector]
)

app = agent.to_a2a(
    name="PydanticAI Restaurant Agent",
    description="An agent that can answer questions about the menu by calling its remote tool service.",
    url="http://localhost:7000"
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7000)
