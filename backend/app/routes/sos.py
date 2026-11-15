import logging

from fastapi import APIRouter

from ..gemini_client import generate_json
from ..schemas import AlertRequest, SOSRequest

router = APIRouter()
log = logging.getLogger("roam.sos")

# Fixed values, written in code so they are always accurate.
HELPLINES = [
    {"name": "Police", "number": "100"},
    {"name": "Ambulance", "number": "108"},
    {"name": "Women Helpline", "number": "1091"},
    {"name": "National Emergency Number", "number": "112"},
]


@router.post("/classify")
async def classify(req: SOSRequest):
    prompt = f"""A person in {req.city}, India reports this emergency: "{req.description}"

1. Classify it as "medical" (injury, illness, accident) or "situational" (crime, harassment, theft, lost, unsafe situation).
2. If medical, list 4 to 5 real, well-known hospitals near {req.city}. If situational, list 4 to 5 real police stations near {req.city}.
Reply with VALID JSON ONLY, exactly:
{{"type": "medical" or "situational",
  "places": [{{"name": "...", "address": "..."}}]}}"""

    data = await generate_json(prompt)
    etype = data.get("type") if data.get("type") in ("medical", "situational") else "situational"
    return {"type": etype, "places": data.get("places", []), "helplines": HELPLINES}


@router.post("/alert")
async def alert(req: AlertRequest):
    # Placeholder: later, write to a database and notify contacts.
    log.warning("SOS ALERT user=%s location=%s time=%s", req.user_id, req.location, req.timestamp)
    return {"status": "received", "sync": "pending"}
