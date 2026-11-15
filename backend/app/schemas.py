from pydantic import BaseModel, Field


class ItineraryRequest(BaseModel):
    destination: str = "Udaipur"
    budget: int = Field(15000, ge=0)
    duration: int = Field(3, ge=1, le=30)
    transport: str = "Train"
    hotel: str = "Mid-range"


class SOSRequest(BaseModel):
    description: str = Field(..., min_length=3)
    city: str = "Indore, Madhya Pradesh"


class AlertRequest(BaseModel):
    location: str
    timestamp: str
    user_id: str = "anonymous"
