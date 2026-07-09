# Plain tool implementations - imported by mcp/server.py
# LangGraph receives these as tools via MultiServerMCPClient in app.py
from tools.weather import get_weather
from tools.maps import search_places, can_walk
from tools.itinerary import create_itinerary
