# Booking URLs come from OUR table, never from the AI, so a made-up link can't reach the user.
VERIFIED_LINKS = {
    "irctc": "https://www.irctc.co.in",
    "makemytrip": "https://www.makemytrip.com",
    "booking.com": "https://www.booking.com",
    "ixigo": "https://www.ixigo.com",
    "goibibo": "https://www.goibibo.com",
    "redbus": "https://www.redbus.in",
    "yatra": "https://www.yatra.com",
    "airbnb": "https://www.airbnb.co.in",
    "oyo": "https://www.oyorooms.com",
}


def attach_links(platforms) -> list[dict]:
    result = []
    for item in platforms or []:
        if not isinstance(item, dict):
            continue
        name = str(item.get("platform", "")).lower().replace(" ", "")
        for key, url in VERIFIED_LINKS.items():
            if key in name:
                result.append({"purpose": item.get("purpose", ""),
                               "platform": item.get("platform", key), "url": url})
                break
    return result
