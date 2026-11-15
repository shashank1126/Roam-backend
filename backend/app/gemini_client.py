import json
import re

from fastapi import HTTPException
from google import genai
from google.genai import errors, types

from .config import GEMINI_API_KEY, GEMINI_MODEL

_client = None


def _get_client() -> genai.Client:
    global _client
    if _client is None:
        if not GEMINI_API_KEY:
            raise HTTPException(500, "GEMINI_API_KEY is missing in .env")
        _client = genai.Client(api_key=GEMINI_API_KEY)
    return _client


def clean_json(text: str) -> str:
    """Strip markdown code fences Gemini sometimes wraps around its answer."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


async def generate_json(prompt: str) -> dict:
    try:
        response = await _get_client().aio.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                temperature=0.7,
            ),
        )
        return json.loads(clean_json(response.text))
    except json.JSONDecodeError:
        raise HTTPException(502, "Gemini returned invalid JSON. Please try again.")
    except errors.APIError as e:
        # 429 = free-tier quota hit, 404 = model name retired, etc.
        raise HTTPException(e.code if e.code in (404, 429) else 502, f"Gemini error: {e.message}")
