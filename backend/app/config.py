import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", "")
GNEWS_API_KEY = os.getenv("GNEWS_API_KEY", "")
# If Google retires the model, the 404 error message names the current one.
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
