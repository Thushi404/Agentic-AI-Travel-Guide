import sys
import os

# Move project directory to end of sys.path so the installed `mcp` package
# is found before the local mcp/ folder, which would otherwise shadow it.
_project_dir = os.path.dirname(os.path.abspath(__file__))                     # fix the python import path.
if _project_dir in sys.path:
    sys.path.remove(_project_dir)
sys.path.append(_project_dir)

import asyncio                                                       # used for asynchronous programming , langgraph and mcp use async functions.
import uuid                                                          # generates unique conversation id.
from langchain_core.messages import HumanMessage                     # Converts the user's text into a LangChain message.
from langchain_mcp_adapters.client import MultiServerMCPClient       # Creates an MCP client that communicates with MCP servers.
from graph.graph import build_graph                                  # imports the langgraph workflow.


MCP_CONFIG = {                                                      # this tells the application how to connect the mcp server.
    "travel": {
        "command": "python",
        "args": ["mcp/server.py"],
        "transport": "stdio",
    }
}

 
async def main():                                                   # main function of the application.
    mcp_client = MultiServerMCPClient(MCP_CONFIG)
    tools = await mcp_client.get_tools()                            # loads all registered tools.
    graph = build_graph(tools)                                      # build langgraph.

    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    print("Travel Agent (LangGraph + MCP)")                               # display startup messages.
    print("Type 'quit' to exit | 'clear' to start a new session\n")

    while True:                                                      # start chat loop and keeps the chatbot running continuously.
        try:
            user_input = input("You: ").strip()                     # Reads what the user types. 
        except (KeyboardInterrupt, EOFError):                      # Handle keyboard interruption
            print("\nGoodbye!")
            break

        if not user_input:                                       # ignore empty input.
            continue

        if user_input.lower() in ("quit", "exit", "q"):          # exit command to stop the chatbot.(quit, exit or q)
            print("Goodbye!")
            break

        if user_input.lower() == "clear":                              # clear conversation history and start a new session.
            thread_id = str(uuid.uuid4())                              # creates a new conversation id.
            config = {"configurable": {"thread_id": thread_id}}
            print("Session cleared. Starting a new conversation.\n")
            continue

        result = await graph.ainvoke(                              # send message to langgraph.
            {"messages": [HumanMessage(content=user_input)]},
            config=config,
        )

        last_message = result["messages"][-1]
        print(f"\nAssistant: {last_message.content}\n")                 # print response.


if __name__ == "__main__":                               # run the application.
    asyncio.run(main())                                  # start the main function in an asynchronous event loop.
