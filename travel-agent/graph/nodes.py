from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import ToolNode               # imports langgraph's toolnode.
from config import OPENAI_API_KEY, OPENAI_MODEL       # imports the configuration values from config.py.
from prompts import SYSTEM_PROMPT


def create_nodes(tools: list):                                    # this function recieves a list of tools.
    llm = ChatOpenAI(model=OPENAI_MODEL, api_key=OPENAI_API_KEY)
    llm_with_tools = llm.bind_tools(tools)                        # connect the tools to the model.

    def agent_node(state):                                        # create the agent node.
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + list(state["messages"])
        response = llm_with_tools.invoke(messages)                                       # this send the message to the model.
        return {"messages": [response]}

    return agent_node, ToolNode(tools)                          # return two nodes (agent node and tool node).
