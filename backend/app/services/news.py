import httpx

from ..config import GNEWS_API_KEY


async def get_travel_alerts(destination: str) -> list[dict]:
    """Up to 3 recent articles; empty list on failure or when nothing is happening."""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(
                "https://gnews.io/api/v4/search",
                params={
                    "q": f"{destination} travel advisory OR flooding OR disruption",
                    "lang": "en", "country": "in", "max": 3, "apikey": GNEWS_API_KEY,
                },
            )
            r.raise_for_status()
        return [
            {"title": a["title"], "url": a["url"], "source": a.get("source", {}).get("name", "")}
            for a in r.json().get("articles", [])
        ]
    except Exception:
        return []
