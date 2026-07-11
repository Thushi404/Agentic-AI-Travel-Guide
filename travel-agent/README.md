# Travel Agent AI

An AI-powered travel planning assistant built with **LangGraph** and **MCP (Model Context Protocol)**. It helps users plan trips by providing weather forecasts, nearby places, walking distances, and day-wise itineraries through a conversational interface.

---

## Features

- **Weather** — Get current or forecast weather for any city
- **Nearby Places** — Find attractions, restaurants, cafes, hotels, and parks near a location
- **Walking Distance** — Check walking time and distance between two locations
- **Itinerary Planner** — Generate a day-wise travel itinerary with budget options

---

## Tech Stack

| Layer | Technology |
|---|---|
| AI Framework | LangGraph |
| Tool Protocol | MCP (Model Context Protocol) via FastMCP |
| LLM | OpenAI GPT-4o Mini |
| MCP Adapter | langchain-mcp-adapters |
| Maps & Places | Geoapify API |
| Language | Python 3.10+ |

---

## Project Structure

```
travel-agent/
├── app.py                  # Main entry point (CLI chat loop)
├── config.py               # Loads API keys from .env
├── prompts.py              # System prompt for the AI agent
├── requirements.txt        # Python dependencies
│
├── graph/
│   ├── graph.py            # Builds and compiles the LangGraph StateGraph
│   ├── nodes.py            # Agent node and Tool node definitions
│   └── state.py            # AgentState TypedDict
│
├── mcp/
│   └── server.py           # FastMCP server exposing travel tools
│
└── tools/
    ├── weather.py          # Weather tool logic
    ├── maps.py             # Places and walking distance tool logic
    └── itinerary.py        # Itinerary generation logic
```

---

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/Thushi404/Agentic-AI-Travel-Guide.git
cd Agentic-AI-Travel-Guide/travel-agent
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file
```
OPENAI_API_KEY=your_openai_api_key
GEOAPIFY_API_KEY=your_geoapify_api_key
OPENAI_MODEL=gpt-4o-mini
```

> Get your OpenAI API key at [platform.openai.com](https://platform.openai.com/api-keys)
> Get your Geoapify API key at [myprojects.geoapify.com](https://myprojects.geoapify.com)

---

## Run

```bash
python app.py
```

### Example conversation

```
Travel Agent (LangGraph + MCP)
Type 'quit' to exit | 'clear' to start a new session

You: Plan a 3-day trip to Paris with a medium budget
Assistant: Here is your 3-day Paris itinerary...

You: What is the weather like in Paris today?
Assistant: The current weather in Paris is...

You: Find restaurants near the Eiffel Tower
Assistant: Here are some restaurants near the Eiffel Tower...
```

### Commands

| Command | Action |
|---|---|
| `quit` / `exit` / `q` | Exit the application |
| `clear` | Start a new conversation session |

---

## How It Works

1. `app.py` starts a **MultiServerMCPClient** which launches `mcp/server.py` as a subprocess
2. The MCP server exposes 4 tools over **stdio transport**
3. Tools are loaded into a **LangGraph StateGraph** with an agent node and a tool node
4. The agent (LLM) decides which tool to call based on the user's message
5. Results are returned to the agent and a final response is sent to the user

---

## Dependencies

```
langchain-openai
langchain-core
langgraph
langchain-mcp-adapters
mcp
python-dotenv
requests
```
