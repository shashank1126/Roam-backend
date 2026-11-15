import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import itinerary, sos

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Roam.io API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app.include_router(itinerary.router, prefix="/api/itinerary", tags=["itinerary"])
app.include_router(sos.router, prefix="/api/sos", tags=["sos"])


@app.get("/")
def root():
    return {"message": "Roam.io server running"}
