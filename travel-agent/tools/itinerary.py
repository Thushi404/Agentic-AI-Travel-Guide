from tools.maps import search_places
from tools.weather import get_weather


def create_itinerary(destination: str, days: int = 1, budget: str = "medium") -> dict:
    days = max(1, min(days, 7))

    weather = get_weather(destination, "today")
    attractions = search_places(destination, "attractions", radius_m=8000, limit=days * 3)
    restaurants = search_places(destination, "restaurants", radius_m=8000, limit=days * 2)
    cafes = search_places(destination, "coffee shops", radius_m=8000, limit=days)

    attraction_list = attractions.get("results", [])
    restaurant_list = restaurants.get("results", [])
    cafe_list = cafes.get("results", [])

    plan = []

    for day_number in range(1, days + 1):
        first_index = (day_number - 1) * 3

        day_attractions = attraction_list[first_index:first_index + 3]
        lunch = restaurant_list[(day_number - 1) % len(restaurant_list)] if restaurant_list else None
        coffee = cafe_list[(day_number - 1) % len(cafe_list)] if cafe_list else None

        plan.append(
            {
                "day": day_number,
                "morning": day_attractions[0] if len(day_attractions) > 0 else "Explore city center",
                "lunch": lunch if lunch else "Find a local restaurant nearby",
                "afternoon": day_attractions[1] if len(day_attractions) > 1 else "Visit a museum or park",
                "evening": day_attractions[2] if len(day_attractions) > 2 else "Walk around a popular area",
                "coffee_break": coffee if coffee else "Optional cafe stop",
            }
        )

    return {
        "destination": destination,
        "days": days,
        "budget": budget,
        "weather_summary": weather,
        "itinerary": plan,
        "packing_tip": "Carry an umbrella or raincoat." if weather.get("umbrella_needed") else "Normal light travel packing is enough.",
    }