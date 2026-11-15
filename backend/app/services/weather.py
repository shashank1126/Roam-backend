import httpx

from ..config import WEATHER_API_KEY


async def get_weather(city: str, days: int = 3) -> dict | None:
    """Returns forecast info, or None on any failure (never blocks the itinerary)."""
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(
                "https://api.weatherapi.com/v1/forecast.json",
                params={"key": WEATHER_API_KEY, "q": city, "days": days, "aqi": "no", "alerts": "no"},
            )
            r.raise_for_status()
        forecast = []
        for d in r.json()["forecast"]["forecastday"]:
            day = d["day"]
            forecast.append({
                "date": d["date"],
                "condition": day["condition"]["text"],
                "min_temp_c": day["mintemp_c"],
                "max_temp_c": day["maxtemp_c"],
                "chance_of_rain": day.get("daily_chance_of_rain", 0),
            })
        first = forecast[0]
        return {
            **first,
            "rain_alert": any(f["chance_of_rain"] > 60 for f in forecast),
            "forecast": forecast,
        }
    except Exception:
        return None
