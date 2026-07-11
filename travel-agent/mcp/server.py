import sys                            # working with file and folder paths.
import os                             # access python system settings.

# Append travel-agent/ to END of sys.path so the installed mcp package
# (in site-packages) is found before the local mcp/ folder.
_parent = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))             # this gets the parent directory of the current file.
if _parent not in sys.path:                                                       # add the project folder to python's search path.
    sys.path.append(_parent)

from mcp.server.fastmcp import FastMCP                                        # import the FastMCP class from the mcp.server.fastmcp module.
from tools.weather import get_weather                                         # import the get_weather function from the tools.weather module.
from tools.maps import search_places, can_walk
from tools.itinerary import create_itinerary

mcp = FastMCP("Travel Agent Tools")                                           # creates the mcp server named "Travel Agent Tools".


@mcp.tool()                                                                   # decorator to register the function as a tool in the mcp server.
def weather_tool(location: str, day: str = "today") -> dict:
    """Get current or forecast weather for a city.

    Args:
        location: City or place name, e.g. Paris or Tokyo.
        day: Weather day - 'today' or 'tomorrow'.
    """
    return get_weather(location, day)                                         # call the weather function from the tools.weather module.


@mcp.tool()
def places_tool(                                                              # function searches for places such as attractions and restaurents.
    near: str,
    category: str = "attractions",
    radius_m: int = 5000,
    limit: int = 5,
) -> dict:
    """Find places such as attractions, restaurants, cafes, or hotels near a location.

    Args:
        near: Location to search near, e.g. Eiffel Tower or central Paris.
        category: Place type - attractions, restaurants, coffee shops, hotels, parks, museums.
        radius_m: Search radius in meters.
        limit: Number of places to return.
    """
    return search_places(near, category, radius_m, limit)                    # call the search_places function from the tools.maps module.


@mcp.tool()
def walking_tool(origin: str, destination: str) -> dict:
    """Check distance and estimated walking time between two locations.

    Args:
        origin: Starting location.
        destination: Destination location.
    """
    return can_walk(origin, destination)


@mcp.tool()
def itinerary_tool(destination: str, days: int = 1, budget: str = "medium") -> dict:
    """Create a day-wise travel itinerary with attractions, food, and packing tips.

    Args:
        destination: Travel destination city or region.
        days: Number of days for the trip (1 to 7).
        budget: Budget level - 'low', 'medium', or 'high'.
    """
    return create_itinerary(destination, days, budget)


if __name__ == "__main__":             # run the server only if this script is executed directly (not imported as a module).
    mcp.run()                          # start the mcp server.
