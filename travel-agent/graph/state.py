from typing import Annotated                          # used to attach extra information to a type.
from typing_extensions import TypedDict               # used to define a dictionary with specific keys and value types.
from langgraph.graph.message import add_messages      # used to add messages to the existing conversation histrory.


class AgentState(TypedDict):                         # creates a dictionary type for the agent's state, which includes a list of messages.
    messages: Annotated[list, add_messages]          # merge new messages into the list using add_messages function.
