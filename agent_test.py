import asyncio
from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP

load_dotenv()

mcp_server_url = 'http://localhost:8001/mcp'
server_connector = MCPServerStreamableHTTP(url=mcp_server_url)

agent = Agent(
    "openai:gpt-4o-mini",
    instructions="You are a restaurant assistant. Use your tools to answer questions about the menu.",
    mcp_servers=[server_connector]
)

async def main():
    print("▶️  Starting direct agent run...")
    try:
        async with agent.run_mcp_servers():
            print("✅ MCP server connection context is active.")
            print("▶️  Running agent with a user prompt...")
            
            result = await agent.run("How much does Tiramisu cost?")
            
            print("\n" + "="*50)
            print("✅ Agent run finished!")
            print(f"   Final Output: {result.output}")
            print("="*50)

    except Exception as e:
        print(f"\n❌ An error occurred during the agent run: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())