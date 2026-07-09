import json
from tools.weather import get_weather
from tools.maps import search_places, can_walk
from tools.itinerary import create_itinerary


class MCPClient:                            # stores all available tools and allows the chatbot to call them.
    """
    MCP-equivalent local tool client.

    This demonstrates:
    1. Tool discovery
    2. Tool schema exposure
    3. Tool invocation
    4. Separation between LLM and external APIs
    """

    def __init__(self):                            # constructor initializes the tool functions available to the chatbot.
        self.tool_functions = {
            "get_weather": get_weather,
            "search_places": search_places,
            "can_walk": can_walk,
            "create_itinerary": create_itinerary,
        }

    def discover_tools(self):                        # tools discovery , this method returns the list of available tools and helps the llm decide which tool to use.
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_weather",                   # gets weather for a given location and day.
                    "description": "Get current or forecast weather for a city.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {
                                "type": "string",
                                "description": "City or place name, for example Paris or Tokyo.",
                            },
                            "day": {
                                "type": "string",
                                "enum": ["today", "tomorrow"],
                                "description": "Weather day.",
                            },
                        },
                        "required": ["location"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "search_places",                    # find nearby places of a given category around a location.
                    "description": "Find places such as attractions, restaurants, cafes, hotels, parks, or museums near a location.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "near": {
                                "type": "string",
                                "description": "Location to search near, for example Eiffel Tower.",
                            },
                            "category": {
                                "type": "string",
                                "description": "Place type: attractions, restaurants, coffee shops, hotels, parks, museums, indoor.",
                            },
                            "radius_m": {
                                "type": "integer",
                                "description": "Search radius in meters.",
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Number of places to return.",
                            },
                        },
                        "required": ["near", "category"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "can_walk",                                # check whether two locations are walkable.
                    "description": "Check distance and estimated walking time between two locations.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "origin": {"type": "string"},
                            "destination": {"type": "string"},
                        },
                        "required": ["origin", "destination"],
                    },
                },
            },
            {
                "type": "function",
                "function": {
                    "name": "create_itinerary",                        # creates a travel pan for a given destination, number of days, and budget.
                    "description": "Create a day-wise travel itinerary with attractions, food suggestions, and packing tips.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "destination": {"type": "string"},
                            "days": {"type": "integer"},
                            "budget": {
                                "type": "string",
                                "enum": ["low", "medium", "high"],
                            },
                        },
                        "required": ["destination", "days"],
                    },
                },
            },
        ]

    def call_tool(self, name: str, arguments: dict) -> str:                 # this method runs a selected tools.
        if name not in self.tool_functions:                                    # tool validation.
            return json.dumps({"error": f"Tool not found: {name}"})               # tool execution.

        try:
            result = self.tool_functions[name](**arguments)
            return json.dumps(result, ensure_ascii=False)
        except Exception as error:                                   # error handling , if anything goes wrong it returns the error as json instead of crashing the program.
            return json.dumps({"error": str(error)})