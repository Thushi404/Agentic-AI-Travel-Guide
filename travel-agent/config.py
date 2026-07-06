import os                       # it is used to read environment variables.
from dotenv import load_dotenv

load_dotenv()               # makes the variables available inside the python code

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")        # this gets the OPENAI_API_KEY from the .env file  
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.5")

OPENMETEO_BASE_URL = os.getenv("OPENMETEO_BASE_URL", "https://api.open-meteo.com/v1")
GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is missing in .env")    # this checks whether the open api key exists.

if not GEOAPIFY_API_KEY:
    raise ValueError("GEOAPIFY_API_KEY is missing in .env")   