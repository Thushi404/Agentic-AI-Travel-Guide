import math                              # used for distance calculations 
import requests
from config import GEOAPIFY_API_KEY


CATEGORY_MAP = {                                     # converts user-friendly words into geoapify categories.
    "attractions": "tourism.sights",
    "tourist attractions": "tourism.sights",
    "restaurants": "catering.restaurant",
    "restaurant": "catering.restaurant",
    "coffee": "catering.cafe",
    "coffee shops": "catering.cafe",
    "cafes": "catering.cafe",
    "hotels": "accommodation.hotel",
    "parks": "leisure.park",
    "museums": "entertainment.museum",
    "indoor": "entertainment.museum",
}


def haversine_km(lat1, lon1, lat2, lon2) -> float:          # calculate the distance between two GPS coordinates using the Haversine formula .
    radius = 6371

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)

    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(delta_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))    
    return round(radius * c, 2)


def geocode_location(query: str) -> dict:                # converts a place name into coordinates using the Geoapify Geocoding API.
    url = "https://api.geoapify.com/v1/geocode/search"

    try:
        response = requests.get(
            url,
            params={
                "text": query,
                "format": "json",
                "limit": 1,
                "apiKey": GEOAPIFY_API_KEY,
            },
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()

        results = data.get("results", [])
        if not results:
            return {"error": f"Could not find location: {query}"}

        place = results[0]

        return {
            "name": place.get("formatted", query),
            "lat": place.get("lat"),
            "lon": place.get("lon"),
            "city": place.get("city"),
            "country": place.get("country"),
        }

    except requests.RequestException as error:                          # error handling for the geocoding request.
        return {"error": f"Geoapify geocoding failed: {str(error)}"}


def search_places(
    near: str,
    category: str = "attractions",
    radius_m: int = 5000,
    limit: int = 5,
) -> dict:
    center = geocode_location(near)

    if "error" in center:
        return center

    geoapify_category = CATEGORY_MAP.get(category.lower(), category)
    url = "https://api.geoapify.com/v2/places"

    try:
        response = requests.get(
            url,
            params={
                "categories": geoapify_category,
                "filter": f"circle:{center['lon']},{center['lat']},{radius_m}",
                "bias": f"proximity:{center['lon']},{center['lat']}",
                "limit": limit,
                "apiKey": GEOAPIFY_API_KEY,
            },
            timeout=15,
        )
        response.raise_for_status()
        data = response.json()

        places = []

        for feature in data.get("features", []):
            props = feature.get("properties", {})
            lat = props.get("lat")
            lon = props.get("lon")

            distance_km = None
            if lat and lon:
                distance_km = haversine_km(center["lat"], center["lon"], lat, lon)

            places.append(
                {
                    "name": props.get("name") or props.get("address_line1") or "Unnamed place",
                    "address": props.get("formatted"),
                    "distance_km": distance_km,
                    "categories": props.get("categories", []),
                }
            )

        return {
            "near": center["name"],
            "category": category,
            "radius_m": radius_m,
            "results": places,
        }

    except requests.RequestException as error:
        return {"error": f"Places API failed: {str(error)}"}


def can_walk(origin: str, destination: str) -> dict:
    start = geocode_location(origin)
    end = geocode_location(destination)

    if "error" in start:
        return start

    if "error" in end:
        return end

    distance_km = haversine_km(start["lat"], start["lon"], end["lat"], end["lon"])
    walking_minutes = round((distance_km / 4.8) * 60)

    return {
        "origin": start["name"],
        "destination": end["name"],
        "distance_km": distance_km,
        "estimated_walking_minutes": walking_minutes,
        "walkable": distance_km <= 3,
        "advice": "Walkable" if distance_km <= 3 else "Better to use public transport or taxi",
    }