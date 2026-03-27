from .schemas import TravelQuery, TravelPlan, DailyPlan, RouteStop, HotelSuggestion
from datetime import datetime, timedelta
import asyncio
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

def _build_prompt(query: TravelQuery) -> str:
    interests_str = ", ".join(query.interests) if query.interests else "general sightseeing"
    is_car = query.travel_mode == "Car"

    route_instruction = ""
    route_format = ""
    if is_car:
        route_instruction = "\n- Since the travel mode is Car/Road Trip, suggest a REAL and SPECIFIC road route. Use actual city/town names as waypoints (NOT placeholders). Include real highway/route numbers (e.g. NH48, NH66) and realistic drive times between each stop."
        route_format = """,
  "road_route": [
    {"stop": "Exact starting city (e.g. Mumbai)", "drive_time": null, "highlight": "Your starting point"},
    {"stop": "Real waypoint city/town name (e.g. Pune)", "drive_time": "~2 hrs via NH48", "highlight": "What to do / why stop here"},
    {"stop": "Another real waypoint if needed (e.g. Kolhapur)", "drive_time": "~2.5 hrs via NH48", "highlight": "Brief note"},
    {"stop": "Exact destination city", "drive_time": "~3 hrs via NH66", "highlight": "Arrival at your destination"}
  ]"""

    try:
        start_dt = datetime.strptime(query.start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(query.end_date, "%Y-%m-%d")
        total_days = (end_dt - start_dt).days + 1
        if total_days < 1: total_days = 1
    except:
        total_days = 3

    return f"""You are an expert travel planner. Create a detailed {total_days}-day travel itinerary for the following trip.{route_instruction}

Trip Details:
- From: {query.source}
- To: {query.destination}
- Start Date: {query.start_date} (Day 1)
- End Date: {query.end_date} (Day {total_days})
- Budget: {query.budget}
- Travel Mode: {query.travel_mode}
- Interests: {interests_str}

Respond ONLY with a valid JSON object in this exact format (no extra text, no markdown):
{{
  "destination": "{query.destination}",
  "total_cost_estimate": "estimated cost in INR e.g. ₹45,000 - ₹60,000",
  "itinerary": [
    {{
      "day": 1,
      "date": "YYYY-MM-DD",
      "description": "Brief overview of arrival day",
      "places": ["Real landmark 1", "Real landmark 2"],
      "activities": ["Activity 1", "Activity 2"],
      "accommodation": "Specific hotel name",
      "cost_estimate": "Daily estimate in INR"
    }},
    ... (one object for each of the {total_days} days)
  ]{route_format}
}}

CRITICAL RULES for accuracy:
- Every daily plan MUST contain exactly {total_days} days.
- GEOGRAPHIC INTEGRITY CHECK: You MUST ensure every landmark, restaurant, or hotel actually exists in {query.destination}. Do NOT invent locations.
- LOGICAL ROUTING: Places within a single day MUST be within 10-15km of each other to ensure a realistic travel schedule.
- NO PLACEHOLDERS: Use exact, real-world names (e.g. 'The British Museum', NOT 'the main museum').
- NO REPETITION: Every single spot listed across the entire {total_days}-day itinerary must be unique.
- All costs must be provided in Indian Rupees (₹) and should be realistic for the budget tier requested.
- If travel mode is "Car", ensure the road_route contains specific highway numbers and real-world waypoint towns.

Suggest 3 REAL hotels for the destination. Use hotels that exist in reality:
"hotels": [
  {{"name": "Actual Hotel Name", "type": "Budget", "price_per_night": "₹X,XXX", "rating": "3.8/5", "location": "Area", "highlights": ["Feature"]}},
  {{"name": "Actual Luxury Hotel", "type": "Luxury", "price_per_night": "₹XX,XXX", "rating": "4.8/5", "location": "Prime Area", "highlights": ["Spa", "Pool"]}}
]
Accuracy is your top priority. Cross-reference your internal knowledge base with current 2024 mapping data."""


def _mock_plan(query: TravelQuery) -> TravelPlan:
    """Fallback plan when Gemini API key is not configured."""
    interests = query.interests if query.interests else ["local sights"]
    travel_mode = query.travel_mode or "Flight"

    travel_mode_map = {
        "Flight": f"Board your flight from {query.source} to {query.destination}.",
        "Train": f"Enjoy a scenic train journey from {query.source} to {query.destination}.",
        "Bus": f"Travel by bus from {query.source} to {query.destination}.",
        "Car": f"Begin your road trip from {query.source} to {query.destination}.",
        "Cruise": f"Board your cruise from {query.source} to {query.destination}.",
    }
    travel_day_desc = travel_mode_map.get(travel_mode, f"Travel from {query.source} to {query.destination}.")

    road_route = None
    if travel_mode == "Car" and GOOGLE_API_KEY and GOOGLE_API_KEY != "your_google_api_key_here":
        try:
            import google.generativeai as genai
            genai.configure(api_key=GOOGLE_API_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")
            route_prompt = f"""List the real road route waypoints from {query.source} to {query.destination} by car.
Respond ONLY as a JSON array, no markdown:
[{{"stop": "City name", "drive_time": null, "highlight": "Starting point"}}, {{"stop": "Real city name", "drive_time": "~X hrs via NHxxx", "highlight": "Brief description"}}, ...]
Use real city/town names, real highway numbers. Include 2-4 waypoints total including start and end."""
            import asyncio
            loop = asyncio.get_event_loop()
            resp = loop.run_until_complete(loop.run_in_executor(None, lambda: model.generate_content(route_prompt)))
            raw = resp.text.strip().lstrip("```json").lstrip("```").rstrip("```")
            stops = json.loads(raw)
            road_route = [RouteStop(stop=s["stop"], drive_time=s.get("drive_time"), highlight=s.get("highlight")) for s in stops]
        except Exception:
            road_route = [
                RouteStop(stop=query.source, drive_time=None, highlight="Starting point of your road trip"),
                RouteStop(stop=query.destination, drive_time="Check maps for exact time", highlight="Arrival at your destination"),
            ]
    elif travel_mode == "Car":
        road_route = [
            RouteStop(stop=query.source, drive_time=None, highlight="Starting point — fill up your tank!"),
            RouteStop(stop=f"Add your Google API key for real waypoints between {query.source} & {query.destination}", drive_time="—", highlight="Enable AI for specific route stops"),
            RouteStop(stop=query.destination, drive_time="Check Google Maps for exact time", highlight="Your destination"),
        ]

    # --- NEW: Retrieve Data from Database ---
    from .database import SessionLocal
    from . import models
    
    db = SessionLocal()
    raw_dest = query.destination.lower().strip()
    query_dest = raw_dest.split(',')[0].replace(' city', '').replace(' destination', '').strip()

    db_dest = db.query(models.Destination).filter(
        (models.Destination.name.ilike(f"%{query_dest}%")) | 
        (query_dest.lower() == models.Destination.name)
    ).first()

    matched_places_flat = None
    matched_hotels = None

    if db_dest:
        matched_places_flat = [p.name for p in db_dest.places]
        matched_hotels = [
            HotelSuggestion(
                name=h.name, type=h.type, price_per_night=h.price_per_night,
                rating=h.rating, location=h.location, highlights=h.highlights
            ) for h in db_dest.hotels
        ]
    
    db.close()
    
    if not matched_places_flat:
        matched_places_flat = [
            f"Ancient Quarter of {query.destination}", f"{query.destination} City Square", f"{query.destination} Heritage Museum",
            f"Public Gardens in {query.destination}", f"Local Street Food Hub, {query.destination}", f"Iconic Landmark at {query.destination}",
            f"Viewpoint overlooking {query.destination}", f"Creative Art District of {query.destination}", f"{query.destination} Grand Market",
            f"Famous Local Temple/Church, {query.destination}", f"Sunset Point in {query.destination}", f"Historical Gate of {query.destination}"
        ]

    if not matched_hotels:
        matched_hotels = [
            HotelSuggestion(name=f"The Grand {query.destination} Hotel", type="Luxury", price_per_night="₹15,000+", rating="4.7/5", location="City Center", highlights=["Premium stay", "City views"]),
            HotelSuggestion(name=f"{query.destination} Business Inn", type="Mid-range", price_per_night="₹7,000", rating="4.2/5", location="Near Station", highlights=["Reliable", "Free Breakfast"]),
            HotelSuggestion(name=f"{query.destination} Budget Stay", type="Budget", price_per_night="₹2,500", rating="3.9/5", location="Downtown", highlights=["Affordable", "Clean"])
        ]

    try:
        start_dt = datetime.strptime(query.start_date, "%Y-%m-%d")
        end_dt = datetime.strptime(query.end_date, "%Y-%m-%d")
        total_days = (end_dt - start_dt).days + 1
        if total_days < 1: total_days = 1
    except:
        total_days = 3

    itinerary = []
    per_day = 2
    
    for d in range(1, total_days + 1):
        curr_date = (start_dt + timedelta(days=d-1)).strftime("%Y-%m-%d")
        start_idx = (d-1) * per_day
        end_idx = start_idx + per_day
        day_places = matched_places_flat[start_idx:end_idx]
        
        if not day_places or len(day_places) < per_day:
            needed = per_day - len(day_places)
            for i in range(needed):
                day_places.append(f"Unique Spot {d}-{i+1} in {query.destination}")

        if d == 1:
            desc = travel_day_desc
            act = [f"{travel_mode} from {query.source}", f"Check-in at {query.destination}", f"Visit {day_places[0]}"]
        elif d == total_days:
            desc = f"Final sights and prepare for departure."
            act = [f"Morning visit to {day_places[0]}", "Souvenir shopping", f"Return to {query.source}"]
        else:
            desc = f"Continuing to explore iconic sights — Day {d}."
            act = [f"Discover {p}" for p in day_places] + ["Local dining exploration"]

        itinerary.append(DailyPlan(
            day=d,
            date=curr_date,
            description=desc,
            places=day_places,
            activities=act,
            accommodation="Recommended Hotel" if d < total_days else "None",
            cost_estimate="₹9,500"
        ))

    return TravelPlan(
        destination=query.destination,
        total_cost_estimate=f"Within {query.budget}",
        road_route=road_route,
        hotels=matched_hotels,
        itinerary=itinerary
    )


async def generate_itinerary(query: TravelQuery) -> TravelPlan:
    if not GOOGLE_API_KEY or GOOGLE_API_KEY == "your_google_api_key_here":
        await asyncio.sleep(1.5)
        return _mock_plan(query)

    try:
        import google.generativeai as genai
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = _build_prompt(query)

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: model.generate_content(prompt))

        raw = response.text.strip()
        raw = re.sub(r"^```(?:json)?\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)

        data = json.loads(raw)

        road_route = None
        if query.travel_mode == "Car" and "road_route" in data:
            road_route = [
                RouteStop(
                    stop=r.get("stop", ""),
                    drive_time=r.get("drive_time"),
                    highlight=r.get("highlight"),
                )
                for r in data["road_route"]
            ]

        itinerary = []
        for d in data.get("itinerary", []):
            itinerary.append(DailyPlan(
                day=d.get("day", 1),
                date=d.get("date", ""),
                description=d.get("description", ""),
                places=d.get("places", []),
                activities=d.get("activities", []),
                accommodation=d.get("accommodation"),
                cost_estimate=d.get("cost_estimate"),
            ))

        hotels = None
        if "hotels" in data:
            hotels = [
                HotelSuggestion(
                    name=h.get("name", ""),
                    type=h.get("type"),
                    price_per_night=h.get("price_per_night"),
                    rating=h.get("rating"),
                    location=h.get("location"),
                    highlights=h.get("highlights", []),
                )
                for h in data["hotels"]
            ]

        return TravelPlan(
            destination=data.get("destination", query.destination),
            total_cost_estimate=data.get("total_cost_estimate", ""),
            itinerary=itinerary,
            road_route=road_route,
            hotels=hotels,
        )

    except Exception as e:
        print(f"[AI Agent] Gemini error: {e} — falling back to mock plan.")
        return _mock_plan(query)
