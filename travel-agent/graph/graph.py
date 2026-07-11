from langgraph.graph import StateGraph, START            # creates the workflow graph and defines the starting point of the graph.
from langgraph.checkpoint.memory import MemorySaver      # allows chatbot to save the conversation history in memory.
from langgraph.prebuilt import tools_condition           # checks weather the AI wants to call a tool or not.
from graph.state import AgentState
from graph.nodes import create_nodes                     # imports the function to create the agent and tool nodes.


def build_graph(tools: list):                            # creates and returns the complete langgraph workflow.
    agent_node, tool_node = create_nodes(tools)

    builder = StateGraph(AgentState)                           # create a new workflow grapg.
    builder.add_node("agent", agent_node) 
    builder.add_node("tools", tool_node)

    builder.add_edge(START, "agent")
    builder.add_conditional_edges("agent", tools_condition)          # add a conditional routing from the agent node to the tools node based on the tools_condition function.
    builder.add_edge("tools", "agent")                               # after a tool finishes the results goes back to the AI.

    return builder.compile(checkpointer=MemorySaver())               # complies the workflow to run.
