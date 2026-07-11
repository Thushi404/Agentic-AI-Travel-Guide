import os                              # Import the os module to access environment variables
from dotenv import load_dotenv         # Load environment variables from .env file

load_dotenv()                            # reads the .env file in the project.

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")            # Get the GeoAPIfy API key from environment variables

if not OPENAI_API_KEY:                                       # raises an error if the OpenAI API key is missing in the .env file.
    raise ValueError("OPENAI_API_KEY is missing in .env")

if not GEOAPIFY_API_KEY:                                     # raises an error if the Geoapify API key is missing in the .env file.
    raise ValueError("GEOAPIFY_API_KEY is missing in .env")
