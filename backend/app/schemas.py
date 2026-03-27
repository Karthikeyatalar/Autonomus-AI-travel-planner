from pydantic import BaseModel, Field
from typing import List, Optional

# Auth Schemas
class UserCreate(BaseModel):
    username: str
    password: str
    role: Optional[str] = "user"

class UserOut(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Existing Travel Schemas
class TravelQuery(BaseModel):
    source: str = Field(..., min_length=1)
    destination: str = Field(..., min_length=1)
    start_date: str = Field(..., min_length=1)
    end_date: str = Field(..., min_length=1)
    budget: str = Field(..., min_length=1)
    travel_mode: str = "Flight"
    interests: Optional[List[str]] = []

class DailyPlan(BaseModel):
    day: int
    date: str
    description: str
    activities: List[str]
    places: Optional[List[str]] = []
    accommodation: Optional[str] = None
    cost_estimate: Optional[str] = None

class RouteStop(BaseModel):
    stop: str
    drive_time: Optional[str] = None
    highlight: Optional[str] = None

class HotelSuggestion(BaseModel):
    name: str
    type: Optional[str] = None        # e.g. "Budget", "Mid-range", "Luxury"
    price_per_night: Optional[str] = None
    rating: Optional[str] = None
    location: Optional[str] = None
    highlights: Optional[List[str]] = []

class TravelPlan(BaseModel):
    destination: str
    total_cost_estimate: str
    itinerary: List[DailyPlan]
    road_route: Optional[List[RouteStop]] = None
    hotels: Optional[List[HotelSuggestion]] = None
