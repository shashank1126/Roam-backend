import asyncio

from fastapi import APIRouter

from ..booking_links import attach_links
from ..gemini_client import generate_json
from ..schemas import ItineraryRequest
from ..services.news import get_travel_alerts
from ..services.weather import get_weather

router = APIRouter()

START_CITY = "Indore"


def build_prompt(req: ItineraryRequest) -> str:
    return f"""You are a local travel curator who avoids generic tourist itineraries.
Plan a {req.duration}-day trip from {START_CITY} to {req.destination}, India.
Budget: Rs {req.budget}. Transport: {req.transport}. Hotel preference: {req.hotel}.

Rules:
- Favour local markets, traditional eateries, artisan communities and lesser-known experiences.
- Include recurring festivals, melas and local events, each marked with an asterisk (*) because exact dates vary by year.
- Mark any recommendation you are not confident about with an asterisk (*).
- Structure the plan day by day with morning, afternoon and evening activities.
- Only name trusted booking platforms suited to the transport mode (IRCTC, MakeMyTrip, Booking.com, Ixigo, Goibibo, RedBus, Yatra, Airbnb, OYO). Do NOT invent prices; give rough estimates only.
- Reply with VALID JSON ONLY (no markdown), in exactly this structure:
{{
  "destination": "{req.destination}",
  "duration": {req.duration},
  "distance": "approx distance from {START_CITY}",
  "transport": {{"mode": "{req.transport}", "estimated_fare": "..."}},
  "hotel": {{"type": "{req.hotel}", "estimated_cost_per_night": "..."}},
  "days": [{{"day": 1, "morning": "...", "afternoon": "...", "evening": "..."}}],
  "local_events": ["..."],
  "hidden_gems": ["..."],
  "booking_platforms": [{{"purpose": "...", "platform": "..."}}],
  "total_budget": "...",
  "route": {{"from": "{START_CITY}", "to": "{req.destination}"}}
}}"""


@router.post("/generate")
async def generate_itinerary(req: ItineraryRequest):
    itinerary = await generate_json(build_prompt(req))  # raises HTTPException on failure

    # Weather and news run in parallel; each has its own error handling.
    weather, news = await asyncio.gather(
        get_weather(req.destination), get_travel_alerts(req.destination)
    )

    itinerary["booking_platforms"] = attach_links(itinerary.get("booking_platforms"))
    itinerary["weather"] = weather
    itinerary["travel_alerts"] = news
    return itinerary
