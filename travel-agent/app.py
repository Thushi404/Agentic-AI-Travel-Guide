import sys
import os

# Move project directory to end of sys.path so the installed `mcp` package
# is found before the local mcp/ folder, which would otherwise shadow it.
_project_dir = os.path.dirname(os.path.abspath(__file__))
if _project_dir in sys.path:
    sys.path.remove(_project_dir)
sys.path.append(_project_dir)

import asyncio
import uuid
from langchain_core.messages import HumanMessage
from langchain_mcp_adapters.client import MultiServerMCPClient
from graph.graph import build_graph


MCP_CONFIG = {
    "travel": {
        "command": "python",
        "args": ["mcp/server.py"],
        "transport": "stdio",
    }
}


async def main():
    mcp_client = MultiServerMCPClient(MCP_CONFIG)
    tools = await mcp_client.get_tools()
    graph = build_graph(tools)

    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    print("Travel Agent (LangGraph + MCP)")
    print("Type 'quit' to exit | 'clear' to start a new session\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        if user_input.lower() == "clear":
            thread_id = str(uuid.uuid4())
            config = {"configurable": {"thread_id": thread_id}}
            print("Session cleared. Starting a new conversation.\n")
            continue

        result = await graph.ainvoke(
            {"messages": [HumanMessage(content=user_input)]},
            config=config,
        )

        last_message = result["messages"][-1]
        print(f"\nAssistant: {last_message.content}\n")


if __name__ == "__main__":
    asyncio.run(main())
